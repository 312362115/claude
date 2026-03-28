---
name: diagram
description: >
  专业图表生成技能：根据需求自动选择合适的图表类型和工具，生成符合设计规范的 PNG 图表。
  覆盖结构图（流程图、泳道图、时序图、架构图、状态图、ER图、类图、思维导图、甘特图等）
  和统计图（柱状图、折线图、饼图、雷达图、热力图、桑基图等）。
  统一工具：HTML/SVG（全部图表类型）。纯 HTML+CSS+SVG 实现，内联 JS 仅做布局计算，无外部依赖。
  所有图表遵循统一的设计规范（配色/字体/组件/间距），风格现代简洁。
  触发词：画图、画一个、生成图表、流程图、架构图、时序图、柱状图、对比图、关系图。
  即使用户没有说"画图"，只要需求中涉及可视化展示（流程、架构、数据对比、关系），都应触发此技能。
  被 deep-research 等其他技能调用时，同样遵循本规范生成图表。
---

# 画图技能（Diagram Skill）

> 用自然语言描述需求，自动生成专业的 PNG 图表，直接嵌入 Markdown 文档。

---

## 第一步：理解需求，选择图表类型

收到画图需求后，判断：
1. **画什么** — 需要展示的信息类型（流程？架构？数据对比？关系？）
2. **哪种图表** — 根据信息类型匹配最合适的图表
3. **用什么工具** — 根据图表类型选择工具

### 图表类型速查

| 要展示什么 | 图表类型 | 工具 | 专属规范 |
|-----------|---------|------|---------|
| 工作流程、决策逻辑 | 流程图 | HTML/SVG | `references/diagrams/flowchart.md` |
| 多角色协作流程 | 泳道图 | HTML/SVG | `references/diagrams/swimlane.md` |
| API 调用、消息交互 | 时序图 | HTML/SVG | `references/diagrams/sequence.md` |
| 系统分层、技术栈 | 架构图 | HTML/SVG | `references/diagrams/architecture.md` |
| 状态迁移 | 状态图 | HTML/SVG | `references/diagrams/state.md` |
| 数据库表结构 | ER 图 | HTML/SVG | `references/diagrams/er.md` |
| 面向对象设计 | 类图 | HTML/SVG | `references/diagrams/class.md` |
| 网络拓扑 | 网络图 | HTML/SVG | `references/diagrams/network.md` |
| 选型决策 | 决策树 | HTML/SVG | `references/diagrams/decision-tree.md` |
| 数据管道 | 数据流图 | HTML/SVG | `references/diagrams/dataflow.md` |
| C4 系统视图 | C4 图 | HTML/SVG | `references/diagrams/c4.md` |
| 知识结构 | 思维导图 | HTML/SVG | `references/diagrams/mindmap.md` |
| 项目排期 | 甘特图 | HTML/SVG | `references/diagrams/gantt.md` |
| 发展历程 | 时间线 | HTML/SVG | `references/diagrams/timeline.md` |
| 组织架构 | 组织结构图 | HTML/SVG | `references/diagrams/orgchart.md` |
| 优劣势分析 | SWOT 图 | HTML/SVG | `references/diagrams/swot.md` |
| 根因分析 | 鱼骨图 | HTML/SVG | `references/diagrams/fishbone.md` |
| 集合关系 | 文氏图 | HTML/SVG | `references/diagrams/venn.md` |
| 用户体验 | 旅程图 | HTML/SVG | `references/diagrams/journey.md` |
| 离散对比 | 柱状图 | HTML/SVG | `references/diagrams/bar-chart.md` |
| 趋势变化 | 折线图 | HTML/SVG | `references/diagrams/line-chart.md` |
| 占比构成 | 饼图 | HTML/SVG | `references/diagrams/pie-chart.md` |
| 多维评估 | 雷达图 | HTML/SVG | `references/diagrams/radar-chart.md` |
| 矩阵数据 | 热力图 | HTML/SVG | `references/diagrams/heatmap.md` |
| 流量路径 | 桑基图 | HTML/SVG | `references/diagrams/sankey.md` |
| 分布关系 | 散点图 | HTML/SVG | `references/diagrams/scatter.md` |

确定图表类型后，**读取对应的专属规范文件**，按规范生成图表。

---

## 第二步：读取规范，生成图表

### 2.1 公共规范

所有图表共享一套设计规范，定义在 `references/design-system.md`：
- 调色板（基础色 / 主题色 / 语义色 / 层级色）
- 字体（字体栈 / 字号层级）
- 基础组件（节点类型 / 连线类型 / 容器类型）
- 排版间距（间距网格 / 节点间距 / 容器间距 / 图表整体间距）
- 流向选择（纵向 vs 横向的判断规则）

### 2.2 专属规范

每种图表有自己的专属规范文件（`references/diagrams/<type>.md`），定义：
- 该图表使用哪些组件、怎么用
- 布局规则（流向、对齐、间距的特殊调整）
- 示例模板路径
- 禁忌（什么不能做）

### 2.3 生成流程

```
1. 读取专属规范 → 了解该图表的规则和模板
2. 基于模板生成源文件（.d2 / .mmd / .html）
3. 渲染为 PNG：用 `browser_run_code` 截图（fullPage, 原生 DPI）→ output.png
4. 输出到指定目录
```

---

## 第三步：输出规范

### 3.1 文件格式
- 格式：PNG
- 背景：白色 `#FFFFFF`
- 四周 padding：至少 24px
- 缩放：原生设备 DPI（Retina 设备自动输出 2x 清晰图）

### 3.2 截图方式

**必须使用 `browser_run_code` + body 元素截图**，不要用 `browser_take_screenshot`（它强制 `scale: 'css'` 且按视口宽度截图，导致 1x 模糊 + 大片空白）。

```javascript
// 正确的截图方式：body 元素截图
async (page) => {
  await page.locator('body').screenshot({
    path: '<输出路径>.png',
    type: 'png'
  });
}
```

> **为什么用 body 元素截图**：
> - 自动裁切到内容区域，无多余空白
> - 默认 `scale: 'device'`，Retina 设备输出 2x 清晰图
> - 模板 CSS 设置 `body { display: inline-block }` 确保 body 收缩包裹 SVG 内容

### 3.3 文件命名
`<图表类型>-<描述>.png`（英文小写 + 连字符）

### 3.4 存放位置
- 默认：与调用方的 Markdown 文件同级的 `assets/` 或 `images/` 目录
- deep-research 调用时：`docs/research/assets/`

---

## 工具依赖

| 工具 | 安装方式 | 用途 |
|------|---------|------|
| Playwright | MCP 插件（已集成） | HTML/SVG → PNG 截图（用 `browser_run_code` 截图） |

首次使用时检测依赖是否已安装，未安装则提示安装命令。
