---
name: diagram
version: 1.4.0
last_updated: 2026-04-01
repository: https://github.com/312362115/claude
changelog: skills/diagram/CHANGELOG.md
description: >
  专业图表生成技能：根据需求自动选择合适的图表类型，生成符合设计规范的 PNG 图表。
  覆盖 29 种图表：结构图（流程图、泳道图、时序图、架构图、状态图、ER图、类图、思维导图、甘特图、Kanban、Git Graph 等）
  和统计图（柱状图、折线图、饼图、雷达图、热力图、散点图、桑基图、漏斗图、瀑布图、矩形树图、柱线混合图等）。
  统一工具：HTML/SVG + 内联 JS 布局计算。ER/类图使用 ELKjs 布局引擎。
  所有图表遵循统一的设计规范（配色/字体/组件/间距），风格现代简洁。
  支持三种输出：PNG（默认）、HTML（富文档嵌入）、DSL（Mermaid 文本，嵌入 MD 文档）。
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

### Mermaid / Graphviz 标记语言转换

当发现 Markdown 中有 ` ```mermaid ` 或 ` ```dot ` 代码块时：

1. **解读**图结构（节点、边、标签、类型、分组等）
2. **映射**到对应的图表类型模板数据结构
3. **渲染**为设计规范统一的 PNG
4. **替换**原始文本块为图片引用

映射规则：

| 源格式 | 关键字/语法 | 映射目标 |
|--------|-----------|---------|
| Mermaid `graph TD` / `flowchart` | 节点 + 箭头 | flowchart 模板 |
| Mermaid `sequenceDiagram` | 参与者 + 消息 | sequence 模板 |
| Mermaid `classDiagram` | 类 + 关系 | class 模板 |
| Mermaid `stateDiagram` | 状态 + 转换 | state 模板 |
| Mermaid `erDiagram` | 实体 + 关系 | er 模板 |
| Mermaid `gantt` | 任务 + 日期 | gantt 模板 |
| Mermaid `pie` | 标签 + 数值 | pie 模板 |
| Mermaid `journey` | 阶段 + 评分 | journey 模板 |
| DOT `digraph` | 有向图 | flowchart / state / class（按结构判断） |
| DOT `graph` | 无向图 | er / network（按结构判断） |

> **注意**：不是调用 Mermaid/Graphviz 工具渲染，而是 Claude 理解标记语言描述的图结构，转成我们的模板数据，用统一设计规范渲染。这样所有图表风格一致。

### 图表类型速查

| 要展示什么 | 图表类型 | 布局策略 | 专属规范 |
|-----------|---------|---------|---------|
| 工作流程、决策逻辑（单路径） | 流程图（线性） | 手动布局 | `references/diagrams/flowchart.md` |
| 多源汇聚、资源流转、关系图 | 流程图（DAG） | **ELKjs** | `references/diagrams/flowchart.md` |
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
| 数据占比/层级面积 | 矩形树图 | Squarified | `references/diagrams/treemap.md` |
| 柱状+折线混合 | 柱线混合图 | 笛卡尔双 Y 轴 | `references/diagrams/combo.md` |
| 项目管理/任务看板 | Kanban | 竖列卡片 | `references/diagrams/kanban.md` |
| Git 分支工作流 | Git Graph | 横向分支线 | `references/diagrams/git-graph.md` |

---

## 第二步：读取规范，生成图表

### 2.1 规范体系

- **公共规范** `references/design-system.md` — 配色、字体、组件、间距
- **公共工具** `references/diagram-utils.md` — SVG 工具函数、文字测量、碰撞检测
- **专属规范** `references/diagrams/<type>.md` — 每种图表的数据结构、布局规则、渲染细节

### 2.2 布局策略

图表布局分两种：

**ELKjs 自动布局**（ER图、类图、状态图、流程图 DAG 模式）：
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
6. 用 capture.py 截图 → PNG（禁止手动调用 Playwright）
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

- **标题可选**：`title` 为空字符串或 `null` 时跳过标题渲染，标题区高度设为 0
- 有标题时：位置左上角（x=0, y=18），16px bold，颜色 `#1a1a2e`
- 副标题：12px，颜色 `#888888`，y=36
- 标题区高度：有标题 52px，无标题 0px

```javascript
// 标题可选的标准写法
var TITLE_AREA_H = title ? 52 : 0;

// 渲染时条件判断
if (title) {
  nodeGroup.appendChild(el('text', { ... })).textContent = title;
  if (subtitle) nodeGroup.appendChild(el('text', { ... })).textContent = subtitle;
}
```

---

## 第三步：输出规范

### 3.1 文件格式

**PNG（默认）** — 用于 Markdown 文档配图：
- 背景：白色 `#FFFFFF`
- 四周 padding：至少 24px
- 缩放：原生设备 DPI（Retina 设备自动输出 2x 清晰图）

**HTML（可选）** — 用于富文档嵌入、交互式展示：
- 自包含：所有 CSS/JS 内联，无外部依赖，单文件可直接浏览器打开
- 矢量：SVG 无损缩放，文字可选中/搜索
- 适用场景：嵌入 HTML 报告、做交互式架构文档、需要二次编辑的图表
- 生成方式：`python scripts/capture.py input.html -f html`

**DSL（可选）** — 用于嵌入 Markdown 文档，文本可 diff、可版本控制：
- 结构图 + 部分统计图支持 Mermaid DSL 输出
- 输出为 Mermaid 语法的纯文本
- 适用场景：MD 文档配图不想维护 PNG 文件、需要 preview-md 实时渲染、GitHub/GitLab 原生渲染
- 生成方式：直接输出文本，用户复制到 MD 文件的代码块中

DSL 选择规则：

| 图表类型 | DSL | 代码块标记 |
|---------|-----|----------|
| flowchart / sequence / class / state / er | Mermaid | ` ```mermaid ` |
| gantt / mindmap / timeline / c4 / sankey / journey | Mermaid | ` ```mermaid ` |
| architecture / swimlane / network / dataflow / orgchart / decision-tree | Mermaid（flowchart + subgraph） | ` ```mermaid ` |
| bar / line（柱状图、折线图） | Mermaid（xychart-beta） | ` ```mermaid ` |
| pie（饼图） | Mermaid | ` ```mermaid ` |
| radar / heatmap / scatter / funnel / waterfall 等 | **不支持 DSL** | 继续用 PNG |
| quadrant / gitGraph / block | **暂不支持** | 后续按需开放 |

DSL 输出格式示例：

```
用户：画一个用户登录的流程图，输出 mermaid

输出：
` ` `mermaid
flowchart TD
    A[用户访问登录页] --> B{已有账号?}
    B -->|是| C[输入用户名密码]
    B -->|否| D[跳转注册页]
    C --> E{验证通过?}
    E -->|是| F[跳转首页]
    E -->|否| G[提示错误]
    G --> C
` ` `
```

```
用户：画一个微服务架构图，输出 mermaid

输出：
` ` `mermaid
flowchart TD
    subgraph 网关层
        nginx[Nginx 负载均衡] --> api_gw[API Gateway]
    end
    subgraph 服务层
        user_svc[用户服务]
        order_svc[订单服务]
        pay_svc[支付服务]
    end
    subgraph 数据层
        mysql[(MySQL)]
        redis[(Redis)]
    end
    api_gw --> user_svc & order_svc & pay_svc
    user_svc --> mysql
    order_svc --> mysql
    pay_svc --> redis
` ` `
```

### 3.2 截图方式

**必须使用固化脚本，禁止手动调用 Playwright MCP 工具截图。**

```bash
# 结构图：HTML → PNG
python ~/.claude/skills/diagram/scripts/capture.py <HTML文件> <输出路径>.png

# 结构图：HTML → 自包含 HTML
python ~/.claude/skills/diagram/scripts/capture.py <HTML文件> <输出路径>.html -f html

# 统计图：JSON → PNG（bridge.py 内部自动截图）
python ~/.claude/skills/diagram/scripts/bridge.py -c <配置>.json -o <输出路径>.png

# 统计图：JSON → 自包含 HTML
python ~/.claude/skills/diagram/scripts/bridge.py -c <配置>.json -o <输出路径>.html -f html
```

> **为什么不能手动截图？** capture.py / bridge.py 已封装好 HTTP 服务启动、ELKjs 异步等待、Retina 2x 输出、body 元素定位等逻辑。手动用 `browser_run_code` / `browser_take_screenshot` 容易遗漏等待逻辑导致截图空白或模糊。

### 3.3 文件命名
`<图表类型>-<描述>.png`（英文小写 + 连字符）

### 3.4 存放位置
- 默认：与调用方的 Markdown 文件同级的 `assets/` 或 `images/` 目录
- deep-research 调用时：`docs/research/assets/`

---

## 工具依赖

| 工具 | 位置 | 用途 |
|------|------|------|
| `capture.py` | `scripts/capture.py` | 结构图 HTML → PNG/HTML（内部调用 Playwright） |
| `bridge.py` | `scripts/bridge.py` | 统计图 JSON → PNG/HTML（内部调用 Playwright） |
| ELKjs | `lib/elk.bundled.js`（已内联） | ER图/类图/状态图/流程图DAG的自动布局 |

> **Playwright 仅作为 capture.py / bridge.py 的内部实现**，不要直接调用 Playwright MCP 工具（`browser_navigate`、`browser_take_screenshot`、`browser_run_code` 等）来截图。

### ELKjs 使用说明

ELKjs 仅用于**自由图布局**（节点和边的位置需要算法优化的场景）。以下图表类型**不用 ELKjs**：
- 流程图 **线性模式**（领域规则：主路径向下，否分支向右）
- 泳道图（领域规则：泳道固定行序）
- 架构图（领域规则：层级预定义）
- 时序图（领域规则：参与者横排，消息纵向）

原因：这些图表有明确的领域布局规则，ELKjs 的自动优化会打破这些规则（比如重排泳道顺序、改变分组位置）。

**例外**：流程图的 **DAG 模式**（多根节点、汇聚、非决策分支）使用 ELKjs，因为此类拓扑无法用简单的"主路径+侧分支"手动布局。详见 `references/diagrams/flowchart.md`。

### 流程图 DAG 模式注意事项

- **忠实还原拓扑**：不存在的连线绝不添加，多个独立入口不能强行归到同一根节点
- **节点类型忠实原图**：同层级/同角色的节点用相同 type。`highlight` 仅用于原图明确标注为关键/核心的节点，不要用它来区分"不同类别"——类别差异用 `process`/`external`/`datastore` 等语义类型表达

---

## 更新检查

任务完成后，检查本 skill 是否有新版本。规则：

1. **频率控制（每天一次）**：用 Read 读取 `~/.claude/.skill-check-diagram`。如果文件内容是今天的日期（YYYY-MM-DD），跳过后续所有步骤。如果文件不存在或日期不是今天，继续
2. **读取本地版本**：从本文件 frontmatter 的 `version` 字段获取
3. **获取远端版本**：用 WebFetch 请求 `https://raw.githubusercontent.com/312362115/claude/main/skills/diagram/VERSION`（仅含版本号）
4. **写入检查标记**：用 Bash 执行 `echo "$(date +%Y-%m-%d)" > ~/.claude/.skill-check-diagram`
5. **比对与更新**：版本相同则静默跳过。版本不同则告知用户并询问是否更新：
   ```
   diagram skill 有新版本可用：<本地版本> → <远端版本>
   查看更新内容：https://github.com/312362115/claude/blob/main/skills/diagram/CHANGELOG.md
   是否立即更新？
   ```
   用户确认后，依次 WebFetch 以下文件并覆盖本地对应文件：
   - `https://raw.githubusercontent.com/312362115/claude/main/skills/diagram/SKILL.md`
   - `https://raw.githubusercontent.com/312362115/claude/main/skills/diagram/VERSION`
   - `https://raw.githubusercontent.com/312362115/claude/main/skills/diagram/CHANGELOG.md`
   更新完成后提示用户重新加载 skill（开始新会话或 `/reload-plugins`）
6. **容错**：任何步骤失败时静默跳过，不报错不打扰用户
