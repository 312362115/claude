# ER 图规范（Entity Relationship Diagram）

> 工具：D2（`shape: sql_table`） · 仅快速模式（D2 效果已足够专业）

---

## 适用场景

- 数据库表结构设计
- 实体关系展示
- 数据模型文档

---

## 组件使用

| 元素 | D2 实现 |
|------|--------|
| 实体表 | `shape: sql_table` |
| PK | `{constraint: primary_key}` |
| FK | `{constraint: foreign_key}` |
| 关系连线 | `table1 -> table2`，标注基数 |

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

## 布局规则

1. 核心实体居中
2. 关联实体围绕核心展开
3. 只展示 PK/FK + 核心业务字段（不列全部字段）
4. 连线标注基数（1:1 / 1:N / M:N）
5. 单图不超过 8 张表

---

## 样式模板

```d2
users: 用户表 {
  shape: sql_table
  style: {
    fill: "#3B82F6"
    stroke: "#3B82F6"
    font-color: "#FFFFFF"
    font-size: 13
  }
  id: INT {constraint: primary_key}
  username: VARCHAR(50)
  email: VARCHAR(100)
}

orders: 订单表 {
  shape: sql_table
  style: {
    fill: "#EFF6FF"
    stroke: "#93C5FD"
    font-color: "#1E293B"
    font-size: 13
  }
  id: INT {constraint: primary_key}
  user_id: INT {constraint: foreign_key}
  total: DECIMAL
}

users -> orders: 1:N
```

---

## 模板

`templates/d2/er.d2`

---

## 生成命令

```bash
d2 --theme 0 --pad 40 input.d2 output.png
```
