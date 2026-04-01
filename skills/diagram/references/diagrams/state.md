# 状态图规范（State Diagram）

> 工具：HTML/SVG + ELKjs · 流向：默认横向（RIGHT）

---

## 适用场景

- 订单状态机、任务生命周期、审批状态流转

---

## 组件使用

| 元素 | 节点类型 | type 值 | 说明 |
|------|---------|---------|------|
| 初始状态 | 小实心圆 | `start` | 填充 `#1E293B`，直径 24px |
| 普通状态 | 圆角矩形 | `state` | C-1 蓝色系（`#EFF6FF` / `#93C5FD`） |
| 复合状态 | 圆角矩形容器 | `composite` | 层级色背景，包含子状态 |
| Choice 伪状态 | 小菱形 | `choice` | 28×28px，Amber 色（`#FFFBEB` / `#FCD34D`） |
| 终止状态 | 双圆（外圈+内圆） | `end` | `#1E293B` |

---

## 数据结构

```javascript
var states = [
  { id: 'start', label: '●', type: 'start' },
  { id: 'active', label: '活跃', type: 'composite', children: [
    { id: 'idle', label: '空闲', type: 'state' },
    { id: 'processing', label: '处理中', type: 'state' }
  ]},
  { id: 'c1', label: '', type: 'choice' },
  { id: 'end', label: '◎', type: 'end' }
];

var transitions = [
  { from: 'start', to: 'active', label: '激活' },
  { from: 'idle', to: 'processing', label: '收到请求' },
  { from: 'active', to: 'c1', label: '完成' },
  { from: 'c1', to: 'end', label: '[成功]' },
  { from: 'c1', to: 'active', label: '[重试]' }
];
```

---

## 复合状态（Composite）

- `type: 'composite'` + `children` 数组
- 支持最多 2 层嵌套（composite 里套 composite）
- ELKjs compound nodes 自动布局
- 容器背景使用层级色（L-1/L-2/L-3 按深度）
- 容器内子状态用白底（`#FFFFFF`）+ C-1 边框，与容器形成层次
- 标签在容器左上角，13px Bold

---

## Choice 伪状态

- `type: 'choice'`，小菱形，无文字
- 用于条件分支：出边标签使用 guard 格式如 `[条件]`
- 配色：Amber（`fill: #FFFBEB`, `stroke: #FCD34D`）

---

## 布局规则

1. 默认 RIGHT（从左到右），ELKjs layered 算法
2. 初始状态最左，终止状态最右
3. 正交路由 + 8px 圆角转折
4. 状态不超过 10 个（不含 start/end）
5. 边标签放在路径中点，白底衬底

---

## 配色

- 普通状态：C-1 Blue（`#EFF6FF` / `#93C5FD`）
- 复合容器：层级色 L-1~L-3
- Choice：Amber（`#FFFBEB` / `#FCD34D`）
- 连线：`#94A3B8`

---

## 模板

`templates/html/state.html`
