# Changelog — finance-analysis

## 0.3.3（2026-05-07）

**吸收 Dexter 工程化优点**。从 ~/workspace/dexter（virattt 的金融研究 agent）深度扫描借鉴 6 维度工程模式，挑出 3 个 P0 落地，避免破坏 skill 跨平台 / 零依赖能力。

### P0-1：Framework 顶部 When to/NOT to Use 对照表

借鉴 Dexter 的 tool description "When to Use / When NOT to Use / Usage Notes" 三段式（参见 `screen-stocks.ts:13-38`、`read-filings.ts:15-41`）。

**改造文件**：
- `frameworks/asset-type-classifier.md` — 顶部加 5 项使用边界（明确不覆盖基金 / 加密 / 期权 / 跨境套利 / 极端宏观危机）
- `frameworks/valuation-dcf.md` — 顶部对照表 6 项 NOT Use 强禁令（含 A_event / B_momentum 强档禁令）
- `frameworks/valuation-relative.md` — 顶部对照表 7 项 NOT Use（含 F_cyclical 必用 PB 不用 PE）
- `frameworks/stock-selection.md` — 顶部对照表 5 项 + 输出后强制路由（Top-N 后必须走 asset-type-classifier）

**核心机制**：framework 路由从"看完文档底部失效场景再判断"升级为"顶部对照表第一眼判断"，降低错配概率。

### P0-2：决策卡 checklist JSON 输出契约

借鉴 Dexter 的 Zod structured output 模式（`screen-stocks.ts:140-156`、`read-filings.ts:163-321`）+ schema 字段级 description。

**改造文件**：
- `templates/alpha-thesis-card.md` — checklist 段末尾新增「Checklist 机器可读输出」子段，每张决策卡末尾必填 JSON 代码块

**核心字段**：
- `checklist.data_calibration.{passed, quote_script_ran, price_recorded, data_timestamp, stale_data_used}`
- `checklist.asset_type_classifier.{tags_triggered, B_strength_level, C_confidence, asset_profile, main_framework, fallback_action}`
- `checklist.reverse_argumentation.{bull_case_words, bear_case_words, weakest_link}`
- `checklist.cognitive_bias_check.{narrative_reverse_check, intraday_pattern_check, static_ev_under_AB_check, post_hoc_rationalization_check}`
- `all_passed`、`process_violation`

**机制收益**：self-improvement-loop 从"问 LLM 它是否做了"升级到"扫文件统计真实通过率"。命中率统计、铁律 0 真实通过率、D 类型错判触发分布等指标全部脚本可算。

### P0-3：SKILL.md STABLE PREFIX / VOLATILE TAIL 分段

借鉴 Dexter 的 Anthropic prompt caching 设计（`llm.ts:200-213, 265-286`）—— 让前缀稳定 = 缓存命中。

**改造文件**：
- `SKILL.md` — 重排为两段式结构

**变更**：
1. **STABLE PREFIX**（前 70%）：灵魂 / 核心定位 / 决策前置 / 5 类命题路由 / 三原则 / 决策卡格式 / 加载方式 / 自我迭代 / 协作边界 / 信源 —— 永不变方法论
2. **VOLATILE TAIL**（后 30%）：辅助 framework 列表 / 能力两档 / 关于自动触发 / 版本路线图 —— 随版本升级而变
3. 中段新增「Framework 升级铁律」段，明确 4 条铁律：先升 STABLE 后升 VOLATILE / 禁止 query-specific 引入 STABLE / breaking 改动需 CHANGELOG 标注 / 决策卡只写 finance-journal 不进 SKILL.md

**机制收益**：Anthropic prompt cache 命中前缀，前缀稳定 = ~90% input token 节省。Claude Code 自动处理 cache，无需手工 cache_control 标记。

### 不抄清单（保护既有路线）

明确不吸收的 7 类 Dexter 设计（破坏跨平台 / 不适用 prompt-driven skill）：
1. SQLite + FTS5 + embedding hybrid search（破坏跨平台 + 引入运行时基础设施）
2. Multi-LLM provider factory（skill 不调 SDK，由 harness 决定）
3. Two-step planner / sub-LLM 调用（需要运行时 LLM 调度，prompt skill 没有）
4. Agent loop / microcompact / turn budget 工程概念（harness 责任，不应往 skill 文档塞）
5. Financial Datasets API 业务实现（美股 only，破坏 A股/港股能力）
6. Anthropic `cache_control` 手工标记（Claude Code 自动处理）
7. Buffett/Munger 长期价值哲学路线（与多 framework / 博弈型路线冲突）

### 0.4.0 路线图保持不变

capital-flow / event-driven / technical-pattern 三个 framework 仍是下一版核心。本版仅做工程化吸收。

---

## 0.3.2（2026-05-07）

**asset-type-classifier 前置分类器 + 决策卡强制 checklist**。沉淀于致尚科技 301486 血泪案例：用价值股 framework 切博弈型标的，4/28 决策 skip 后到 5/7 早盘 6 个交易日累计 +22.7%（同期创业板指 +5.4%，相对超额 +17.3pt），短期方向 100% 反向。

### 根因分析（6 层拆解）

| 层级 | 根因 | 影响 |
|---|---|---|
| L1 数据 | 决策日股价用过期数据（4/27 收盘代替 4/28 收盘） | <5% |
| L2 模型 | 静态 EV 模型缺路径分布（终点 EV ≠ 持有期 EV） | ~30% |
| **L3 框架** | **用价值股 framework（valuation-relative）切博弈型标的（重组+主升浪+小盘）** | **~40% 单一最大** |
| L4 认知 | 已沉淀的"叙事覆盖"铁律没进入决策卡强制流程，4/29 用分时倒 T 字头判主力出货 = 同一种"看穿大资金"幻觉换载体 | ~20% |
| L5 维度 | 完全没看资金面（龙虎榜/北上/融资） | ~10% |
| L6 时机 | 没识别"洗盘 vs 出货"（4/28 缩量阴线 = 洗盘末端，不是出货）| ~10% |

### 新增 framework

- **`frameworks/asset-type-classifier.md`**（前置分类器，决策前必跑）
  - 7 项标签：A_event / B_momentum / C_smallcap / D_ipo / E_value / F_cyclical / G_turnaround
  - 标签组合 → framework 路由表（A+B+C 等 10 种组合）
  - 必看维度 / 可降权维度对照表（5 类标的 × 9 项维度）
  - 致尚 301486 worked example（应识别为 A+B+C，实际错配走 E）
  - 标签更新机制（动态分类 + 转换触发器）
  - 0.4.0 待建 framework 占位（capital-flow / event-driven / technical-pattern）

### 决策卡模板升级

- **`templates/alpha-thesis-card.md`**：顶部新增 4 项强制 checklist
  1. **铁律 0：数据时点校准**（quote.sh 跑过 + 记录精确时点）
  2. **标的类型分类**（asset-type-classifier 输出 + 路由 framework）
  3. **反向论证**（最强 bull case + 最强 bear case 各 ≥ 100 字）
  4. **认知偏误自检**（4 项高危幻觉勾选）

未过 4 项 checklist 而出具的决策卡 = 流程违规决策。

### 路由 / 主入口升级

- `frameworks/_index.md` 新增 Step 0「强制前置：跑 asset-type-classifier」+ asset-type-classifier 加入主入口必读表
- `SKILL.md` 主入口新增「🚦 决策前置必跑」章节 + 0.3.2 版本路线图

### 0.3.2.1 补丁（同版内）— 致尚回归用例发现的两个改进

跑致尚 4/28 案例验证分类器时发现的小漏洞，立即补：

1. **B_momentum 强度分级**：原始仅"触发/不触发"二元判定。新增 6 项命中数 → 弱（2 项）/ 中（3-4 项）/ 强（5-6 项）三级。**B 强 → 静态估值彻底失效 + 禁止做空决策 + 决策卡顶部红字标注"高错配代价区"**
2. **C_smallcap 判定优先级**：明确 C2（流通市值）> C1（总市值）。仅用 C1 = 弱判定，应手工补查流通股本 / 龙虎榜 / 北上 / 融资余额。capital-flow framework 落地前给出手工抓取路径占位
3. **分类标签卡输出格式升级**：增加"强度判定明细"+"判定置信度"两栏

致尚 4/28 实测：B 命中 4/6 = 中等偏强 + C 判定为弱（只读了 C1）→ 决策卡顶部应红字标注高错配代价区，**短期 6 日 +22.7% 偏差与该强度等级匹配**。

### 0.4.0 路线图（本次错判暴露的 framework 缺口）

| Framework | 适用 | 优先级 |
|---|---|---|
| capital-flow.md | C 标签（小盘资金面）| P0 |
| event-driven.md | A 标签（事件节奏）| P0 |
| technical-pattern.md | B 标签（洗盘 vs 出货）| P0 |

---

## 0.3.1（2026-04-24）

**铁律 0 再次升级 + 行情抓取脚本落地**。沉淀于沪电血泪案例：WebSearch 研报片段里的股价是历史价，不是当前价，必须走实时行情接口。

### 铁律 0 升级（command-driven-analysis.md）

- **新增核心原则**：每个数据引用都必须先确认时点——查不出日期 = 禁用。特别是股价，禁止从 WebSearch 研报/新闻片段中二次转引。
- **股价抓取源重排**：新增 P0 `scripts/quote.sh`（封装新浪实时行情），A/港/美股通用、带日期时间戳、零依赖免 API key。WebSearch 行情快讯降到 P3，研报片段中的股价改为 ❌ 禁用。
- **红线新增 2 条**：
  - 引用数字前未确认"这是哪一天的" = 违反铁律 0 = 重做
  - 从 WebSearch 研报/新闻片段里提取股价当当前价用 = 违反铁律 0 = 重做

### 新增 scripts/

- `scripts/quote.sh`：批量实时行情抓取脚本（bash，依赖 curl + iconv）。支持 sz/sh（A 股）、rt_hk（港股）、gb_（美股），输出结构化表格（代码 / 名称 / 当前价 / 涨跌% / 数据时点 / 状态），自动判断数据新鲜度（当日 / N 天前收盘 / 陈旧）。

### 血泪案例（沪电股份 2026-04-24）

- AI 板块扫描首版报告把 WebSearch 返回的"沪电股份 ¥81.18"片段当当前价用
- 实际片段是 2-3 月研报引用价，**真实 4-23 收盘价 ¥106.62**（+31% 偏差）
- Forward PE 误算 30x（真实 40x），错误结论"Top 1 建仓推荐"
- 根因：没有对每个数据做"这是哪一天的"独立校验 → 直接引用 WebSearch 片段
- 修复：铁律强化 + quote.sh 落地 + memory 升级

### 关联

- feedback memory：`feedback_full-data-timepoint-calibration.md` 升级（含沪电案例 + scripts/quote.sh 使用）

---

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
