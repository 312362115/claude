# 图表回归测试用例

> 验证 26 种图表模板在不同数据量下的动态布局可靠性。
> 每种图表至少 2 组数据（L1 简单 / L2 中等），重点图表加 L3 复杂。

---

## 执行方式

```bash
# 1. 启动 HTTP 服务
cd skills/diagram/templates/html && python3 -m http.server 8765

# 2. 用 Playwright 逐个截图
# 通过 browser_run_code 批量执行

# 3. 人工 review 截图或自动检测
```

### 自动检测项

| 检测项 | 方法 | 通过标准 |
|--------|------|---------|
| 画布非空 | SVG width/height > 0 | 必须 |
| 无 JS 报错 | console.error 数量 | 0（favicon 除外） |
| 内容不越界 | body.scrollWidth ≤ viewport | body 无横向滚动 |
| 节点可见 | SVG 子元素数量 > 预期最小值 | 按图表类型定义 |

---

## P0 图表（核心 3 个）

### flowchart 流程图

**L1 — 简单（4 步，0 判断）**
```javascript
var steps = [
  { id: 'start', label: '开始', type: 'start' },
  { id: 's1', label: '处理', type: 'process' },
  { id: 's2', label: '完成检查', type: 'process' },
  { id: 'end', label: '结束', type: 'end' }
];
var sideNodes = [];
var groups = null;
```

**L2 — 中等（8 步，2 判断，含分组）**
- 当前模板默认数据（订单处理流程，3 个分组）

**L3 — 复杂（12+ 步，含侧分支子流程）**
```javascript
// 用户注册 + 实名认证 + 多判断 + 侧分支 next 数组
```

### sequence 时序图

**L1 — 简单（3 参与者，5 消息）**
```javascript
var participants = [
  { id: 'client', label: '客户端', type: 'actor' },
  { id: 'server', label: '服务端', type: 'service' },
  { id: 'db', label: '数据库', type: 'database' }
];
var messages = [
  { from: 'client', to: 'server', label: '请求数据', type: 'sync' },
  { from: 'server', to: 'db', label: '查询', type: 'sync' },
  { from: 'db', to: 'server', label: '返回结果', type: 'return' },
  { from: 'server', to: 'server', label: '处理数据', type: 'self' },
  { from: 'server', to: 'client', label: '响应', type: 'return' }
];
```

**L2 — 中等（6 参与者，含 fragment）**
- 当前模板默认数据

### er ER 图

**L1 — 简单（3 表）**
```javascript
var tables = [
  { id: 'users', label: '用户', type: 'core', fields: [
    { name: 'id', dtype: 'INT', pk: true },
    { name: 'name', dtype: 'VARCHAR' }
  ]},
  { id: 'posts', label: '文章', type: 'normal', fields: [
    { name: 'id', dtype: 'INT', pk: true },
    { name: 'user_id', dtype: 'INT', fk: true },
    { name: 'title', dtype: 'VARCHAR' }
  ]},
  { id: 'comments', label: '评论', type: 'junction', fields: [
    { name: 'id', dtype: 'INT', pk: true },
    { name: 'post_id', dtype: 'INT', fk: true },
    { name: 'content', dtype: 'TEXT' }
  ]}
];
var relations = [
  { from: 'users', to: 'posts', label: '1 : N' },
  { from: 'posts', to: 'comments', label: '1 : N' }
];
```

**L2 — 中等（6 表）**
- 当前模板默认数据

---

## P1 图表（3 个）

### class 类图

**L1** — 3 个类，无枚举
**L2** — 当前默认数据（6 类 3 枚举）

### architecture 架构图

**L1** — 2 层，各 2 节点
**L2** — 当前默认数据（4 层）

### swimlane 泳道图

**L1** — 2 泳道，4 步骤
**L2** — 当前默认数据（4 泳道 9 步骤）

---

## P2 图表（5 个）

### state 状态图

**L1** — 4 状态，3 转换
**L2** — 当前默认数据（8 状态 10 转换）

### swot / fishbone / venn / journey

**L1** — 每项 2-3 条数据
**L2** — 当前默认数据

---

## 已有动态模板（15 个，需验证未退化）

以下模板在本次改造前已是动态布局，需验证当前仍可正常工作：

| 模板 | 验证方式 |
|------|---------|
| mindmap | 截图确认树形展开正常 |
| decision-tree | 截图确认分支展开正常 |
| orgchart | 截图确认层级正常 |
| c4 | 截图确认分层容器正常 |
| dataflow | 截图确认左右流向正常 |
| network | 截图确认拓扑布局正常 |
| timeline | 截图确认纵向时间线正常 |
| gantt | 截图确认日期轴正常 |
| bar | 截图确认柱状正常 |
| line | 截图确认折线正常 |
| pie | 截图确认饼图正常 |
| scatter | 截图确认散点正常 |
| radar | 截图确认雷达正常 |
| heatmap | 截图确认热力正常 |
| sankey | 截图确认流带正常 |

---

## 边界条件测试

| 场景 | 预期 |
|------|------|
| 空数据（0 个节点） | 只显示标题，不报错 |
| 超长文本标签（50+ 字符） | 节点自动变宽，不截断 |
| 单节点图 | 正常显示，不报错 |
| 大量节点（20+） | 画布自动扩展，不重叠 |
| 中文 + 英文混排标签 | 宽度计算正确 |
