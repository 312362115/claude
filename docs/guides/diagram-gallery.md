# 图表类型全览

> 画图 Skill 支持 26 种图表类型，全部使用 HTML+SVG 实现，Playwright 截图输出 PNG。
> 每种图表均有专属规范和示例模板，参见 `skills/diagram/references/diagrams/` 目录。

---

## 结构图（19 种）

### 1. 流程图（Flowchart）

展示工作流程、业务逻辑、决策分支。最常用的图表类型之一。

**适用场景：** 审批流程、业务流程、算法逻辑、操作步骤说明

![流程图](../assets/diagram/showcase/flowchart.png)

---

### 2. 泳道图（Swimlane）

在流程图基础上增加角色/部门维度，展示多方协作流程。

**适用场景：** 跨部门协作流程、多角色审批流、服务间交互流程

![泳道图](../assets/diagram/showcase/swimlane.png)

---

### 3. 时序图（Sequence Diagram）

展示对象之间的消息传递顺序，强调时间维度上的交互。

**适用场景：** API 调用链路、微服务间通信、用户操作时序、协议交互

![时序图](../assets/diagram/showcase/sequence.png)

---

### 4. 架构图（Architecture Diagram）

展示系统分层结构、技术栈组成、模块关系。

**适用场景：** 系统架构设计、技术选型展示、部署架构、分层架构

![架构图](../assets/diagram/showcase/architecture.png)

---

### 5. 状态图（State Diagram）

展示对象在不同状态之间的迁移和触发条件。

**适用场景：** 订单状态流转、任务生命周期、有限状态机、协议状态

![状态图](../assets/diagram/showcase/state.png)

---

### 6. ER 图（Entity-Relationship Diagram）

展示数据库表结构及表之间的关系。

**适用场景：** 数据库设计、数据模型设计、表关系梳理

![ER图](../assets/diagram/showcase/er.png)

---

### 7. 类图（Class Diagram）

展示面向对象设计中的类、属性、方法及类间关系。

**适用场景：** 面向对象设计、领域模型、API 数据结构、设计模式

![类图](../assets/diagram/showcase/class.png)

---

### 8. 网络拓扑图（Network Topology）

展示网络设备、连接关系、分层区域。

**适用场景：** 企业网络规划、服务器部署拓扑、安全分区设计

![网络拓扑图](../assets/diagram/showcase/network.png)

---

### 9. 决策树（Decision Tree）

展示基于条件分支的选择路径，从根节点逐步缩小到结论。

**适用场景：** 技术选型决策、故障排查指南、分类逻辑、产品选择引导

![决策树](../assets/diagram/showcase/decision-tree.png)

---

### 10. 数据流图（Dataflow Diagram）

展示数据从来源经过处理到目标的流转路径。

**适用场景：** ETL 管道设计、数据处理流水线、消息队列架构、数据治理

![数据流图](../assets/diagram/showcase/dataflow.png)

---

### 11. C4 容器图（C4 Container Diagram）

展示软件系统内部的容器（应用、数据库、消息队列等）及其交互关系。C4 模型的第二层视图。

**适用场景：** 系统架构文档、微服务边界划分、技术方案评审

![C4容器图](../assets/diagram/showcase/c4.png)

---

### 12. 思维导图（Mind Map）

以中心主题为根节点，向外发散展示知识结构和概念关系。

**适用场景：** 知识梳理、头脑风暴、技术方案拆解、学习笔记

![思维导图](../assets/diagram/showcase/mindmap.png)

---

### 13. 甘特图（Gantt Chart）

以时间轴为基础展示项目任务的计划、进度和依赖关系。

**适用场景：** 项目排期、迭代规划、里程碑管理、资源分配

![甘特图](../assets/diagram/showcase/gantt.png)

---

### 14. 时间线（Timeline）

按时间顺序展示事件、里程碑或发展历程。

**适用场景：** 产品演进历程、技术发展史、项目大事记、版本发布记录

![时间线](../assets/diagram/showcase/timeline.png)

---

### 15. 组织结构图（Org Chart）

展示组织内部的层级关系和汇报结构。

**适用场景：** 团队架构、公司组织结构、项目团队分工

![组织结构图](../assets/diagram/showcase/orgchart.png)

---

### 16. SWOT 分析图

展示优势（Strengths）、劣势（Weaknesses）、机会（Opportunities）、威胁（Threats）四象限分析。

**适用场景：** 战略分析、竞品分析、项目可行性评估、个人发展规划

![SWOT分析](../assets/diagram/showcase/swot.png)

---

### 17. 鱼骨图（Fishbone / Ishikawa）

展示问题的根本原因分析，按类别分支展开。

**适用场景：** 根因分析、质量问题排查、故障复盘、流程改进

![鱼骨图](../assets/diagram/showcase/fishbone.png)

---

### 18. 文氏图（Venn Diagram）

展示集合之间的交集、并集关系。

**适用场景：** 概念对比、技术方案重叠分析、角色职责划分、功能覆盖对比

![文氏图](../assets/diagram/showcase/venn.png)

---

### 19. 旅程图（Journey Map）

展示用户在完成目标过程中的体验、情绪和触点。

**适用场景：** 用户体验设计、服务设计、产品流程优化、痛点分析

![旅程图](../assets/diagram/showcase/journey.png)

---

## 统计图（7 种）

### 20. 柱状图（Bar Chart）

展示离散类目之间的数值对比。

**适用场景：** 季度营收对比、部门业绩排名、产品销量对比、A/B 测试结果

![柱状图](../assets/diagram/showcase/bar.png)

---

### 21. 折线图（Line Chart）

展示数据随时间或连续变量的变化趋势。

**适用场景：** 用户增长趋势、性能监控曲线、股价走势、温度变化

![折线图](../assets/diagram/showcase/line.png)

---

### 22. 饼图（Pie Chart）

展示整体中各部分的占比构成。

**适用场景：** 市场份额分布、预算分配、技术栈使用比例、用户画像构成

![饼图](../assets/diagram/showcase/pie.png)

---

### 23. 散点图（Scatter Plot）

展示两个变量之间的分布关系，气泡大小可映射第三维度。

**适用场景：** 相关性分析、聚类分析、异常检测、用户行为分布

![散点图](../assets/diagram/showcase/scatter.png)

---

### 24. 雷达图（Radar Chart）

展示多维度指标的综合评估对比。

**适用场景：** 技术方案多维评估、人才能力画像、产品竞品对比、绩效雷达

![雷达图](../assets/diagram/showcase/radar.png)

---

### 25. 热力图（Heatmap）

用颜色深浅展示矩阵数据中的分布规律。

**适用场景：** 用户活跃时段分布、功能使用频率、代码提交热度、相关性矩阵

![热力图](../assets/diagram/showcase/heatmap.png)

---

### 26. 桑基图（Sankey Diagram）

用流带宽度展示数量在不同阶段之间的流向和分配。

**适用场景：** 用户转化路径、能源/资源流向、预算分配流转、流量来源分析

![桑基图](../assets/diagram/showcase/sankey.png)
