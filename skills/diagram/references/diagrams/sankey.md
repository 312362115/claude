# 桑基图规范（Sankey Diagram）

> 工具：HTML/SVG · Playwright 截图

---

## 适用场景

- 流量路径分析（用户行为漏斗、流量来源分布）
- 资源分配流向
- 能量/成本流转

---

## 布局规则

1. 标题居中，副标题标注数据含义
2. 节点宽度: `nodeWidth: 24`
3. 节点间距: `nodeGap: 16`
4. 布局迭代: `layoutIterations: 32`
5. 四周留白: top 90, bottom 40, left/right 80

---

## 配色

每个节点独立配色，使用主题色序列：

| 节点类型 | 色值 |
|---------|------|
| 入口节点 | `#667eea`, `#764ba2`, `#f093fb`, `#f5576c` |
| 中间节点 | `#4facfe`, `#43e97b`, `#fa8231` |
| 终点-成功 | `#20bf6b` |
| 终点-流失 | `#a5b1c2` |

---

## 连线

- 渐变色: `color: 'gradient'`
- 曲率: `curveness: 0.5`
- 透明度: `opacity: 0.35`
- 悬停聚焦: `emphasis.focus: 'adjacency'`

---

## 标签

- 节点标签: 14px Bold，深色
- tooltip: 显示来源→目标和流量值

---

## 模板

`templates/html/sankey.html`

---

## 生成方式

1. 生成 HTML 文件（纯 HTML+CSS+SVG，无外部依赖）
2. Playwright 截图为 PNG（1200×800）
