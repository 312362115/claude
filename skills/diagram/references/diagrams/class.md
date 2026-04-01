# 类图规范（Class Diagram）

> 工具：HTML/SVG · Playwright 截图

---

## 适用场景

- 面向对象设计、领域模型、接口关系

---

## 组件使用

| 元素 | D2 实现 |
|------|--------|
| 类 | `shape: class`，三栏（类名/属性/方法） |
| 接口 | 类名标注 `«interface»` |
| 继承 | 空心三角箭头 + 实线，`type: 'inheritance'` |
| 实现 | 空心三角箭头 + 虚线，`type: 'realization'` |
| 组合 | 实心菱形（起点）+ 实线，`type: 'composition'` |
| 聚合 | 空心菱形（起点）+ 实线，`type: 'aggregation'` |
| 关联 | 开放箭头 + 实线，`type: 'association'` |
| 依赖 | 开放箭头 + 虚线，`type: 'dependency'` |

---

## 配色

- 普通类：C-1 Blue（`#EFF6FF` / `#93C5FD`）
- 接口：C-2 Emerald（`#ECFDF5` / `#6EE7B7`）
- 抽象类：C-5 Violet（`#F5F3FF` / `#C4B5FD`）
- 关键类：Highlight（`#3B82F6` 实心白字）

---

## 基数标记

关系支持 `fromCard` / `toCard` 字段标注多重性：

```javascript
{ from: 'User', to: 'Order', type: 'association', label: '下单', fromCard: '1', toCard: '*' }
```

常用标记值：`"1"` / `"*"` / `"0..1"` / `"1..*"` / `"0..*"`

标记渲染在连线两端，白底等宽字体，不与箭头重叠。

---

## 布局规则

1. 父类/接口在上，子类在下
2. 访问修饰符：`+` public / `-` private / `#` protected
3. 类名 `14px Bold`，属性/方法 `12px Regular`

---

## 模板

`templates/html/class.html`

---

## 生成方式

1. 生成 HTML 文件（纯 HTML+CSS+SVG，无外部依赖）
2. Playwright 截图为 PNG
