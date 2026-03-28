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

| 元素 | 节点类型 | Mermaid 语法 | 色系 |
|------|---------|-------------|------|
| 流程起点 | Terminal Start | `([文字])` | 绿色 Emerald |
| 处理步骤 | Process | `[文字]` | 蓝色 Blue |
| 判断/条件 | Decision | `{文字}` | 黄色 Amber |
| 数据库操作 | Data Store | `[(文字)]` | 紫色 Violet |
| 关键步骤 | Highlight | `[文字]` | 蓝色实心白字 |
| 错误终点 | Error | `[文字]` | 红色 Rose |
| 成功终点 | Success | `[文字]` | 绿色 Emerald |
| 流程终点 | Terminal End | `([文字])` | 灰色 |

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

### 数据结构

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

### 布局算法

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

### 规则

- 节点坐标由 JS 动态计算，不手动写死
- 连线用 `<line>` 和 `<path>`（折线转角 Q 贝塞尔 10px 圆角）
- 箭头用 `<marker>` 定义（8×6 开放 V 形）
- 渲染顺序：连线层 → 节点层
- 配色从 theme 对象取值，不硬编码
- 最终通过 Playwright 截图为 PNG

---

## 禁忌

- 不使用弧线连线
- 判断嵌套不超过 3 层
- 不使用设计规范以外的颜色
- 不加 shadow（除 Highlight 节点外）
