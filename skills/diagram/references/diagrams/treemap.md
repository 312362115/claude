# 矩形树图规范（Treemap）

> 工具：HTML/SVG · 布局：Squarified Treemap 算法 · 配色：S 系列统计图色板

---

## 适用场景

- 数据占比可视化（市场份额、磁盘空间、预算分配）
- 层级数据的面积对比
- 比饼图信息密度更高的比例展示

---

## 数据结构

```javascript
var data = {
  name: 'Root',
  children: [
    { name: 'Category A', value: 100, children: [
      { name: 'A-1', value: 60 },
      { name: 'A-2', value: 40 }
    ]},
    { name: 'Category B', value: 80 }
  ]
};
```

- 叶节点必须有 `value`
- 分支节点的 `value` 自动求和（可省略）
- 支持多层嵌套

---

## 布局算法

Squarified Treemap（Bruls et al. 2000）：
1. 按面积降序排列子节点
2. 贪心选择行/列方向，使宽高比趋近 1
3. 递归布局子节点

---

## 视觉规范

### 配色

- 顶层分类：S-1 ~ S-8 依次分配
- 子节点：继承父类颜色，降低不透明度（深度 1: 0.65，深度 2: 0.5）
- 分类标签：黑色半透明背景条 + 白色文字

### 尺寸

- 默认画布：800 × 500
- 格子间距：2px 白色间隙
- 叶节点圆角：2px
- 最小显示文字：宽 ≥ 50px 且高 ≥ 30px 显示 name + value，宽 ≥ 30px 且高 ≥ 20px 仅显示 name

### 标签

- 大格子：name（12px Bold 白色）+ value（11px 半透明白色），上下排列
- 小格子：仅 name（10px 白色）
- 极小格子：不显示文字

### 图例

- 画布下方，顶层分类 + 数值
- 12px 色块 + 文字

---

## 模板

`templates/html/treemap.html`

---

## Bridge 适配

```bash
python bridge.py --type treemap --config data.json --output chart.png
```

JSON 配置：
```json
{
  "type": "treemap",
  "title": "市场份额分布",
  "subtitle": "Market Share Distribution",
  "data": {
    "name": "Root",
    "children": [...]
  }
}
```
