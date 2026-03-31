---
priority: P2
status: open
---

# MD Preview 升级 — 样式统一 + 图表实时渲染

## 背景

当前 preview-md 使用 GitHub 风格 CSS 渲染 Markdown。deep-research 的 HTML 报告模板（`html-report-template.html`）有一套更精致的专业蓝灰主题，两者风格割裂。同时 MD 报告中的图表只能以 PNG 静态图片引用，无法交互。

## 需求一：样式统一

将 HTML 报告模板的样式能力下沉到 preview-md，作为通用渲染风格：

1. **排版**：行高 1.8、段落呼吸感、标题间距优化
2. **表格**：斑马条纹、圆角边框、表头背景
3. **侧边目录**：滚动高亮、h2/h3 层级缩进（preview-md 已有，但样式可同步）
4. **代码块**：深色背景 + 语法高亮
5. **引用/提示框**：蓝色左边框 + 浅背景
6. **响应式 + 打印友好**

## 需求二：图表 DSL 嵌入 + 实时渲染

在 MD 中用文本 DSL 描述图表，preview 时调 diagram skill 渲染为 HTML/SVG 内嵌。

**两类图表，两种 DSL**：

1. **统计图**（bar/line/pie/radar 等）— 用 JSON 代码块，bridge.py 已支持：
   ````
   ```chart
   {"type": "bar", "title": "xxx", "data": {...}}
   ```
   ````

2. **结构图**（flowchart/sequence/mindmap 等）— 需要文本 DSL，待调研选型：
   ````
   ```flowchart
   用户请求 -> 负载均衡 -> 服务A
   服务A -> 数据库
   ```
   ````

**DSL 选型结论：Mermaid**（业界标准，GitHub/GitLab/Notion 原生支持，12 种图表类型，73K stars）。
两种渲染策略可选：
- **简单路径**：直接用 mermaid.js 渲染（npm 3M 周下载），快速上线
- **进阶路径**：写轻量 Mermaid 子集解析器 → 转为 diagram skill 模板 JSON → 自有渲染引擎，风格统一

**渲染流程**：
1. preview-md.mjs 解析 MD 时检测 `chart` / `flowchart` / `sequence` 等代码块
2. 统计图：提取 JSON → bridge.py -f html → 内嵌 SVG
3. 结构图：解析 DSL → 生成模板 JSON → 对应 HTML 模板渲染 → 内嵌
4. 普通 `![](xxx.png)` 引用保持原样（向后兼容）

**价值**：
- 图表可交互（hover 提示等），比 PNG 截图体验更好
- 不依赖 assets 目录中的 PNG 文件，减少文件管理
- 与 HTML 报告的图表体验一致
- 文本 DSL 可版本控制、可 diff，比二进制 PNG 更适合 git

## 关键点

- 从 `html-report-template.html` 提取通用 CSS 作为共享样式基础
- preview-md 和 HTML 报告模板共用一套 CSS 变量和排版规范
- 不影响 HTML 报告的专属组件（评分条、对比块等），那些仍留在报告模板中
- 图表渲染依赖 bridge.py，需确保 Python 环境和 playwright 可用
