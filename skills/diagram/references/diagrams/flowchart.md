# 流程图规范（Flowchart）

> 双轨制：日常用 Mermaid 快速出图，正式文档用 HTML/SVG 精确控制。

---

## 适用场景

- 工作流程（订单处理、用户注册、审批流程）
- 决策逻辑（条件分支、异常处理）
- 数据处理流程（ETL、请求处理管道）

---

## 模式选择

| 场景 | 模式 | 工具 | 模板 |
|------|------|------|------|
| 日常画图、快速出图、非正式场景 | 快速模式 | Mermaid | `templates/mermaid/flowchart.mmd` |
| 调研报告、方案文档、正式展示 | 精品模式 | HTML/SVG | `templates/html/flowchart.html` |

判断依据：调用方是 deep-research 或用户明确要求高质量 → 精品模式，其余 → 快速模式。

---

## 组件使用规则

| 元素 | 节点类型 | type 值 | Mermaid 语法 | 色系 |
|------|---------|---------|-------------|------|
| 流程起点 | Terminal Start | `start` | `([文字])` | 绿色 Emerald |
| 处理步骤 | Process | `process` | `[文字]` | 蓝色 Blue |
| 判断/条件 | Decision | `decision` | `{文字}` | 黄色 Amber |
| 数据库操作 | Data Store | `datastore` | `[(文字)]` | 紫色 Violet |
| 关键步骤 | Highlight | `highlight` | `[文字]` | 蓝色实心白字 |
| 错误终点 | Error | `error` | `[文字]` | 红色 Rose |
| 成功终点 | Success | `success` | `[文字]` | 绿色 Emerald |
| 流程终点 | Terminal End | `end` | `([文字])` | 灰色 |
| **I/O 操作** | Parallelogram | `io` | `[/文字/]` | 蓝色 Blue |
| **文档** | Document | `document` | `[文字]` | 蓝色 Blue |
| **终态/子流程** | Double Circle | `double-circle` | `(((文字)))` | 绿色 Emerald |
| **手动操作** | Trapezoid | `trapezoid` | `[/文字\]` | 青色 Cyan |
| **事件/信号** | Flag | `flag` | `>文字]` | 橙色 Orange |

---

## 布局规则

1. **流向**：默认从上到下（`TD`）
2. **主路径**：保持直线向下
3. **判断分支**："是/通过"向下，"否/失败"向右
4. **回退/重试**：用虚线 `-.->` 表示
5. **子流程**：用 `subgraph` 包裹
6. **节点数上限**：15 个（超过拆子流程）

---

## 快速模式（Mermaid）

### classDef 样式表

每张 Mermaid 流程图必须包含以下 classDef（对应设计规范色值）：

```
classDef termStart fill:#ECFDF5,stroke:#6EE7B7,stroke-width:1.5px,color:#065F46
classDef termEnd fill:#F1F5F9,stroke:#CBD5E1,stroke-width:1.5px,color:#64748B
classDef process fill:#EFF6FF,stroke:#93C5FD,stroke-width:1.5px,color:#1E293B
classDef decision fill:#FFFBEB,stroke:#FCD34D,stroke-width:1.5px,color:#92400E
classDef highlight fill:#3B82F6,stroke:#3B82F6,stroke-width:1.5px,color:#FFFFFF
classDef success fill:#ECFDF5,stroke:#6EE7B7,stroke-width:1.5px,color:#065F46
classDef error fill:#FFF1F2,stroke:#FDA4AF,stroke-width:1.5px,color:#9F1239
classDef datastore fill:#F5F3FF,stroke:#C4B5FD,stroke-width:1.5px,color:#5B21B6
```

### init 主题配置

```
%%{init: {'theme':'base','themeVariables':{
  'primaryColor':'#EFF6FF','primaryBorderColor':'#93C5FD','primaryTextColor':'#1E293B',
  'lineColor':'#94A3B8','textColor':'#1E293B','fontSize':'13px',
  'fontFamily':'PingFang SC, Inter, sans-serif',
  'edgeLabelBackground':'#FFFFFF'
}}}%%
```

### 生成命令

```bash
mmdc -i input.mmd -o output.png -b white -s 2
```

---

## 精品模式（HTML/SVG + JS 动态布局）

使用内联 JS 动态计算节点坐标，支持任意数量的步骤和判断分支。

### 模式选择：线性模式 vs DAG 模式

流程图有两种数据结构模式，根据图的拓扑结构选择：

| 特征 | 线性模式（steps） | DAG 模式（nodes + edges） |
|------|-----------------|------------------------|
| 入口节点 | 单个起点 | **多个独立起点** |
| 路径结构 | 一条主路径 + 决策侧分支 | 任意有向无环图 |
| 汇聚 | 不支持（一个节点只有一个父节点） | **支持多入边汇聚** |
| 布局引擎 | 手动布局（主路径向下，否分支向右） | **ELKjs 自动布局** |
| 适用场景 | 审批流、处理流程、决策链 | 关系图、资源流转、多源汇聚 |

**判断规则**：
1. 是否有 **多个独立入口**（多个节点没有入边）？→ DAG 模式
2. 是否有 **汇聚**（一个节点接收多条入边）？→ DAG 模式
3. 是否有 **非决策分支**（普通节点分出多条路径）？→ DAG 模式
4. 以上都不是 → 线性模式

> **核心原则：忠实还原原图拓扑。** 不存在的连线绝不添加，多个独立入口不能强行归到同一个根节点。

### 数据结构（线性模式）

```javascript
// 标题
var title = '订单处理流程';
var subtitle = 'Order Processing Workflow';

// 主路径步骤（按顺序排列，自顶向下渲染）
// type: 'start' | 'process' | 'decision' | 'highlight' | 'error' | 'success' | 'datastore' | 'external' | 'end'
// decision 节点的 no 字段指定"否"分支目标 id
var steps = [
  { id: 'start', label: '用户提交订单', type: 'start' },
  { id: 's1', label: '订单参数校验', type: 'process' },
  { id: 'd1', label: '参数合法?', type: 'decision', no: 'e1' },
  { id: 's2', label: '库存检查', type: 'process' },
  { id: 's3', label: '创建订单记录', type: 'highlight' },
  { id: 'end', label: '订单完成', type: 'end' }
];

// 侧分支节点（decision 的"否"路径目标，放在主路径右侧）
// 支持 next 数组实现子流程（多步骤链）
var sideNodes = [
  { id: 'e1', label: '返回参数错误', type: 'error' },
  { id: 'e2', label: '释放锁定库存', type: 'process',
    next: [
      { label: '订单标记支付失败', type: 'error' },
      { label: '发送支付失败通知', type: 'process' }
    ]
  }
];
```

### 分组模式（subgraph）

支持将步骤按模块/服务分组，每组用不同背景色区分，组间自动串联：

```javascript
// 分组模式：定义 groups 数组，每组含 label 和 steps
// groups 为 null 则走简单模式（直接使用 steps）
var groups = [
  { label: '用户端', steps: [
    { id: 'start', label: '用户提交订单', type: 'start' },
    { id: 's1', label: '表单校验', type: 'process' },
  ]},
  { label: '后端处理', steps: [
    { id: 's2', label: '风控检查', type: 'process' },
    { id: 'd1', label: '通过?', type: 'decision', no: 'e1' },
  ]},
];
var steps = null;  // 分组模式时设为 null
```

分组背景使用 `theme.layers` 配色（6 色循环），每组一个圆角矩形 + 左上角标签。

### 数据结构（DAG 模式）

当流程图有多个独立入口、汇聚节点或非决策分支时，使用 `nodes` + `edges` 数据结构 + ELKjs 自动布局：

```javascript
// 标题
var title = '多渠道获客转化';
var subtitle = 'Multi-channel Acquisition Funnel';

// DAG 模式标志
var dagMode = true;

// 节点列表（无需关心顺序，ELKjs 自动排列）
// type: 'start' | 'process' | 'decision' | 'highlight' | 'error' | 'success' | 'datastore' | 'external' | 'end'
var nodes = [
  { id: 'sem', label: 'SEM 投放', type: 'start' },
  { id: 'seo', label: 'SEO 自然流量', type: 'start' },
  { id: 'ref', label: '老客推荐', type: 'start' },
  { id: 'land', label: '落地页', type: 'process' },
  { id: 'reg', label: '注册转化', type: 'process' },
  { id: 'trial', label: '试用体验', type: 'process' },
  { id: 'pay', label: '付费转化', type: 'success' },
  { id: 'crm', label: 'CRM 客户池', type: 'datastore' },
  { id: 'churn', label: '流失召回', type: 'external' },
];

// 边列表（from → to，可选标签）
var edges = [
  { from: 'sem', to: 'land', label: '广告点击' },
  { from: 'seo', to: 'land', label: '搜索进入' },
  { from: 'ref', to: 'reg', label: '邀请码' },
  { from: 'land', to: 'reg' },
  { from: 'reg', to: 'trial' },
  { from: 'trial', to: 'pay', label: '转化' },
  { from: 'trial', to: 'churn', label: '流失' },
  { from: 'pay', to: 'crm' },
  { from: 'churn', to: 'reg', label: '召回' },
];

// 线性模式变量设为 null
var steps = null;
var groups = null;
var sideNodes = [];
```

**DAG 模式关键规则**：
- `nodes` 数组定义所有节点，无需考虑排列顺序
- `edges` 数组定义所有连线，每条边有 `from`、`to`、可选 `label`
- 不存在的连线**绝不添加**，严格按原图拓扑
- 多个节点可以没有入边（多根节点），多个节点可以没有出边（多终点）
- **节点类型忠实原图**：同层级/同角色的节点使用相同 type。`highlight` 仅用于原图明确标注为关键/核心的节点，不要用 `highlight` 来区分"不同类别"——类别差异用 `process`/`external`/`datastore` 等语义类型表达
- 使用 ELKjs 自动布局，流向默认从上到下（`elk.direction: 'DOWN'`）
- 引入 `lib/elk.bundled.js`

### 布局算法（线性模式）

- **主路径**：所有非决策矩形节点统一宽度（取最大值），自顶向下排列
- **决策节点**：菱形，宽高根据文字动态计算
- **侧分支**：与对应 decision 的下一步同行，x 基于**主路径矩形右边缘**（非菱形）+ 60px 间距
- **侧子流程**：`next` 数组中的节点依次向下排列，间距 28px，所有侧节点统一宽度
- **分组背景**：包裹组内所有节点，顶部 36px（含标签）、底部 20px、左右 32px padding
- **组间间距**：32px
- **间距**：步骤间 36px，含判断时 48px
- **画布自适应**：根据节点实际位置计算，最小宽度 1000px
- **连线**：主路径直线，决策后绿色；"否"路径折线（Q 圆角），红色；子流程连线红色 1.5px
- **渲染顺序**：分组背景层 → 连线层 → 节点层

### 布局算法（DAG 模式）

- **引擎**：ELKjs（`lib/elk.bundled.js`），所有渲染代码在 `.then()` 回调中
- **流向**：`'elk.direction': 'DOWN'`（从上到下）
- **间距**：`'elk.spacing.nodeNode': '80'`，`'elk.layered.spacing.nodeNodeBetweenLayers': '80'`，`'elk.spacing.edgeNode': '40'`
- **节点尺寸**：矩形统一宽度（取最大值），高度 40px，terminal 36px
- **连线**：正交路由 + 10px 圆角 Q 贝塞尔转折（与设计规范一致），边标签放在路径中点
- **画布**：根据 ELK 返回的布局尺寸自适应
- **渲染顺序**：连线层 → 节点层 → 标签层

### "是/否"标签定位规则（仅线性模式）

标签必须放在连线旁边，**禁止压在连线上或与节点重叠**：

- **"是"标签**：放在主路径竖线的**左侧**（`cx - 18`），紧贴 decision 节点下方（`bottom + 18` 或 `30%` 处取较小值）
- **"否"标签**：放在水平线**上方**（`dy - 14`），靠近 decision 出口右侧（`right + 24`）
- **白底衬底**：标签底层有白色圆角矩形，宽度 = 文字宽度 + 8px，高度 16px
- **防重叠**：标签 y 坐标不能进入任何节点的 y ~ y+h 范围内，如果间距不够则不显示标签

### 主路径居中规则

画布 `offsetX` 必须基于**主路径宽度**计算，不能把侧分支算进去：

```javascript
// ✅ 正确：基于主路径范围居中
var mainMinX, mainMaxX;  // 只统计主路径节点和分组背景
var offsetX = -mainMinX + pad;

// ❌ 错误：把侧分支也算进去，导致主路径偏左
var offsetX = -allNodesMinX + pad;
```

### 通用规则

- 节点坐标由 JS 动态计算，不手动写死
- 连线用 `<line>` 和 `<path>`（折线转角 Q 贝塞尔 10px 圆角）
- 箭头用 `<marker>` 定义（8×6 开放 V 形）
- 渲染顺序：分组背景层 → 连线层 → 节点层
- 配色从 theme 对象取值，不硬编码
- 最终通过 Playwright 截图为 PNG

---

## 禁忌

- 不使用弧线连线
- 判断嵌套不超过 3 层
- 不使用设计规范以外的颜色
- 不加 shadow（除 Highlight 节点外）
