---
priority: P1
status: done
---

# 图表 DSL 联动 — Mermaid 输出 + MD 渲染

## 背景

当前三个 skill（报告、画图、渲染 MD）的联动现状：
- 报告 HTML + 画图 HTML — 已打通（图表内嵌）
- 报告 MD + 画图 PNG — 能用但笨（PNG 文件要维护在仓库里）
- 渲染 MD + 报告 CSS — 已打通（共享样式体系）
- **渲染 MD + 画图 — 断裂**（MD 里的结构图只能引用 PNG）

目标：结构图用 Mermaid DSL 嵌入 MD，preview-md 直接渲染，不再依赖 PNG 文件。

## 需求一：Diagram Skill 输出 Mermaid DSL

画图 skill 新增输出模式：结构图除 HTML/PNG 外，还能输出 Mermaid DSL 文本。

**覆盖范围**：

| DSL | 覆盖图表类型 |
|-----|-----------|
| Mermaid | flowchart / sequence / class / state / er / gantt / mindmap / timeline / c4 / sankey（10 种） |
| Graphviz (DOT) | architecture / swimlane（2 种，补 Mermaid 缺口） |

**不覆盖**：统计图 bar/line/pie/radar 等（继续走 bridge.py PNG）

**实现方式**：skill 指引调整，让 Claude 根据图表类型选择 Mermaid 或 DOT 输出。不需要写代码转换器。

## 需求二：Preview-md 渲染 DSL 代码块

preview-md 检测 MD 中的 DSL 代码块，渲染为图表。

**支持两种 DSL**：
- ` ```mermaid ` → mermaid.js 渲染（覆盖 10 种结构图）
- ` ```graphviz ` 或 ` ```dot ` → @viz-js/viz（WASM）渲染（覆盖 architecture、swimlane）

**渲染方案**：CDN 直接渲染，通过 CSS 主题配置尽量好看。
**不要求**与 diagram skill PNG 视觉一致（后续迭代可做）。

**实现要点**：
1. preview-md.mjs 的 `renderMarkdown` 后处理中检测 `language-mermaid` / `language-dot` 代码块
2. 引入 mermaid.js CDN + @viz-js/viz CDN
3. 将代码块内容交给对应渲染引擎渲染为 SVG
4. 用 `.chart-container` 包裹，和报告中的图表容器风格统一
5. 配置 mermaid 主题（使用共享 CSS 变量中的配色）

## 需求三（远期）：风格统一

preview-md 中 Mermaid 渲染的视觉效果与 diagram skill PNG 输出一致。
需要写 Mermaid DSL → diagram 模板 JSON 的解析器。
**本期不做**，仅记录方向。

## 实施顺序

1. 需求二先做（preview-md 渲染 mermaid 块）— 下游先通
2. 需求一后做（diagram skill 输出 Mermaid）— 上游供给
3. 需求三远期（风格统一）— 按需迭代

先通渲染再通输出，这样可以立刻手写 mermaid 代码块测试渲染效果。

## 需求四（待定）：SWOT / 鱼骨图 / 文氏图加入 bridge.py

这 3 种图表的视觉形态特殊（四象限、骨架、圆形交叠），DSL 无法表达，目前只能走 HTML 模板 → PNG。
考虑加入 bridge.py 统一管道，实现 JSON → HTML/PNG 的标准化输出，和统计图走同一链路。

| 图表 | 数据结构 | 复杂度 |
|------|---------|-------|
| SWOT | 4 个列表（优势/劣势/机会/威胁） | 低 |
| 鱼骨图 | 主骨 + 分支列表 | 中 |
| 文氏图 | 2-4 个集合 + 交集描述 | 中 |

**本期不做**，按需迭代。
