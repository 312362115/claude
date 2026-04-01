# Diagram Skill 第三批能力补齐 — 实施方案

## 六条工作线

| # | 工作线 | 改动文件 | 复杂度 |
|---|--------|---------|--------|
| A | 流程图剩余形状（10+ 种） | `flowchart.html`, `flowchart.md` | 低（重复模式） |
| B | 状态图并发/fork-join/Notes | `state.html`, `state.md` | 中 |
| C | 柱线混合图 | 新建 `combo.html` + `combo.md`, `bridge.py`, `SKILL.md` | 中 |
| D | 流程图图标节点 + 富文本 | `flowchart.html`, `flowchart.md` | 中 |
| E | Kanban | 新建 `kanban.html` + `kanban.md`, `bridge.py`, `SKILL.md` | 中 |
| F | Git Graph | 新建 `git-graph.html` + `git-graph.md`, `SKILL.md` | 中 |

---

## A. 流程图剩余形状

当前 15 种，补齐到 25+ 种。新增：

| type 值 | 形状 | SVG 实现 | 用途 |
|---------|------|---------|------|
| `hexagon` | 六边形 | polygon 6 点 | 准备/初始化步骤 |
| `subroutine` | 双竖线矩形 | rect + 两条竖线 | 预定义处理/子程序 |
| `circle` | 正圆 | circle | 连接符/汇合点 |
| `manual-input` | 斜顶矩形 | polygon（左上角高） | 手动输入 |
| `delay` | D 形（右半圆） | path（矩形+右弧） | 延迟/等待 |
| `stored-data` | 弧形左侧矩形 | path（左弧+矩形） | 存储数据（磁盘侧视图） |
| `multi-document` | 堆叠文档 | 3 层偏移 path | 多文档/批量报告 |
| `tagged-document` | 折角文档 | path + 三角折角 | 标记文档 |
| `display` | 屏幕形 | path（左尖+右弧） | 显示输出 |
| `collate` | 沙漏/蝴蝶结 | polygon 交叉三角 | 合对/校验 |
| `extract` | 正三角 | polygon 3 点 | 提取/抽取 |
| `merge` | 倒三角 | polygon 3 点 | 合并 |

配色：复用现有 theme 配色（大部分用 node/process 蓝色系）。

---

## B. 状态图并发/fork-join/Notes

### 并发状态
`type: 'concurrent'`，容器内用水平虚线分隔并行区域。

数据结构：
```javascript
{ id: 'active', label: '活跃', type: 'concurrent', regions: [
  { id: 'r1', label: '网络', children: [{ id: 's1', ... }, { id: 's2', ... }] },
  { id: 'r2', label: '缓存', children: [{ id: 's3', ... }, { id: 's4', ... }] }
]}
```

ELK 实现：每个 region 是一个 compound node，外层 concurrent 是容器，regions 间画虚线分隔。

### Fork/Join
`type: 'fork'` / `type: 'join'`，黑色粗横条（宽 60px，高 4px）。

### Notes
`type: 'note'`，左边框矩形（`#F8FAFC` bg, 左 3px `#3B82F6`），通过 `attachTo` 字段关联状态。

---

## C. 柱线混合图（Combo Chart）

新建 `combo.html`，复合 bar + line 在同一坐标系。

数据结构：
```javascript
var data = {
  categories: ['Q1', 'Q2', 'Q3', 'Q4'],
  series: [
    { name: '营收', type: 'bar', values: [120, 150, 180, 200] },
    { name: '利润率', type: 'line', values: [0.15, 0.18, 0.22, 0.25], yAxis: 'right' }
  ]
};
```

支持双 Y 轴（左：柱状图绝对值，右：折线图百分比/比率）。配色用 S 系列。

---

## D. 流程图图标节点 + 富文本

### 图标节点
使用 Emoji 作为图标源（跨平台无依赖）。新增 `icon` 字段：

```javascript
{ id: 's1', label: '数据库', type: 'process', icon: '🗄️' }
```

渲染：icon 放在 label 左侧，14px 大小，间距 6px。

### 富文本
节点 label 支持 `\n` 换行 + `**加粗**` 语法：

```javascript
{ id: 's1', label: '用户认证\n**JWT Token**', type: 'process' }
```

渲染：多行 `<tspan>`，加粗段 font-weight 700。

---

## E. Kanban

新建 `kanban.html`，看板图。

数据结构：
```javascript
var columns = [
  { title: 'Backlog', cards: [
    { title: '用户登录', tag: 'feature', assignee: '张三' },
    { title: '修复 Bug #123', tag: 'bug' }
  ]},
  { title: 'In Progress', cards: [...] },
  { title: 'Done', cards: [...] }
];
```

视觉：竖列布局，每列有标题 + 计数。卡片有标签色条（feature=蓝/bug=红/task=绿）。

---

## F. Git Graph

新建 `git-graph.html`，Git 分支图。

数据结构：
```javascript
var commits = [
  { id: 'c1', message: 'Initial commit', branch: 'main' },
  { id: 'c2', message: 'Add feature', branch: 'main', parent: 'c1' },
  { id: 'c3', message: 'Start feature', branch: 'feature', parent: 'c2' },
  { id: 'c4', message: 'WIP', branch: 'feature', parent: 'c3' },
  { id: 'c5', message: 'Merge feature', branch: 'main', parent: ['c2', 'c4'], merge: true }
];
```

视觉：横向时间轴，每个 branch 一条彩色水平线，commit 圆点，merge 用连线汇合。配色按 branch 用 C-1~C-6。

---

## 实施顺序

| 阶段 | 内容 |
|------|------|
| 1 | 流程图剩余形状（批量加 case，低风险） |
| 2 | 状态图并发/fork-join/Notes |
| 3 | 流程图图标 + 富文本 |
| 4 | 柱线混合图 |
| 5 | Kanban |
| 6 | Git Graph |
