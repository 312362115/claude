# Changelog — finance-analysis

## 0.2.0（2026-04-23）

**估值 + 选股 + 美股 IPO 补全**。从单股决策扩展到"从赛道到 Top-N，从现价到三情景，从 HK IPO 到 US IPO"的完整决策链。

### Frameworks（新增 4）

- `valuation-relative.md`（364 行）：相对估值，三段式（对标池 → 三情景 × 合理 PE × 概率加权 → 主题溢价 → 隐含预期位置）。承接"股市是预期驱动"认知，Worked Example：东山精密。
- `valuation-dcf.md`（449 行）：DCF 估值，只讲三情景 + 敏感性必选。Gordon & 出口倍数交叉验证。Worked Example：NVDA 2023 成长期。
- `stock-selection.md`（416 行）：alpha-generation 的可执行简化版。4 步筛选器（赛道/龙头/质量/成长）+ 30/60/100 打分 + Top-N 待研究清单。Worked Example：A 股动力电池（CATL 92 / 比亚迪 87 / 亿纬 79）。
- `us-ipo-arbitrage.md`（479 行）：美股 IPO，对照港股差异，核心命题从"打不打"转为"三路径 EV 比较"（不参与等 Lockup / 首日追涨 / 长期持有）。Worked Example：DoorDash 2020-12。

### Templates（新增 2）

- `valuation-card.md`（479 行）：通用估值决策卡，同时支持 valuation-relative 和 valuation-dcf。含东山精密 + NVDA 填充示例（双方法论覆盖）。
- `stock-screening-card.md`（311 行）：选股筛选卡，记录 4 步筛过程 + 30/60/100 打分 + Top-N 清单（Core/Satellite 标注）。CATL 填充示例。

### SKILL.md

- frontmatter 版本 0.1.0 → 0.2.0，last_updated 2026-04-23
- 触发词扩充：相对估值 / DCF / 合理估值 / DoorDash / Coinbase / Lockup / 筛选 / Top-N / 赛道龙头 / 情景分析
- 辅助 framework 表补齐 4 个新 framework + 版本标注
- 路线图表 0.2.0 标 ✅ 本版

### frameworks/_index.md

- 辅助 framework 表分组（核心分析/估值选股）+ 版本标注
- 占位扩展表移除 0.2.0 已完成项（valuation-relative / valuation-dcf / stock-selection / us-ipo-arbitrage）
- 路由规则补充新命题映射（"美股 IPO" / "成长股估值" / "从赛道筛 N 只"）
- 长度校准：从"800-1500 行"改为"400-600 行（实测）"

### 回归测试（新增）

- `docs/tests/finance-analysis-0.2.0.md`：5+ 用例覆盖 4 个新 framework + 跨 framework 组合

### 架构决策

- **长度校准**：_index.md 原规范"800-1500 行/framework"实测从未达到。0.2.0 统一到 400-600 行（与 0.1.0 现状一致），避免注水
- **us-ipo 提前**：原计划 0.5.0（加密 + 美股 IPO），本轮提前到 0.2.0（补齐估值/选股姐妹篇）
- **stock-selection 定位**：不重复 alpha-generation 的方法论，只做"可执行简化版"（4 步筛选器 + Top-N 清单）
- **valuation-card 双用**：一张 template 同时支持相对估值和 DCF，通过 §6 DCF 专用字段切换

### 关联

- 关联 backlog：`docs/backlog/2026-04-20-finance-analysis-skill.md`
- 关联 spec：`docs/specs/2026-04-23-finance-analysis-0.2.0-frameworks.md`
- 关联 plan：`docs/plans/2026-04-23-finance-analysis-0.2.0-plan.md`

---

## 0.1.0（开发中，待 merge 后确定版本号）

从群核科技（0068.HK）首日套利案例 + AI 主题投资 + 数据深度 + 自我迭代 系列讨论中沉淀的决策导向金融分析 skill。

### 定位

- **决策导向**（买/卖/持 + 目标价 + 止损），与 deep-research（研究导向）正交
- **命题驱动 + 手动触发**，skill 不做自动定时扫描
- **3 大核心价值**：数据深度 / 分析深度 / 透过表象+预判未来
- **能力两档**：Tier 1 基础（Claude Code 原生 WebSearch/WebFetch 能做 80%）+ Tier 2 增强（本地 PG + 量化栈，高阶 20%）

### Frameworks

- `command-driven-analysis.md`（主入口）：3 大核心价值 + 4 类命题（个股/政策/事件/主题）+ 执行检查单
- `hk-ipo-arbitrage.md`：港股 IPO 首日套利（群核 worked example + EV 计算）
- `alpha-generation.md`：10x 股 + 顶级 IPO 早期捕捉（5 执行差）
- `ai-thematic-investing.md`：AI 革命主题（8 层产业链 + 趋势启动识别 + 四层监控频率）
- `self-improvement-loop.md`：4 层闭环（决策留档/事后验证/错判归因/framework 升级）

### Templates

- `ipo-decision-card.md`：打新决策卡（T-1 填 T0 执行）
- `alpha-thesis-card.md`：个股 7 问法投资论点卡
- `earnings-deep-dive.md`：财报深度解读（3 层拆解+4 维预判，体现"透过表象"核心能力）
- `ai-daily-checkup.md`：日度多源扫描（可选辅助）
- `ai-monthly-checkup.md`：月度 8 层系统扫描（可选辅助）

### Integrations

- `integrations/local-data-stack.md`：可选增强对接（CLI / psql / PG schema 建议）

### 0.1.4 升级：铁律 +1 澄清（2026-04-23 炬光 v2 反馈沉淀）

- **铁律 +1 升级：自检是内部动作，不对外**
  - 删除"报告末尾强制输出完成度评分卡"规则
  - 改为"对外报告只呈现事实性数据局限，不呈现作者的方法论打分 / 迭代痕迹 / 版本号"
  - 新增红线：版本号（v1/v2）、"补第一版缺失"、"修正版"、自检评分表、方法论标签（"铁律 +1 维度 3"）暴露给用户 = 重做
  - 核心理念：脚手架（自检 / 方法论）不进房（对外报告）；读者看到的只有结论+数据+局限，不是作者的自我打分
  - 相关通用准则沉淀到 memory feedback_single-final-version-no-iteration-trace.md

### 0.1.3 新增：铁律 +1（2026-04-22 炬光科技自评反馈沉淀）

- **铁律 +1：报告完成前必须自检 + 改进（写完 ≠ 完成）**
  - 任何报告输出前必须经过 8 维度自检：方法论 / 数据深度 / 估值工具匹配 / 逻辑一致性 / 时机判断 / 技术+筹码面 / 反面证据 / 模板思维残留
  - 问题分档：致命（必修复）/ 重要（修复或标注）/ 次要（数据局限披露）
  - 报告末尾强制输出"完成度评分卡"（6 维度分 + 综合分 + 未修复项 + 存疑）
  - 血泪案例：炬光科技首版报告方法论到位但时机错、估值工具错、核心数字薄弱、同业对标缺失、模板思维残留——都应该在输出前就发现
  - 核心理念：LLM 天然倾向"完成任务"，金融报告的价值在"经得起挑战"不在"结构完整"

### 0.1.2 新增：铁律 0 升级（2026-04-22 炬光科技压测沉淀）

- **铁律 0 升级：全量数据时点校准（不只是股价）**
  - 从"抓当前股价"扩展为"校准四类数据时点"：股价 + 财务数据 + 分析师数据 + 订单/客户信息
  - 新规则：财务数据最新季报优先于过时年报（绝不用隔年年报）
  - 新规则：高波动期（股价 3 月内 ±30%+）聚合目标价必失效
  - 新规则：订单客户信息以最新调研纪要为准，不用年报"前五大客户"
  - 新产出格式：报告首段强制输出"数据时点校准块"
  - 血泪案例：炬光科技 2024 年报 + ¥65.40 聚合目标价双错，导致"6 倍极端高估"假分歧结论

### 0.1.1 新增：铁律 -0.6（2026-04-22 东山精密压测沉淀）

- **铁律 -0.6：不熟悉标的必须先做全业务线 × 主题映射矩阵**
  - 5 步强制流程：业务线矩阵穷举 / 每条线 × 主题映射 / 子公司穿透三问 / 同业反向映射 / 券商分歧 > 1.5x 必拆
  - 位置：插入在铁律 -0.5（估值重塑归因）之前，作为归因的前置
  - 血泪案例：东山精密分析漏掉 Multek 子公司是英伟达 GB200/H200 背板核心供应商，把"传统 PCB"归为主业平淡，错误结论"透支 30-85%"；真实按双 Alpha 引擎（Multek AI PCB + 索尔思光模块）Forward PE 42x 接近公允
  - 本质：修复"不熟悉标的时业务线枚举不完整"的系统性风险——靠直觉和用户提醒不行，必须靠强制流程

### 核心洞察（本轮讨论沉淀）

- Alpha 在执行不在发现：明牌是常态，差的是 5 执行差（精度/时点/仓位/持有/顶点）
- IPO 首日套利 vs 长期估值是两套方法论
- AI 8 层产业链 + 多 Layer 卡位（群核 Layer 6+7 = 37x PS 溢价的真实来源）
- 数据深度：SEC/HKEXnews/API > 新闻摘要 > 社区观点
- 分析深度：自己算自己推，不做观点复读机
- 透过表象：3 层信息（表层 / 中层 / **里层 = Alpha 所在**）
- 可证伪的前瞻预判：T+3 / T+6 / T+12 / T+24
- Skill 战斗力在方法论 + 读财报 + 独立推演，不依赖量化栈
- 没有 4 层自我迭代闭环，skill 永远不会变强

### 关联

- deep-research skill 信源复用：`skills/deep-research/references/sources/finance.yaml` + `blacklist.yaml`
- RSS 数据源扩展（可选）：`~/workspace/rss/` 的 2026-04-20 金融源扩展 backlog
