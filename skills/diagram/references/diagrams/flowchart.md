# 流程图规范（Flowchart）

> 双轨制：日常用 Mermaid 快速出图，正式文档用 HTML/SVG 精确控制。

---

## 适用场景

- 工作流程（订单处理、用户注册、审批流程）
- 决策逻辑（条件分支、异常处理）
- 数据处理流程（ETL、请求处理管道）

---

## 模式选择

| 场景 | 模式 | 工具 | 模板 |
|------|------|------|------|
| 日常画图、快速出图、非正式场景 | 快速模式 | Mermaid | `templates/mermaid/flowchart.mmd` |
| 调研报告、方案文档、正式展示 | 精品模式 | HTML/SVG | `templates/html/flowchart.html` |

判断依据：调用方是 deep-research 或用户明确要求高质量 → 精品模式，其余 → 快速模式。

---

## 组件使用规则

| 元素 | 节点类型 | Mermaid 语法 | 色系 |
|------|---------|-------------|------|
| 流程起点 | Terminal Start | `([文字])` | 绿色 Emerald |
| 处理步骤 | Process | `[文字]` | 蓝色 Blue |
| 判断/条件 | Decision | `{文字}` | 黄色 Amber |
| 数据库操作 | Data Store | `[(文字)]` | 紫色 Violet |
| 关键步骤 | Highlight | `[文字]` | 蓝色实心白字 |
| 错误终点 | Error | `[文字]` | 红色 Rose |
| 成功终点 | Success | `[文字]` | 绿色 Emerald |
| 流程终点 | Terminal End | `([文字])` | 灰色 |

---

## 布局规则

1. **流向**：默认从上到下（`TD`）
2. **主路径**：保持直线向下
3. **判断分支**："是/通过"向下，"否/失败"向右
4. **回退/重试**：用虚线 `-.->` 表示
5. **子流程**：用 `subgraph` 包裹
6. **节点数上限**：15 个（超过拆子流程）

---

## 快速模式（Mermaid）

### classDef 样式表

每张 Mermaid 流程图必须包含以下 classDef（对应设计规范色值）：

```
classDef termStart fill:#ECFDF5,stroke:#6EE7B7,stroke-width:1.5px,color:#065F46
classDef termEnd fill:#F1F5F9,stroke:#CBD5E1,stroke-width:1.5px,color:#64748B
classDef process fill:#EFF6FF,stroke:#93C5FD,stroke-width:1.5px,color:#1E293B
classDef decision fill:#FFFBEB,stroke:#FCD34D,stroke-width:1.5px,color:#92400E
classDef highlight fill:#3B82F6,stroke:#3B82F6,stroke-width:1.5px,color:#FFFFFF
classDef success fill:#ECFDF5,stroke:#6EE7B7,stroke-width:1.5px,color:#065F46
classDef error fill:#FFF1F2,stroke:#FDA4AF,stroke-width:1.5px,color:#9F1239
classDef datastore fill:#F5F3FF,stroke:#C4B5FD,stroke-width:1.5px,color:#5B21B6
```

### init 主题配置

```
%%{init: {'theme':'base','themeVariables':{
  'primaryColor':'#EFF6FF','primaryBorderColor':'#93C5FD','primaryTextColor':'#1E293B',
  'lineColor':'#94A3B8','textColor':'#1E293B','fontSize':'13px',
  'fontFamily':'PingFang SC, Inter, sans-serif',
  'edgeLabelBackground':'#FFFFFF'
}}}%%
```

### 生成命令

```bash
mmdc -i input.mmd -o output.png -b white -s 2
```

---

## 精品模式（HTML/SVG）

用 SVG 精确控制每个节点位置和连线路径。

### 规则

- 节点坐标手动计算，遵循间距规范（步骤间 36px，含判断 48px，分支 ≥60px）
- 连线用 `<path>` 画直角折线，转角用 `Q` 贝塞尔曲线（10px 圆角）
- 箭头用 `<marker>` 定义，统一 12×10 尺寸
- 节点样式直接引用 CSS 变量（设计规范的色值）
- 最终通过 Playwright 截图为 PNG

### SVG 节点模板

```html
<!-- Process 节点 -->
<rect x="" y="" width="140" height="40" rx="6"
  fill="#EFF6FF" stroke="#93C5FD" stroke-width="1.5"/>
<text x="" y="" text-anchor="middle"
  font-size="13" font-weight="500" fill="#1E293B">步骤名</text>

<!-- Decision 节点 -->
<polygon points="cx,cy-30 cx+40,cy cx,cy+30 cx-40,cy"
  fill="#FFFBEB" stroke="#FCD34D" stroke-width="1.5"/>

<!-- 直角折线（带圆角转角） -->
<path d="M x1,y1 L x2,y1 Q x2+r,y1 x2+r,y1+r L x2+r,y2"
  stroke="#94A3B8" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>
```

---

## 禁忌

- 不使用弧线连线
- 判断嵌套不超过 3 层
- 不使用设计规范以外的颜色
- 不加 shadow（除 Highlight 节点外）
