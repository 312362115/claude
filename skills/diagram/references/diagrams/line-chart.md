# 折线图规范（Line Chart）

> 工具：HTML/SVG · Playwright 截图

---

## 适用场景

- 趋势变化（用户增长、性能指标、收入变化）
- 多系列对比趋势
- 带面积填充的趋势图

---

## 布局规则

1. 标题居中，副标题标注时间范围
2. 图例居中，`icon: 'roundRect'`
3. x 轴 `boundaryGap: false`（折线起始于轴线）
4. 线宽 `width: 3`，数据点 `symbolSize: 8`
5. 面积填充用渐变透明度（上 0.35 → 下 0.02）
6. 可选 dataZoom 滑块（数据量大时启用）

---

## 配色

| 系列 | 主色 | 面积渐变 |
|------|------|---------|
| 1 | `#667eea` | `rgba(102,126,234,0.35)` → `0.02` |
| 2 | `#f5576c` | `rgba(245,87,108,0.3)` → `0.02` |
| 3 | `#43e97b` | `rgba(67,233,123,0.3)` → `0.02` |

---

## 交互配置

- tooltip: `trigger: 'axis'`，十字准线
- 曲线平滑: `smooth: true`
- 数据点: 白色边框 `borderWidth: 2`

---

## 模板

`templates/html/line.html`

---

## 生成方式

1. 生成 HTML 文件（纯 HTML+CSS+SVG，无外部依赖）
2. Playwright 截图为 PNG（1200×800）
