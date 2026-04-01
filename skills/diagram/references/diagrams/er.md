# ER 图规范（Entity Relationship Diagram）

> 工具：HTML/SVG + ELKjs 布局引擎

---

## 适用场景

- 数据库表结构设计
- 实体关系展示
- 数据模型文档

---

## 组件使用

| 元素 | 实现 |
|------|------|
| 实体表 | 圆角矩形，表头+字段列表 |
| PK | 字段标注 `pk: true` |
| FK | 字段标注 `fk: true`，紫色高亮 |
| 关系连线 | ELKjs 自动布局，支持 crow's foot 符号或文本标注 |

---

## 配色规则

**不再每张表用不同颜色**。统一用蓝色系（C-1），核心表用 Highlight 突出：

| 表类型 | 填充 | 边框 | 说明 |
|--------|------|------|------|
| 普通表 | `#EFF6FF` | `#93C5FD` | 默认 |
| 核心表 | `#3B82F6` | `#3B82F6` | 白色文字，重点表 |
| 关联表 | `#F8FAFC` | `#CBD5E1` | 中间表/辅助表 |

---

## 关系确认（画图前必做）

**画 ER 图前必须先逐条确认每对实体之间的关系类型**，不能默认都是 1:N。

确认方法：对每条关系问"A 的一条记录对应 B 的几条记录？反过来呢？"

| 关系类型 | 判断标准 | 典型场景 |
|---------|---------|---------|
| **1:1** | 双方各只有一条 | 用户 ↔ 用户详情、订单 ↔ 发票 |
| **1:N** | 一方有多条，另一方只有一条 | 用户 → 订单、分类 → 商品 |
| **M:N** | 双方都可有多条（需中间表） | 学生 ↔ 课程、标签 ↔ 文章 |

> M:N 关系在物理表设计中通过中间表拆成两个 1:N（如 order_items 拆 orders ↔ products）。ER 图中可以直接标 M:N，也可以展示中间表 + 两个 1:N。

---

## Crow's Foot 符号

支持两种关系标注模式：

### 模式一：Crow's foot 图形符号（推荐）

使用 `fromCard` / `toCard` 字段，支持四种符号：

| 符号 | 含义 | 说明 |
|------|------|------|
| `\|\|` | 恰好一个（Exactly One） | 两条垂直短线 |
| `\|o` | 零或一（Zero or One） | 垂直线 + 空心圆 |
| `\|{` | 一或多（One or More） | 垂直线 + 三叉 |
| `o{` | 零或多（Zero or More） | 空心圆 + 三叉 |

```javascript
{ from: 'users', to: 'orders', fromCard: '||', toCard: '|{', identifying: true }
```

### 模式二：文本标注（向后兼容）

使用 `label` 字段，文本放在连线中点白底矩形内：

```javascript
{ from: 'users', to: 'orders', label: '1 : N' }
```

## Identifying / Non-identifying

- `identifying: true`（默认）：实线，表示强依赖（子表的主键包含父表的外键）
- `identifying: false`：虚线，表示弱依赖（子表可独立存在）

---

## 布局规则

1. 核心实体居中
2. 关联实体围绕核心展开
3. 只展示 PK/FK + 核心业务字段（不列全部字段）
4. 连线标注基数（crow's foot 或文本）
5. 单图不超过 8 张表

---

## 数据结构示例

```javascript
var tables = [
  { id: 'users', label: '用户表', type: 'core', fields: [
    { name: 'id', dtype: 'INT', pk: true },
    { name: 'username', dtype: 'VARCHAR(50)' },
    { name: 'email', dtype: 'VARCHAR(100)' }
  ]},
  { id: 'orders', label: '订单表', type: 'normal', fields: [
    { name: 'id', dtype: 'INT', pk: true },
    { name: 'user_id', dtype: 'INT', fk: true },
    { name: 'total', dtype: 'DECIMAL' }
  ]}
];

var relations = [
  { from: 'users', to: 'orders', fromCard: '||', toCard: '|{', identifying: true }
];
```

---

## 模板

`templates/html/er.html`
