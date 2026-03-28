# 饼图规范（Pie Chart）

> 工具：HTML/SVG · Playwright 截图

---

## 适用场景

- 占比构成（市场份额、技术栈分布、预算分配）
- 南丁格尔玫瑰图（值差异较大时）
- 环形图（中心可显示总计）

---

## 布局规则

1. 标题居中，副标题标注数据来源
2. 图例右侧垂直排列，`icon: 'circle'`
3. 环形: `radius: ['40%', '70%']`
4. 玫瑰图: `roseType: 'area'`
5. 扇区圆角: `borderRadius: 8`，白色间隔 `borderWidth: 3`
6. 中心文字: graphic 组件显示总计

---

## 配色

8 色序列：`#667eea`, `#f5576c`, `#4facfe`, `#43e97b`, `#fa8231`, `#a55eea`, `#fc5c65`, `#26de81`

---

## 标签

- 外侧标签: 名称 + 占比百分比
- 引导线: `length: 20`, `length2: 30`
- rich 文本: 名称 14px Bold，百分比 13px 灰色

---

## 模板

`templates/html/pie.html`

---

## 生成方式

1. 生成 HTML 文件（纯 HTML+CSS+SVG，无外部依赖）
2. Playwright 截图为 PNG（1200×800）
