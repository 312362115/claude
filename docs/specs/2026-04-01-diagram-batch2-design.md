# Diagram Skill 第二批能力补齐 — 实施方案

## Context

对标 Mermaid v11.13.0，补齐 diagram skill 在状态图、流程图、统计图上的能力差距。第一批已完成类图 UML 箭头/ER crow's foot/流程图新形状，本批聚焦：状态图复合状态、流程图连线+子图嵌套、Treemap 新类型。

---

## 三条工作线

| # | 工作线 | 改动文件 | 复杂度 |
|---|--------|---------|--------|
| A | 状态图：复合/嵌套状态 + Choice 伪状态 | `state.html`, `state.md` | 中 |
| B | 流程图：4 种新连线 + DAG 子图嵌套（3 层） | `flowchart.html`, `flowchart.md` | 中高 |
| C | Treemap 矩形树图 | 新建 `treemap.html` + `treemap.md`, `bridge.py`, `SKILL.md` | 中 |

---

## A. 状态图增强

### A1. 复合/嵌套状态

**数据结构**：states 数组支持 `type: 'composite'` + `children`:

```javascript
var states = [
  { id: 'start', label: '●', type: 'start' },
  { id: 'active', label: '活跃', type: 'composite', children: [
    { id: 'idle', label: '空闲', type: 'state' },
    { id: 'processing', label: '处理中', type: 'state' }
  ]},
  { id: 'end', label: '◎', type: 'end' }
];
```

**布局**：ELKjs 原生支持 compound nodes，composite state 作为带 `children` 的父节点：
- padding: `top=40`（给标签留空间）, `left/right/bottom=16`
- ELK 自动计算父节点尺寸

**渲染**：
- 容器：圆角矩形 `rx: 8`，层级色 L-1/L-2（按深度）
- 标签：左上角 13px Bold
- 子节点：白底 + C-1 边框（与容器形成层次）
- 支持 2 层嵌套（composite 里套 composite）

### A2. Choice 伪状态

- `type: 'choice'`，小菱形 28×28px，无文字
- 配色复用 Amber（`fill: #FFFBEB`, `stroke: #FCD34D`）
- 出边带 guard 条件标签（如 `[金额 > 100]`）

### A3. 改动清单

| 文件 | 改动 |
|------|------|
| `templates/html/state.html` | 加 `flattenStates()` 递归函数、ELK compound node 构建、composite 背景渲染、choice 菱形渲染 |
| `references/diagrams/state.md` | 全面重写：D2 → HTML/SVG+ELKjs，补 composite/choice 文档 |

---

## B. 流程图增强

### B1. 四种新连线类型

新增 SVG marker + edge 数据扩展：

| edgeType | 视觉效果 | marker 实现 |
|----------|---------|------------|
| `bidirectional` | 双向箭头 ←→ | 两端各一个箭头 marker（正/反） |
| `circle` | 圆头 ─● | 终点小实心圆 r=3 |
| `cross` | 叉头 ─✕ | 终点 X 形 |
| `thick` | 粗线 ═→ | stroke-width: 3，复用标准箭头 |

**数据结构**（DAG 模式）：
```javascript
var edges = [
  { from: 'a', to: 'b', edgeType: 'bidirectional' },
  { from: 'b', to: 'c', edgeType: 'circle' },
  // 默认不写 = 标准箭头
];
```

### B2. DAG 模式子图嵌套（最多 3 层）

**数据结构**：DAG 模式增加 `groups` 定义，节点通过 `group` 字段归属：

```javascript
var groups = [
  { id: 'frontend', label: '前端服务', children: [
    { id: 'react', label: 'React 模块' }
  ]},
  { id: 'backend', label: '后端服务' }
];
var nodes = [
  { id: 'a', label: 'Step A', type: 'process', group: 'frontend' },
  { id: 'b', label: 'Step B', type: 'process', group: 'react' },
];
```

**ELKjs compound nodes**：每个 group → ELK 父节点 + children，padding `top=40, sides=16`
**渲染**：层级色 L-1/L-2/L-3 按深度，圆角矩形背景，渲染顺序 groups → edges → nodes

### B3. 改动清单

| 文件 | 改动 |
|------|------|
| `templates/html/flowchart.html` | 4 个新 marker 函数、edgeType 处理逻辑、groups 层级构建 + ELK compound + 背景渲染 |
| `references/diagrams/flowchart.md` | 补 4 种连线文档 + DAG 子图嵌套文档 |

---

## C. Treemap 新图表类型

### C1. 算法

Squarified treemap（Bruls et al. 2000），纯 JS 实现 ~60 行。递归分区，贪心选择行/列方向使宽高比趋近 1。

### C2. 数据结构

```javascript
var data = {
  name: 'Root',
  children: [
    { name: 'Category A', value: 100, children: [
      { name: 'A-1', value: 60 },
      { name: 'A-2', value: 40 }
    ]},
    { name: 'Category B', value: 80 }
  ]
};
```

叶节点有 `value`，分支节点自动求和。

### C3. 视觉设计

- 配色：S-1~S-8 分配给顶层类别，子节点同色系降低不透明度
- 文字：大格子显示 name + value，小格子（<40px）隐藏文字
- 间距：格子间 2px 白色间隙，叶节点 rx=2
- 标题：22px Bold `#1a1a2e`（统计图标准）
- body class: `auto-size`

### C4. 改动清单

| 文件 | 改动 |
|------|------|
| 新建 `templates/html/treemap.html` | squarify 算法 + SVG 渲染，~150 行 |
| 新建 `references/diagrams/treemap.md` | 数据结构 + 配色 + 示例 |
| `scripts/bridge.py` | 加 `adapt_treemap()` + 注册 ADAPTERS |
| `SKILL.md` | 图表类型速查表加 treemap |

---

## 实施顺序

| 阶段 | 内容 | 依赖 |
|------|------|------|
| **Phase 1** | 流程图 4 种新连线 | 无 |
| **Phase 2** | 状态图 composite + choice | 无 |
| **Phase 3** | 流程图 DAG 子图嵌套 | Phase 1（marker 复用） |
| **Phase 4** | Treemap 新类型 | 无（独立） |

每个阶段完成后：浏览器验证 → 回归测试 → 更新文档。

---

## 验证方式

1. **每阶段产出测试用例**，用 Playwright 截图验证渲染正确性
2. **回归测试**：跑现有 25 种图表 × L1-L4 全量用例，确保无破坏
3. **边界 case**：
   - 状态图：空 composite、单子节点 composite、2 层嵌套
   - 流程图连线：4 种类型混合在同一图
   - 流程图子图：空 group、跨 group 连线、3 层嵌套
   - Treemap：单节点、等值、极小值、单子节点分支
4. 测试用例沉淀到 `docs/tests/`
