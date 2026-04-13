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

## 扩展语法：terminal / flow 代码块

preview-md 在标准 Markdown 之上提供两种**轻量图示代码块**，专为"不想调 diagram skill 但又想比纯文字更有画面感"的场景设计。生产端（writing / deep-research 等）应按本节约定输出。

### ```terminal — 终端窗口

展示命令行操作、CLI 输出、安装/启动步骤时使用。渲染为 macOS 风格的终端窗口（红黄绿圆点 + 标题栏）。

**何时用**：
- 展示一段命令执行（单条或多条）
- 展示命令的输出示例
- 开发指南/快速开始中的 setup 步骤

**何时别用**：
- 单条命令且没有特殊格式 → 用普通 `` ```bash `` 即可
- 纯代码片段（非 shell 语境）→ 用对应语言的代码块

**语法**：首行可选 `$ title` 作为窗口标题，其余为内容。

````markdown
```terminal
$ 快速开始
npm install
npm run dev
# 服务启动在 http://localhost:3000
```
````

### ```flow — 轻量流程图

展示流程、决策树、步骤串联时使用。比调 diagram skill 更快、更贴近正文，适合**简单到中等复杂度**的线性/分叉流程。

**何时用**：
- 方案中的"执行步骤"示意
- 决策树（含 `？`/`?` 的节点自动高亮为决策样式）
- 工作流阶段串联

**何时别用**：
- 复杂的多分叉合流、有向图 → 调 diagram skill 画真正的流程图
- 时序交互（多角色）→ 调 diagram skill 画时序图

**语法**：

| 形态 | 写法 | 渲染 |
|------|------|------|
| 竖向主干 | 每行一个节点，`↓` 单独一行作为连接符 | 主干 pill 居中列，↓ 对齐主干 |
| 横向流 | 一行内用 `→` 分隔多个节点 | 平铺横向 pill 链 |
| 横竖混合 | 主干竖向，某一行内嵌 `→ 分支` | 主干走中间列，分支向右延伸 |
| 决策节点 | 节点文本含 `？` 或 `?` | 黄底带边框 pill |
| 注释 | 节点后追加 `（xxx）` | 灰色注释文字挂在节点右侧 |

**示例**：

````markdown
```flow
task-manager
↓
task-start（对焦 + 方案）
↓
task-execute → 编码 → 调试
↓
需求完成？→ task-finish → 标 done
```
````

**设计原则**：
- flow 块中不要写长句，每个节点控制在 10 字内，超长的信息放正文说明
- `→` 扩展只用于挂 1-3 个分支节点；再多就该拆成多行或改调 diagram
- 一个 flow 块表达一个完整小流程，别把多个无关流程塞进同一个块

---
