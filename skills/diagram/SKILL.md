---
name: diagram
description: >
  专业图表生成技能：根据需求自动选择合适的图表类型，生成符合设计规范的 PNG 图表。
  覆盖结构图（流程图、泳道图、时序图、架构图、状态图、ER图、类图、思维导图、甘特图等）
  和统计图（柱状图、折线图、饼图、雷达图、热力图、桑基图等）。
  统一工具：HTML/SVG + 内联 JS 布局计算。ER/类图使用 ELKjs 布局引擎。
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
3. **用什么布局** — 根据图表类型选择布局策略

### 图表类型速查

| 要展示什么 | 图表类型 | 布局策略 | 专属规范 |
|-----------|---------|---------|---------|
| 工作流程、决策逻辑 | 流程图 | 手动布局 | `references/diagrams/flowchart.md` |
| 多角色协作流程 | 泳道图 | 手动网格 | `references/diagrams/swimlane.md` |
| API 调用、消息交互 | 时序图 | 自定义顺序堆叠 | `references/diagrams/sequence.md` |
| 系统分层、技术栈 | 架构图 | 手动层堆叠 | `references/diagrams/architecture.md` |
| 数据库表结构 | ER 图 | **ELKjs** | `references/diagrams/er.md` |
| 面向对象设计 | 类图 | **ELKjs** | `references/diagrams/class.md` |
| 状态迁移 | 状态图 | ELKjs | `references/diagrams/state.md` |
| 网络拓扑 | 网络图 | 手动分层 | `references/diagrams/network.md` |
| 选型决策 | 决策树 | 树形布局 | `references/diagrams/decision-tree.md` |
| 数据管道 | 数据流图 | 手动分层 | `references/diagrams/dataflow.md` |
| C4 系统视图 | C4 图 | 手动分层 | `references/diagrams/c4.md` |
| 知识结构 | 思维导图 | 双侧树形 | `references/diagrams/mindmap.md` |
| 项目排期 | 甘特图 | 日期轴网格 | `references/diagrams/gantt.md` |
| 发展历程 | 时间线 | 纵向列表 | `references/diagrams/timeline.md` |
| 组织架构 | 组织结构图 | 树形 | `references/diagrams/orgchart.md` |
| 优劣势分析 | SWOT 图 | 卡片四象限 | `references/diagrams/swot.md` |
| 根因分析 | 鱼骨图 | 鱼骨骨架 | `references/diagrams/fishbone.md` |
| 集合关系 | 文氏图 | 圆形交叠 | `references/diagrams/venn.md` |
| 用户体验 | 旅程图 | 卡片横向 | `references/diagrams/journey.md` |
| 离散对比 | 柱状图 | 笛卡尔坐标 | `references/diagrams/bar-chart.md` |
| 趋势变化 | 折线图 | 笛卡尔坐标 | `references/diagrams/line-chart.md` |
| 占比构成 | 饼图 | 径向 | `references/diagrams/pie-chart.md` |
| 多维评估 | 雷达图 | 径向 | `references/diagrams/radar-chart.md` |
| 矩阵数据 | 热力图 | 网格 | `references/diagrams/heatmap.md` |
| 流量路径 | 桑基图 | 流带分层 | `references/diagrams/sankey.md` |
| 分布关系 | 散点图 | 笛卡尔坐标 | `references/diagrams/scatter.md` |

---

## 第二步：读取规范，生成图表

### 2.1 规范体系

- **公共规范** `references/design-system.md` — 配色、字体、组件、间距
- **公共工具** `references/diagram-utils.md` — SVG 工具函数、文字测量、碰撞检测
- **专属规范** `references/diagrams/<type>.md` — 每种图表的数据结构、布局规则、渲染细节

### 2.2 布局策略

图表布局分两种：

**ELKjs 自动布局**（ER图、类图、状态图）：
- 引用 `lib/elk.bundled.js`
- 定义 ELK 图结构（nodes + edges）
- `elk.layout(graph).then(result => { /* 渲染 */ })`
- 注意：ELKjs 是异步的，所有渲染代码放在 `.then()` 回调里

**手动布局**（流程图、泳道图、架构图、时序图等）：
- 根据图表类型的领域规则计算坐标
- 流程图：主路径向下，"否"分支向右
- 泳道图：列 × 行网格，泳道固定行序
- 架构图：预定义层级从上到下堆叠
- 时序图：参与者横排等距，消息纵向堆叠

### 2.3 生成流程

```
1. 读取专属规范 → 了解数据结构和布局规则
2. 定义数据（nodes/edges/steps/tables 等）
3. 计算布局坐标（ELKjs 或手动）
4. 渲染 SVG（节点 → 连线 → 标签，按层级顺序）
5. 写入 HTML 文件（含内联 JS + CSS）
6. 启动 HTTP 服务 → Playwright 截图 → PNG
```

### 2.4 HTML 模板结构

所有模板遵循统一结构：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, system-ui, 'PingFang SC', sans-serif;
    background: #ffffff;
    padding: 24px;
    display: inline-block;  /* 关键：画布收缩包裹内容 */
  }
</style>
<!-- ELKjs 仅在 ER/类图/状态图中引入 -->
<script src="lib/elk.bundled.js"></script>
</head>
<body>
<svg id="canvas"></svg>
<script>
(function() {
  // 1. 数据定义（title, subtitle, nodes, edges 等）
  // 2. 主题定义（colors, fonts, spacing）
  // 3. 工具函数（el, measureText）
  // 4. 布局计算（ELKjs 或手动）
  // 5. 渲染（背景层 → 连线层 → 节点层 → 标签层）
})();
</script>
</body>
</html>
```

### 2.5 标题规范

- 位置：左上角（x=0, y=18）
- 标题：16px bold，颜色 `#1a1a2e`
- 副标题：12px，颜色 `#888888`，y=36
- 标题区高度：52px

---

## 第三步：输出规范

### 3.1 文件格式
- 格式：PNG
- 背景：白色 `#FFFFFF`
- 四周 padding：至少 24px
- 缩放：原生设备 DPI（Retina 设备自动输出 2x 清晰图）

### 3.2 截图方式

**必须使用 `browser_run_code` + body 元素截图**，不要用 `browser_take_screenshot`（它强制 `scale: 'css'` 导致 1x 模糊输出）。

```javascript
async (page) => {
  await page.locator('body').screenshot({
    path: '<输出路径>.png',
    type: 'png'
  });
}
```

### 3.3 文件命名
`<图表类型>-<描述>.png`（英文小写 + 连字符）

### 3.4 存放位置
- 默认：与调用方的 Markdown 文件同级的 `assets/` 或 `images/` 目录
- deep-research 调用时：`docs/research/assets/`

---

## 工具依赖

| 工具 | 安装方式 | 用途 |
|------|---------|------|
| Playwright | MCP 插件（已集成） | HTML → PNG 截图 |
| ELKjs | `lib/elk.bundled.js`（已内联） | ER图/类图/状态图的自动布局 |

### ELKjs 使用说明

ELKjs 仅用于**自由图布局**（节点和边的位置需要算法优化的场景）。以下图表类型**不用 ELKjs**：
- 流程图（领域规则：主路径向下，否分支向右）
- 泳道图（领域规则：泳道固定行序）
- 架构图（领域规则：层级预定义）
- 时序图（领域规则：参与者横排，消息纵向）

原因：这些图表有明确的领域布局规则，ELKjs 的自动优化会打破这些规则（比如重排泳道顺序、改变分组位置）。
