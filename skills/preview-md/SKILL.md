---
name: preview-md
version: 1.1.0
last_updated: 2026-03-30
repository: https://github.com/312362115/claude
changelog: skills/preview-md/CHANGELOG.md
description: >
  MD 文件浏览器预览：GitHub 风格渲染 + 左侧自动目录。
  在完成方案设计（specs）或开发计划（plans）的 MD 文件后触发。
  询问用户是否要在浏览器中打开预览，确认后执行。
  触发词：方案写完、计划写完、review MD、预览文档。
  工作流位置：task-start 方案产出后 / 任意 MD 文档完成后
---

# MD 文件浏览器预览

> 写完方案/计划等需要 review 的 MD 文件后，用浏览器打开 GitHub 风格预览。

---

## 触发条件

当你（Claude）完成以下类型的 MD 文件创建或大幅修改时，**必须触发此 skill**：

1. 方案设计文档（`docs/specs/**/*.md`）
2. 开发计划文档（`docs/plans/**/*.md`）
3. 用户明确要求预览的任何 MD 文件

**不可跳过原则**：满足上述触发条件时，必须执行 Step 1 询问用户是否预览。Claude 不得以任何理由（如"纯后端文档"、"内容简单"、"不涉及 UI"等）自行判断跳过。是否预览由用户决定，不由 Claude 决定。

**不触发** 的场景：
- **非 `.md` 文件**：HTML、JSON、YAML 等其他格式文件不走此 skill（HTML 原型直接用 `open` 命令打开）
- memory 文件、CLAUDE.md、README.md 等非 review 类文件
- 对 MD 文件的小幅修改（如修错别字、更新状态标记）

---

## 执行流程

### Step 1: 询问用户

MD 文件写完后，向用户提问：

```
文件已创建：<文件路径>
要在浏览器中打开预览吗？
```

### Step 2: 用户确认后打开预览

用户确认后，执行：

```bash
node ~/.claude/skills/preview-md/scripts/preview-md.mjs <md-file-absolute-path>
```

### Step 3: 等待反馈

预览打开后，等待用户 review 反馈，根据反馈修改文档内容。

---

## 注意事项

- 脚本位置在 `~/.claude/skills/preview-md/scripts/preview-md.mjs`
- 脚本会生成临时 HTML 文件并用默认浏览器打开
- 渲染特性：GitHub Markdown CSS + 左侧固定目录（h1-h4）+ 滚动高亮 + 平滑跳转

---

## 更新检查

任务完成后，检查本 skill 是否有新版本。规则：

1. **频率控制（每天一次）**：用 Read 读取 `~/.claude/.skill-check-preview-md`。如果文件内容是今天的日期（YYYY-MM-DD），跳过后续所有步骤。如果文件不存在或日期不是今天，继续
2. **读取本地版本**：从本文件 frontmatter 的 `version` 字段获取
3. **获取远端版本**：用 WebFetch 请求 `https://raw.githubusercontent.com/312362115/claude/main/skills/preview-md/VERSION`（仅含版本号）
4. **写入检查标记**：用 Bash 执行 `echo "$(date +%Y-%m-%d)" > ~/.claude/.skill-check-preview-md`
5. **比对与更新**：版本相同则静默跳过。版本不同则告知用户并询问是否更新：
   ```
   preview-md skill 有新版本可用：<本地版本> → <远端版本>
   查看更新内容：https://github.com/312362115/claude/blob/main/skills/preview-md/CHANGELOG.md
   是否立即更新？
   ```
   用户确认后，先判断安装方式再执行更新：
   - 用 Bash 执行 `git -C <本skill所在目录的父目录> remote get-url origin 2>/dev/null`
   - **如果输出包含 `312362115/claude`**（整仓安装）：执行 `git -C <仓库根目录> pull origin main`
   - **否则**（单 skill 安装）：依次 WebFetch 以下文件并覆盖本地对应文件：
     - `https://raw.githubusercontent.com/312362115/claude/main/skills/preview-md/SKILL.md`
     - `https://raw.githubusercontent.com/312362115/claude/main/skills/preview-md/VERSION`
     - `https://raw.githubusercontent.com/312362115/claude/main/skills/preview-md/CHANGELOG.md`
   - 更新完成后提示用户重新加载 skill（开始新会话或 `/reload-plugins`）
6. **容错**：任何步骤失败时静默跳过，不报错不打扰用户
