---
priority: P2
status: open
spec:
plan:
---

# Diagram Skill 独立发布

## 背景
diagram skill 已经足够成熟（v1.4.0，29 种图表），且几乎无外部依赖（唯一的 shared/base.css 已有本地副本），具备独立发布条件。

## 描述
将 diagram skill 拆分为独立 GitHub 仓库，发布为可安装的 Claude Code skill。

## 具体步骤
- [ ] 创建独立仓库 `claude-skill-diagram`
- [ ] 复制 `skills/diagram/` 全部内容
- [ ] 确认 `base.css` 本地副本完整，移除对 `shared/` 的任何引用
- [ ] 清理 SKILL.md 中 deep-research/writing 的调用方说明（改为通用描述）
- [ ] 写 README（安装方式、功能介绍、截图示例）
- [ ] 提交到社区 Registry（claude-skill-registry）
- [ ] 考虑做成 Plugin Marketplace 格式

## 验收标准
- 用户通过 `git clone` 安装后，所有 29 种图表均可正常生成
- README 有清晰的安装指引和效果截图
