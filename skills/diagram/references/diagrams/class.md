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
| 继承 | `Child -> Parent`，标签 `extends` |
| 实现 | 虚线，标签 `implements` |
| 组合 | `Part -> Whole`，菱形箭头 |

---

## 配色

- 普通类：C-1 Blue（`#EFF6FF` / `#93C5FD`）
- 接口：C-2 Emerald（`#ECFDF5` / `#6EE7B7`）
- 抽象类：C-5 Violet（`#F5F3FF` / `#C4B5FD`）
- 关键类：Highlight（`#3B82F6` 实心白字）

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
