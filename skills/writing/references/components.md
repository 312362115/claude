# 写作组件库（Components）

> 这不是一份"必读文档"。它是组件的目录——按你写的内容**长什么样**来挑组件，而不是按"写的是 spec / PRD / 汇报"来挑模板。
>
> 用法：先看清你要表达的内容是什么形态（数字？决策？对比？流程？时间线？），再来这里查"哪个组件能装这种形态"。

---

## 阅读指南

每个组件按**统一格式**描述：

| 字段 | 含义 |
|------|------|
| **触发条件** | 你要写的内容长什么样，会召唤这个组件 |
| **HTML 类名 / Markdown 形式** | 实现方式 |
| **输入数据形态** | 这个组件吃什么数据 |
| **不要用的场景** | 什么情况下别用，避免误用 |

组件无层级——hero 不比 callout 高级，只是触发条件不同。能组合的组合，能省的省。

---

## A. 顶部冲击型组件（建立全局认知）

### A1. Hero 区

- **触发条件**：文档需要"一屏建立全局认知"——通常是评审、路演、对外宣讲、季度复盘、年度总结。**短报告 / 内部 spec 不需要**。
- **HTML 类名**：`.hero` + `.eyebrow` + `<h1>` + `.lead` + `.pill` + `.toc`
- **输入数据形态**：标题、副标（一句话）、3-8 个关键词、4 个章节锚点
- **不要用**：技术 spec、API 文档、内部 plan——这些读者打开就直接进正文

### A2. Eyebrow（小标）

- **触发条件**：标题前需要给读者一个"这是哪种文档"的前缀（如 `Technical Review` / `Q1 OKR Recap` / `Architecture Pitch`）
- **HTML 类名**：`.eyebrow`
- **输入数据形态**：一行大写英文短语，2-4 词
- **不要用**：中文场景、内部技术文档——让出空间给标题

### A3. Pill（关键词芯片）

- **触发条件**：要在标题旁强化方案/项目的几个关键属性（"四层架构 / 多租户 / 事件驱动"）
- **HTML 类名**：`.pill`
- **输入数据形态**：3-8 个短关键词
- **不要用**：超过 8 个会变成"关键词云"反而失焦——超出就不是 pill 该解决的问题，改用表格或分组卡

### A4. TOC Chips（章节快跳）

- **触发条件**：长报告需要顶部快速跳转，且章节数 ≤ 6（再多变 sidebar TOC）
- **HTML 类名**：`.toc a`
- **输入数据形态**：4-6 个 `{label, anchor}`
- **不要用**：章节 ≥ 7 时改用 `.sidebar` 侧栏 TOC（参见 `report-template.html`）

---

## B. 章节组织组件

### B1. 章节双栏头

- **触发条件**：章节多（≥ 4 个）且每节有清晰的"是什么"提要时——读者扫读时不打开正文也能知道这一章干嘛
- **HTML 类名**：`.section-head` + `.section-index` + `<h2>` + `.summary`
- **输入数据形态**：编号（01/02）、标题、一句话提要（≤ 30 字）
- **不要用**：章节 ≤ 3 时省掉编号；提要写不出一句话就说明章节本身定位模糊，先想清楚再写

### B2. 普通章节标题

- **触发条件**：默认就用——任何 Markdown / HTML 文档
- **形式**：Markdown `## / ###` 或 HTML `<h2> / <h3>`

---

## C. 内容主体组件

### C1. Figure（图片画框）

- **触发条件**：内容是"一张图说清楚的事"——架构图、流程图、ER 图、roadmap
- **HTML 类名**：`.figure` + `<img>` + `.caption`
- **输入数据形态**：图片路径、可选的简短 caption
- **不要用**：图本身就在 `.chart-container` 里时（图表容器自带画框），不要再嵌一层

### C2. Card-Grid（卡片网格）

- **触发条件**：要并列展示**同质**的多项内容（3-9 项）——核心边界、Agent 角色、模块特性、风险点
- **HTML 类名**：`.grid-2` / `.grid-3` / `.grid-4` 容器 + `.card`
- **输入数据形态**：每张卡 `{title, description}`
- **不要用**：项数 ≥ 10 时改用表格；项与项之间不同质（一个是数据一个是结论）时不要硬塞同一个 grid

### C3. 表格

- **触发条件**：内容是结构化的"行 × 列"——评审项 vs 当前方案、维度 × 候选方案、API 参数表
- **HTML 类名**：`<table>` + `<thead>` / `<tbody>`（直接用，模板自带样式）
- **输入数据形态**：列定义 + 行数据
- **不要用**：表格只有 2 列且每行只有一句话时考虑用 `.callout` 或列表；超过 5 列建议拆分

### C4. VS-Block（双栏对比块）

- **触发条件**：明确的"A vs B"二选一对比——计划 vs 实际、本期 vs 上期、方案 A vs 方案 B
- **HTML 类名**：`.vs-block` + 两个 `.vs-col`
- **输入数据形态**：左右两侧 `{label, content (list / paragraph)}`
- **不要用**：三方及以上对比改用表格；同方向不同维度的对比改用 grid-2

### C5. Timeline（时间轴）

- **触发条件**：内容有**时间维度**或**阶段顺序**——里程碑、版本演进、roadmap 阶段
- **HTML 类名**：`.timeline` + `.tl-item` + `.tl-dot` + `.tl-title` + `.tl-desc`
- **输入数据形态**：每项 `{title, time, description}`
- **不要用**：阶段没有时间含义时（仅是逻辑分层）改用 grid 或卡片

---

## D. 决策与状态组件

### D1. Decision-Card（决策卡，三色信号）

- **触发条件**：内容是**决策性陈述**——已经做出的决策、待观察的约束、未决的风险
- **HTML 类名**：`.card.decision` / `.card.decision-warn` / `.card.decision-risk`
- **输入数据形态**：`{title, description, optional reasoning}`
- **三色信号规则**（信号 = 颜色，混用会失效）：

| 内容性质 | 类名 | 颜色 |
|---------|------|------|
| 已选方案 / 已确认决策 | `.decision` | 青绿 |
| 有约束 / 待验证 / 看趋势再决定 | `.decision-warn` | 橙 |
| 风险点 / 未决问题 / 阻塞项 | `.decision-risk` | 粉红 |

- **不要用**：单纯的描述性内容（"这是什么"）不要套决策卡——改用普通 `.card`；不要为了视觉好看混色

### D2. Callout（提示框）

- **触发条件**：在正文中插入需要**视觉打断**的关键提示——重要发现、警告、备注、限制条件
- **HTML 类名**：`.callout-note` / `.callout-warning` / `.callout-danger` / `.callout-success`
- **输入数据形态**：`{title (optional), body}`
- **不要用**：满篇 callout = 没有 callout，每节最多 1-2 个

### D3. Badge（行内徽章）

- **触发条件**：在标题/表格行/列表项中标注一个状态——`已完成` `进行中` `延期` `风险`
- **HTML 类名**：`.badge.badge-green/blue/orange/red/gray/purple`
- **输入数据形态**：极短文字（≤ 4 字）
- **不要用**：篇幅长的状态说明改用 callout

---

## E. 数据可视化组件

### E1. Metric-Card（指标卡片）

- **触发条件**：内容是**关键数字**——完成率、收入、用户数、达成率
- **HTML 类名**：`.metric-grid` 容器 + `.metric-card` + `.metric-value` + `.metric-label` + 可选 `.metric-change`
- **输入数据形态**：`{value, label, change? }`
- **不要用**：没有数字的"质性结论"不要硬塞数字凑指标卡

### E2. Progress-Bar（进度条）

- **触发条件**：内容是**有上限的进度百分比**——开发进度、目标达成度、模块完成度
- **HTML 类名**：`.progress-group` + `.progress-item` + `.progress-track` + `.progress-fill.fill-{success|primary|warning|danger}`
- **输入数据形态**：每项 `{label, percentage, color-tier}`
- **不要用**：没有"100% 上限"概念的指标（如"用户数"）改用 metric-card

### E3. Score-Bar（评分条）

- **触发条件**：多维度量化评估——选型雷达的展开、能力评分
- **HTML 类名**：`.score-bar` + `.label` + `.bar` + `.fill-{high|med|low}` + `.score-value`
- **输入数据形态**：每项 `{dimension, score, max}`
- **不要用**：超过 8 个维度改用雷达图（调 diagram skill）

### E4. Chart-Container（图表容器）

- **触发条件**：调 diagram skill 生成的统计图（柱状/折线/饼图等）需要嵌入文档
- **HTML 类名**：`.chart-container` + `.chart-inner` + `.chart-caption`
- **输入数据形态**：嵌入 SVG 或 `<img>` + 可选 caption
- **不要用**：单纯的架构图/流程图用 `.figure` 即可

---

## F. 图示组件（轻量级，不调 diagram skill）

### F1. ` ```flow ` 代码块

- **触发条件**：≤ 10 个节点的简单流程、决策树、阶段串联——方案中的执行步骤、筛选流程
- **形式**：preview-md 扩展语法（详见 preview-md SKILL.md）
- **不要用**：复杂多分叉、跨角色流程改调 diagram skill 的流程图/泳道图

### F2. ` ```terminal ` 代码块

- **触发条件**：CLI 操作、安装/启动步骤、命令输出示例——开发指南、调研附录的复现步骤
- **形式**：preview-md 扩展语法
- **不要用**：单条命令用 `` ```bash ``

---

## G. 文档级结构（不是组件，是组合范式）

`references/templates/*.md` 下的文件（spec.md / plan.md / prd.md / api-doc.md / dev-guide.md / operation-plan.md / user-guide.md）**不是模板**，是**已被验证的常见组合范式**——给的是"这种文档通常含哪些章节"的参考，**不是"必备章节清单"**。

写作时：
- 内容长得像它给的范式 → 直接借鉴章节顺序
- 内容只覆盖部分 → 删掉用不到的章节
- 内容超出范式覆盖 → 加自定义章节

判断标准：**章节存在的理由是内容需要它，不是模板要求它**。

---

## H. 组合速查（"内容长什么样 → 用什么组件"）

| 你要表达的内容 | 推荐组件 |
|--------------|---------|
| "我们做了一件大事，请认真听" | Hero + Pill + TOC |
| "这一章在讲 X" | section-head + summary |
| "一张图说清楚" | Figure |
| "并列展示 N 个同质项" | Card-Grid（grid-2/3/4） |
| "A vs B 二选一" | VS-Block |
| "结构化对照表" | 表格 |
| "时间维度 / 阶段顺序" | Timeline |
| "已选方案 / 待观察 / 风险" | Decision-Card 三色 |
| "关键数字" | Metric-Card |
| "0-100% 进度" | Progress-Bar |
| "维度评分" | Score-Bar |
| "重要提示打断阅读" | Callout |
| "行内状态标注" | Badge |
| "嵌入统计图" | Chart-Container |
| "嵌入架构/流程图" | Figure |
| "≤ 10 节点的轻量流程" | ` ```flow ` 代码块 |
| "CLI 命令演示" | ` ```terminal ` 代码块 |

---

## I. 反模式

- ❌ 因为有路演模板就硬塞 Hero——内部 spec 不需要 Hero
- ❌ 因为有决策卡就把所有结论包成 decision-card——决策卡是为"已决/未决/风险"三态信号化设计的
- ❌ 因为有 metric-card 就编造数字凑指标——没有数字就别用
- ❌ 因为模板说"必备章节"就硬写——章节存在的理由是内容需要它
- ❌ 同一份文档里 grid-2 / grid-3 / grid-4 混用 ≥ 3 种——视觉节奏会乱
- ❌ Decision-card 三色混用——信号失效
