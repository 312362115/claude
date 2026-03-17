---
name: preview-md
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

**不触发** 的场景：
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
node ~/.claude/scripts/preview-md.mjs <md-file-absolute-path>
```

### Step 3: 等待反馈

预览打开后，等待用户 review 反馈，根据反馈修改文档内容。

---

## 注意事项

- 脚本位置固定在 `~/.claude/scripts/preview-md.mjs`，全局可用
- 脚本会生成临时 HTML 文件并用默认浏览器打开
- 渲染特性：GitHub Markdown CSS + 左侧固定目录（h1-h4）+ 滚动高亮 + 平滑跳转
