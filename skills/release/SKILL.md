---
name: release
version: 1.0.0
last_updated: 2026-04-08
repository: https://github.com/312362115/claude
description: >
  发版自动化技能：CalVer 版本号 + 从 git log 生成 changelog + GitHub Releases。
  覆盖完整发版流程：版本号生成→changelog 生成→git tag→GitHub Release（或本地 changelog 文件）。
  在发版前自动触发 security-audit 安全审查（如果配置了 CI/CD 则检查 CI 状态）。
  触发词：发版、发布、release、生成 changelog、打 tag、版本发布。
  触发场景：功能开发完成准备发布、用户主动要求发版、里程碑完成。
---

# 发版（Release）

> 发版不只是打 tag，是一个质量门禁流程：安全审查→生成版本→创建 Release。

---

## 第一步：发版前检查

发版前必须确认以下条件：

```
准备发版
  │
  ├─ 1. 代码状态检查
  │   ├─ 工作区干净？（无未提交改动）
  │   ├─ 在正确的分支上？（main / release branch）
  │   └─ 已合并所有需要的 PR？
  │
  ├─ 2. CI 状态检查（如果有）
  │   └─ GitHub Actions 全绿？
  │
  ├─ 3. 安全审查
  │   └─ 提示用户：是否需要跑 security-audit？（上线服务强烈建议）
  │
  └─ 4. 测试验证
      └─ 核心功能是否经过验证？
```

**检查命令**：
```bash
# 工作区状态
git status

# CI 状态（GitHub）
gh run list --limit 5

# 未合并的 PR
gh pr list
```

任何检查不通过，**提示用户处理后再继续**，不强行发版。

---

## 第二步：确定版本号

### CalVer 格式

```
YYYY.MM.PATCH
```

| 部分 | 含义 | 示例 |
|------|------|------|
| YYYY | 年份 | 2026 |
| MM | 月份（不补零） | 4 |
| PATCH | 当月第几次发布（从 1 开始） | 1, 2, 3... |

**版本号生成逻辑**：

```bash
# 获取当前年月
YEAR=$(date +%Y)
MONTH=$(date +%-m)

# 查找当月已有的最大版本号
LATEST=$(git tag --list "${YEAR}.${MONTH}.*" --sort=-version:refname | head -1)

if [ -z "$LATEST" ]; then
  # 当月第一次发布
  VERSION="${YEAR}.${MONTH}.1"
else
  # 递增 PATCH
  PATCH=$(echo "$LATEST" | awk -F. '{print $3 + 1}')
  VERSION="${YEAR}.${MONTH}.${PATCH}"
fi

echo "版本号: $VERSION"
```

**示例**：
- 2026 年 4 月第 1 次发布 → `2026.4.1`
- 2026 年 4 月第 2 次发布 → `2026.4.2`
- 2026 年 5 月第 1 次发布 → `2026.5.1`

---

## 第三步：生成 Changelog

### 从 git log 提取

```bash
# 获取上一个 tag 到 HEAD 的所有提交
PREV_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

if [ -z "$PREV_TAG" ]; then
  # 没有历史 tag，取所有提交
  COMMITS=$(git log --oneline --pretty=format:"%s")
else
  COMMITS=$(git log ${PREV_TAG}..HEAD --oneline --pretty=format:"%s")
fi
```

### 按 type 分组

根据 commit message 的 `type(scope): desc` 格式自动分组：

```markdown
# Changelog — v2026.4.1

## 新功能（Features）
- **auth**: 支持 OAuth2 第三方登录
- **export**: 用户数据导出功能

## 修复（Fixes）
- **login**: 修复密码错误时返回 500 的问题
- **cache**: 修复缓存 key 冲突

## 重构（Refactoring）
- **api**: 统一错误响应格式

## 其他
- **docs**: 更新 API 文档
- **test**: 补充登录模块测试用例
```

**分组规则**：

| commit type | changelog 分组 |
|-------------|---------------|
| feat | 新功能（Features） |
| fix | 修复（Fixes） |
| refactor | 重构（Refactoring） |
| perf | 性能优化（Performance） |
| docs, test, chore, ci | 其他（如果没有 feat/fix/refactor 可省略） |

### Changelog 输出

- **有 GitHub**：嵌入 GitHub Release 的 body
- **无 GitHub**：写入 `docs/changelog/YYYY-MM-DD-v<版本号>.md`

---

## 第四步：创建 Release

### 方式 A：GitHub Release（优先）

```bash
# 创建 tag
git tag -a "v${VERSION}" -m "Release v${VERSION}"
git push origin "v${VERSION}"

# 创建 GitHub Release
gh release create "v${VERSION}" \
  --title "v${VERSION}" \
  --notes "$(cat <<'EOF'
<changelog 内容>
EOF
)"
```

### 方式 B：本地 Changelog 文件

如果项目不在 GitHub 或不需要 GitHub Release：

```bash
# 创建 tag
git tag -a "v${VERSION}" -m "Release v${VERSION}"

# 写入 changelog 文件
# 存入 docs/changelog/YYYY-MM-DD-v<版本号>.md
```

---

## 第五步：发版后

1. **通知用户**：发版完成，输出版本号和 Release URL
2. **更新 package.json / pyproject.toml**（如果项目需要版本号同步到配置文件）
3. **提醒**：如果有需要手动操作的部署步骤，列出来

---

## 完整发版流程

```
用户：发个版
  │
  ├─ Step 1: 发版前检查（代码状态 + CI + 安全）
  ├─ Step 2: 生成版本号（CalVer）
  ├─ Step 3: 生成 Changelog（从 git log）
  ├─ Step 4: 创建 Release（GitHub 或本地文件）
  └─ Step 5: 发版后处理
```

---

## 与其他 skill 的关系

```
task-finish（功能收尾）
  ↓
security-audit（发版前安全审查）
  ↓ 审查通过
release（本 skill — 发版）
```
