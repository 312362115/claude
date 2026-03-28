# 热力图规范（Heatmap）

> 工具：HTML/SVG · Playwright 截图

---

## 适用场景

- 矩阵数据可视化（用户活跃时段、相关性矩阵、覆盖率分布）
- 二维类目交叉分析

---

## 布局规则

1. 标题居中，副标题标注值域
2. x 轴在底部（时间/列维度），y 轴在左侧（行维度）
3. visualMap 右侧垂直，可拖拽筛选
4. 单元格: 白色边框 `borderWidth: 2`，圆角 `borderRadius: 3`
5. 数据标签: 高值白字，低值灰字（阈值 60）

---

## 配色

冷暖渐变 7 色：
`#e8f4fd` → `#b3d9f7` → `#6cb4ee` → `#3a8fd6` → `#e8755a` → `#d94535` → `#b91c1c`

---

## 交互配置

- tooltip: 显示行、列、值
- visualMap: `calculable: true`，可交互筛选

---

## 限制

- 行不超过 10 个
- 列不超过 24 个

---

## 模板

`templates/html/heatmap.html`

---

## 生成方式

1. 生成 HTML 文件（纯 HTML+CSS+SVG，无外部依赖）
2. Playwright 截图为 PNG（1200×800）
