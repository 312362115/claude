# 画图工具示例对比

> 4 层工具覆盖全部图表类型，所有示例均为 PNG 输出，可直接嵌入 Markdown。

---

## 一、D2 结构图示例（8 种）

D2 擅长架构图、流程图、网络拓扑等，自动布局智能，默认样式专业。

### 1.1 系统架构图（HTML 版 - 推荐）

分层堆叠式架构图，HTML/CSS 精确控制布局，这才是架构图的正确形态。

![架构图-HTML版](./images/custom-architecture.png)

### 1.1b 系统架构图（D2 版 - 对比）

D2 基于图论布局，更适合有连线关系的图，不适合分层架构图。

![D2-架构图](./images/d2-architecture.png)

### 1.2 流程图

订单处理流程：库存检查 → 支付验证 → 发货

![D2-流程图](./images/d2-flowchart.png)

### 1.3 序列图（时序图）

API 认证鉴权流程：用户 → 前端 → API 网关 → 认证服务 → 数据库

![D2-序列图](./images/d2-sequence.png)

### 1.4 状态图

订单状态机：待支付 → 已支付 → 备货中 → 已发货 → 已签收

![D2-状态图](./images/d2-state.png)

### 1.5 ER 图（数据库 Schema）

电商数据库：用户、订单、商品、支付等表及关联关系（sql_table 语法）

![D2-ER图](./images/d2-er.png)

### 1.6 网络拓扑图

企业网络：互联网 → 防火墙 → DMZ → 内网分区（办公/服务器/开发）

![D2-网络拓扑](./images/d2-network.png)

### 1.7 决策树

数据库选型：按数据类型 → 读写比例 → 数据量级逐层决策

![D2-决策树](./images/d2-decision-tree.png)

### 1.8 数据流图

ETL 数据管道：数据源 → 采集 → 清洗 → 聚合 → 存储 → 输出

![D2-数据流图](./images/d2-dataflow.png)

---

## 二、Mermaid 结构图示例（9 种）

Mermaid 覆盖类型更广，序列图、C4 模型、思维导图、甘特图是其独占优势。

### 2.1 流程图

订单处理流程（与 D2 同场景，可对比样式差异）

![Mermaid-流程图](./images/mermaid-flowchart.png)

### 2.2 序列图（时序图）

API 认证流程（与 D2 同场景），支持 alt/loop 片段

![Mermaid-序列图](./images/mermaid-sequence.png)

### 2.3 类图

电商领域模型：User、Order、Product 等类及继承/组合关系

![Mermaid-类图](./images/mermaid-class.png)

### 2.4 状态图

订单状态机（与 D2 同场景），支持复合状态

![Mermaid-状态图](./images/mermaid-state.png)

### 2.5 ER 图

电商数据库实体关系（与 D2 同场景），带属性和基数标注

![Mermaid-ER图](./images/mermaid-er.png)

### 2.6 C4 容器图 ⭐ Mermaid 独占

电商系统 C4 容器视图：人员 → 系统 → 容器 → 外部依赖

![Mermaid-C4模型](./images/mermaid-c4.png)

### 2.7 思维导图 ⭐ Mermaid 独占

微服务架构设计：服务拆分、通信机制、数据管理、部署运维、安全治理

![Mermaid-思维导图](./images/mermaid-mindmap.png)

### 2.8 甘特图 ⭐ Mermaid 独占

电商项目开发计划：需求分析 → 技术方案 → 开发 → 测试 → 上线

![Mermaid-甘特图](./images/mermaid-gantt.png)

### 2.9 时间线 ⭐ Mermaid 独占

前端技术演进：1995-2024

![Mermaid-时间线](./images/mermaid-timeline.png)

---

## 三、ECharts 统计图表示例（6 种）

ECharts 覆盖 36+ 种统计图表，交互式渲染，截图为 PNG 后嵌入文档。

### 3.1 柱状图

2024 年各季度营收对比（分组柱状图，渐变色）

![ECharts-柱状图](./images/echarts-bar.png)

### 3.2 折线图

用户增长趋势（多线 + 面积填充 + 数据缩放）

![ECharts-折线图](./images/echarts-line.png)

### 3.3 饼图

技术栈使用分布（南丁格尔玫瑰图 + 环形）

![ECharts-饼图](./images/echarts-pie.png)

### 3.4 雷达图

技术方案评估对比（3 方案 × 6 维度）

![ECharts-雷达图](./images/echarts-radar.png)

### 3.5 桑基图

用户行为路径分析（流量从入口到转化/流失）

![ECharts-桑基图](./images/echarts-sankey.png)

### 3.6 热力图

一周用户活跃时段分布（24h × 7天）

![ECharts-热力图](./images/echarts-heatmap.png)

---

## 四、自定义 SVG/HTML 特殊图表示例（6 种）

工具覆盖不到的图表类型，用 HTML + CSS + SVG 自定义绘制。

### 4.1 SWOT 分析图

AI 创业公司 SWOT 分析（优势/劣势/机会/威胁四象限）

![SWOT分析](./images/custom-swot.png)

### 4.2 鱼骨图（因果分析）

"系统响应慢"根因分析（人员/流程/技术/环境/数据/工具 6 大类）

![鱼骨图](./images/custom-fishbone.png)

### 4.3 组织结构图

科技公司组织架构：CEO → C-level → 各团队

![组织结构图](./images/custom-orgchart.png)

### 4.4 文氏图

全栈工程师技能集（Frontend ∩ Backend ∩ DevOps）

![文氏图](./images/custom-venn.png)

### 4.5 用户旅程图

电商购物旅程：发现 → 浏览 → 比较 → 下单 → 支付 → 收货 → 评价

![用户旅程图](./images/custom-journey.png)

### 4.6 泳道图

请假审批流程（员工/主管/HR/系统 四泳道）

![泳道图](./images/custom-swimlane.png)

---

## 工具覆盖总结

| 工具 | 覆盖类型 | 示例数 | 适用场景 |
|------|---------|--------|---------|
| **D2** | 架构图、流程图、序列图、状态图、ER图、网络拓扑、决策树、数据流图 | 8 | 结构图（样式专业） |
| **Mermaid** | 流程图、序列图、类图、状态图、ER图、C4模型、思维导图、甘特图、时间线 | 9 | 结构图（类型更广） |
| **ECharts** | 柱状图、折线图、饼图、雷达图、桑基图、热力图等 36+ 种 | 6 | 统计图表 |
| **自定义 HTML/SVG** | SWOT、鱼骨图、组织结构图、文氏图、旅程图、泳道图 | 6 | 特殊图表兜底 |

**共计 29 个示例，覆盖全部主流图表类型。**
