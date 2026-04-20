---
priority: P1
status: in-progress
spec: （待创建）
plan: （待创建）
progress:
  - 2026-04-14 Layer 1 已落地：全局 git hook + gitleaks 8.30.1
---

# CI/CD 安全检测流水线

## 背景

security-audit skill 负责 AI 层面的安全审查（需要理解力的部分），但确定性的自动化检测（依赖漏洞、敏感信息、静态规则）应该由 CI/CD 流水线承担。两者互补：CI/CD 拦确定性问题，skill 审需要判断力的问题。

## 三层防线设计

```
pre-commit（本地）  →  PR Check（远端 CI）  →  Release Gate（AI skill）
拦敏感信息泄露         全量自动化扫描            AI 安全审查
<1s                   30-60s                   人工触发
```

### Layer 1: pre-commit（全局 git hook）

**配置方式**：全局 git hook，配一次所有仓库生效
**配置位置**：`~/.config/git/hooks/pre-commit`
**检查内容**：gitleaks 扫描 staged files，拦截 API key / token / password
**误报处理**：.gitleaksignore 白名单放行
**设计理由**：commit 频率高，必须快（<1s），只做最关键的一件事

### Layer 2: PR Check（GitHub Actions）

**配置方式**：项目级 `.github/workflows/security.yml`
**检查内容**：

| 检查项 | 工具 | 适用 |
|--------|------|------|
| 敏感信息全量扫描 | gitleaks | 所有项目 |
| 依赖漏洞 | npm audit | JS/TS |
| 依赖漏洞 | pip-audit | Python |
| 静态安全规则 | eslint-plugin-security | JS/TS |
| 静态安全规则 | bandit | Python |

**结果**：作为 PR status check，红灯不能合入

### Layer 3: Release Gate（security-audit skill）

由 security-audit skill 负责，详见 skill 体系扩建 backlog。
发版前触发，AI 审查注入/认证/敏感数据/配置/业务安全 5 个维度。

### 可选层: pre-push（暂不实施）

推送前跑依赖检查（npm audit --audit-level=high），需要时再启用。

## Hook 管理策略：全局 + 项目混合

```
全局 git hook（配一次，所有项目通用）
  ~/.config/git/hooks/pre-commit
    └─ gitleaks protect --staged

项目级 hook（按技术栈选择，跟着仓库走）
  JS/TS 项目 → husky + lint-staged → eslint-plugin-security
  Python 项目 → pre-commit 框架 → bandit
```

全局 hook 和项目 hook 共存：git 先跑全局的，再跑项目的。

## 技术栈适配

| 项目类型 | pre-commit（全局） | PR Check | Release Gate |
|---------|-------------------|----------|-------------|
| JS/TS 前端 | gitleaks | gitleaks + npm audit + eslint-plugin-security | security-audit skill |
| TS 后端 | gitleaks | gitleaks + npm audit + eslint-plugin-security | security-audit skill |
| Python 后端 | gitleaks | gitleaks + pip-audit + bandit | security-audit skill |
| 前后端混合 | gitleaks | 全部 | security-audit skill |

## 与 skill 体系的关系

- **security-audit skill**：CI/CD 是自动化前置，skill 是 AI 兜底，两者互补
- **release skill**：发版流程中先检查 CI 全绿，再触发 security-audit skill
- **task-finish**：涉及敏感模块改动时，提示跑快速扫描（可选）
