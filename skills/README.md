# Skills 技能体系

## 技能总览

| 技能 | 用途 | 触发方式 |
|------|------|---------|
| **deep-research** | 深度调研，输出专业研究报告（MD / HTML） | `/deep-research` 或 调研/研究/分析 |
| **diagram** | 专业图表生成（PNG / HTML / Mermaid DSL） | `/diagram` 或 画图/图表 |
| **preview-md** | MD 文件浏览器预览，支持 Mermaid 图表实时渲染 | `/preview-md` 或 预览文档 |
| **task-start** | 任务启动：需求对焦 + UI 原型 + 方案设计 | `/task-start` 或 新功能/实现xxx |
| **task-execute** | 持续执行：跨会话大型任务进度管理 | `/task-execute` |
| **task-finish** | 任务收尾：CR 自检 + 复盘沉淀 | `/task-finish` 或 提交代码 |

---

## 三档输出体系

报告和图表按使用场景分三档，共用一套设计规范（`shared/styles/` 色板 + diagram 配色），视觉风格统一。

### 日常：MD + Mermaid DSL + preview-md

适用于内部文档、方案设计、技术调研等日常场景。

```
deep-research → MD 报告 + Mermaid DSL 图表 → preview-md 浏览器渲染
```

- **报告**：Markdown 文件，可版本控制、可 diff
- **图表**：Mermaid DSL 文本嵌入 MD 代码块（```` ```mermaid ````）
- **渲染**：preview-md 实时预览，Mermaid 图表自动渲染为 SVG
- **优势**：轻量、可 diff、GitHub/GitLab 原生支持

### 正式：HTML 报告 + HTML 图表

适用于对外交付、正式研究报告、需要精美排版的场景。

```
deep-research → HTML 报告（内嵌 SVG 图表）→ 浏览器直接打开
```

- **报告**：自包含 HTML 文件，专业蓝灰主题，内含侧边目录、评分条、对比块等富组件
- **图表**：SVG 内嵌在报告中，支持 hover 等交互
- **优势**：零依赖打开、打印友好、视觉专业

### 其它：PNG 图表

适用于 PPT 插入、邮件附件、Mermaid 未覆盖的图表类型。

```
diagram → PNG 截图 → 插入任意场景
```

- **图表**：Playwright 截图生成高清 PNG
- **适用**：SWOT、鱼骨图、文氏图、雷达图、热力图等 Mermaid 无法覆盖的类型

---

## 图表覆盖范围

### Mermaid DSL 支持（20 种）

日常场景优先输出 Mermaid DSL，preview-md 实时渲染。

| 类型 | Mermaid 语法 | 说明 |
|------|-------------|------|
| flowchart | `flowchart TD/LR` | 流程图 |
| sequence | `sequenceDiagram` | 时序图 |
| class | `classDiagram` | 类图 |
| state | `stateDiagram-v2` | 状态图 |
| er | `erDiagram` | ER 图 |
| gantt | `gantt` | 甘特图 |
| mindmap | `mindmap` | 思维导图 |
| timeline | `timeline` | 时间线 |
| c4 | `C4Context` | C4 架构图 |
| sankey | `sankey-beta` | 桑基图 |
| journey | `journey` | 旅程图 |
| architecture | `flowchart TD` + `subgraph` | 架构图（子图模式） |
| swimlane | `flowchart LR` + `subgraph` | 泳道图 |
| network | `flowchart TD` + `subgraph` | 网络图 |
| decision-tree | `flowchart TD` + 菱形 | 决策树 |
| dataflow | `flowchart LR` + `subgraph` | 数据流图 |
| orgchart | `flowchart TD` | 组织结构图 |
| bar / line | `xychart-beta` | 柱状图 / 折线图 |
| pie | `pie` | 饼图 |

### 仅 PNG / HTML（8 种）

Mermaid 无法覆盖，走 diagram skill 的 HTML 模板 + Playwright 截图。

| 类型 | 说明 |
|------|------|
| radar | 雷达图 |
| heatmap | 热力图 |
| scatter | 散点图 |
| funnel | 漏斗图 |
| waterfall | 瀑布图 |
| fishbone | 鱼骨图 |
| swot | SWOT 分析图 |
| venn | 文氏图 |

---

## 共享资源

```
skills/
  shared/
    styles/
      base.css              # 共享基础样式（排版、表格、代码块、callout 等）
      report-components.css  # HTML 报告专属组件（评分条、对比块、时间轴等）
```

- `base.css`：preview-md 和 HTML 报告共用，定义 CSS 变量、排版、18 种组件样式
- `report-components.css`：仅 HTML 报告使用的 5 种专业组件

---

## 任务工作流

```
task-start（启动）→ task-execute（执行）→ task-finish（收尾）
```

- **小任务**（1-2 文件）：直接动手，跳过 task-start
- **中任务**（有模糊点）：task-start 对焦需求，然后开发
- **大任务**（3+ 文件 / 新模块）：完整走 start → execute → finish
- **跨会话任务**：必须启用 task-execute 管理进度
