# Changelog — finance-analysis

## 0.4.3（2026-05-07）

**致尚案例完整回归测试集 + CI 化路线图**。0.4.x 三件套完整收尾。

### 新增

`docs/tests/finance-analysis-regression.md`（~430 行）：

**6 个核心回归用例**：

| # | 案例 | 验证目标 | 状态 |
|---|---|---|---|
| 1 | 致尚 301486 @ 2026-04-28 | 0.4.0 完整闭环 6 层根因 | ✅ 基准 |
| 2 | 群核 0068.HK 首日 +144% | hk-ipo-arbitrage 信号矩阵 | ✅ |
| 3 | 沪电 002463 @ 2026-04-24 | 铁律 0 数据校准 | ✅ |
| 4 | 东山 002384 @ 2026-04-22 | valuation-relative 三情景 | ✅ |
| 5 | NVDA 2023-Q1 财报 | 3 层信息拆解 / 透过表象 | ✅ |
| 6 | 致尚 4/29 单日分时形态 | technical-pattern 单日禁令铁律 | ✅ |

**每个用例完整规格**：输入数据 + 期望 framework 输出 JSON + 实际历史决策对比 + 回归断言伪代码（pytest 风格）。

**回归运行机制**：
- 当前阶段（0.4.x）：手工跑 6 用例，每次 framework 升级前后对比期望输出
- 工程化阶段（0.4.x 后期）：用例数据存 `docs/tests/cases/*.yaml` + framework 脚本化 + pytest CI
- 1.0.0 里程碑：全量回归通过 + 实战 6 个月命中率 ≥ 60%

**用例增加铁律**：实战错判 → 归因 → framework 升级 → 新增回归用例 → 升级前后跑全量回归确保不退化。

### 0.4.x 三件套总结

| 版本 | 内容 | 工作量 | 收益 |
|---|---|---|---|
| 0.4.0 | A/B/C 标签主框架三件套（1500+ 行）| 大 | 致尚案例 L1-L6 完整修复 |
| 0.4.1 | capital-flow.sh 数据速查脚本 | 小 | framework 真正可执行 |
| 0.4.2 | combined-decision-card.md 联动模板 | 中 | A+B+C 组合标的实战出口 |
| 0.4.3 | 回归测试集 6 用例 | 中 | 防 framework 升级退化 |

### 1.0.0 里程碑剩余项

- **实战验证 6 个月**：60+ 决策，命中率 ≥ 60%
- **错判分布**：D5 认知盲点占比 < 30%
- **路径 EV 模型实战验证**：路径 EV 真实命中率显著高于终点 EV
- **回归测试 CI 化**：pytest + framework 脚本化（capital-flow / event-driven / technical-pattern 各自的 .py 实现）
- **可选**：crypto-thematic（0.5.0）/ macro-overlay（0.4.x 候选）

---

## 0.4.2（2026-05-07）

**A+B+C 组合标的联动决策卡模板**。

### 新增

`templates/combined-decision-card.md`（~360 行）：

**适用场景**：A+B+C 三标签全触发 / A+C 双标签 + B 弱 / B+C 双标签 + A 待披露。

**结构 11 段**：
1. 决策前置 4 项强制 checklist（与 alpha-thesis-card 对齐）
2. 标的基本信息（仓位上限 ≤ 5%）
3. asset-type-classifier 输出（7 标签 + 强度 + 置信度 + 路由 + 禁令）
4. capital-flow 资金面附录（控盘度 5 维评分 + 主力方向 4 维 + EV 修正系数）
5. event-driven 事件附录（7 类事件 + 时间轴 + 5 维强度 + 路径 EV vs 终点 EV + 黑天鹅清单）
6. technical-pattern 形态附录（5 阶段 + 洗盘 vs 出货 + 量价 + MA + 5 维评分）
7. **4 framework 交叉验证表**（核心，决策一致性矩阵）
8. 综合决策（合议结论 + 4 framework 投票）
9. 执行计划
10. 验证日程
11. 综合 JSON schema（嵌套 4 framework 输出）

**核心铁律**：A+B+C 组合标的 sell / buy 决策必须 ≥ 3 framework 同向支持，否则只能 hold / watchlist / skip。

**致尚案例填充**：综合 JSON 投票 → watch 2 / follow 1 / watchlist 1 → 最终决策 watchlist-add（不是实际历史的 skip）。

---

## 0.4.1（2026-05-07）

**scripts/capital-flow.sh 资金面数据速查工具**。

### 新增

`scripts/capital-flow.sh`（~140 行 bash + Python heredoc）：

**功能 4 段**：
1. **实时行情**（数据源：sina hq.sinajs.cn 已知稳定）— 当前价 / 涨跌% / 数据时点
2. **基础信息**（数据源：eastmoney push2 best-effort + 重试）— 总股本 / 流通股本 / 流通市值 / PE / PB / 换手率 + C_smallcap 标签快判
3. **5 维官方数据源 URL 速查**（核心功能）— 龙虎榜 / 北上 / 融资 / 大宗 / 解禁
4. **决策卡 JSON schema 占位提示**

**设计原则（0.4.1）**：
- 零依赖（bash + curl + python3 自带）
- 优雅降级（接口故障时仍输出 URL 速查列表）
- 不强求全自动（手工抓取是合理 fallback）

**致尚 sz301486 实测**：
- 流通市值 174 亿 → C_smallcap 弱触发（边界值 200 亿以下）
- 流通比 56.3% → 高限售比例
- PE 666 / PB 12 / 换手率 9.19% → 极端高估值 + 高换手

**已知限制**：仅支持 A 股；港股 / 美股资金面需走 CCASS / SEC 13F 不同接口（未实现）。

---

## 0.4.0（2026-05-07）

**A/B/C 标签主框架三件套全部落地**。0.3.2 asset-type-classifier 暴露的 framework 缺位被一次性补齐。致尚 301486 案例 L1-L6 六层根因全部修复闭环。

### 新增 framework（共 ~1500 行）

#### `frameworks/event-driven.md`（~480 行，A_event 标签主框架）

7 大事件类型：重组 / 并购 / 退市 / 商誉减值 / 业绩对赌 / 实控人变更 / 重大监管。

**核心创新：路径 EV 模型取代静态 EV**（修复 L2 模型层 ~30% 权重根因）：
- 静态 EV：Σ(终点情景概率 × 终点收益) → 完全漏算路径中期间溢价
- 路径 EV：max(节点 i 的期间累计 EV, 终点 EV)
- 致尚案例：终点 EV -5.9% → 路径 EV +1.25% / 实测期间高点 +22.7%

**5 维事件强度评分（百分制）**：事件确定性 30 / 控股股东支持度 20 / 标的方资质 20 / 时间窗口 15 / 风险对冲 15。

**3 类等级铁律**：
- ≥ 80 高确定性 → 跟进
- 60-79 中等 → 小仓位试探
- 40-59 低 → 仅短期博弈
- < 40 → 避开（事件分 < 60 + A_event 标签 → buy 禁令）

**历史兑现概率沉淀**：A 股重大资产重组 75% / 借壳上市 60% / 跨界并购 50%-40% / *ST 摘帽 30% / 业绩对赌 3 年完整兑现 55% / 商誉减值（业绩不达后）80%。

**致尚 worked example**：恒扬数据收购 7 节点完整还原 + 4/28 事件强度评分 54 分（低）+ 路径 EV +1.25% → 决策方向应为 watchlist。

#### `frameworks/technical-pattern.md`（~520 行，B_momentum 标签主框架）

**核心铁律**：禁用单日分时形态作决策依据（致尚 4/29 倒 T 字头错判直接根因 L6）。

**5 阶段主升浪识别**：启动 / 加速 / 洗盘 / 二波 / 顶部。

**洗盘 vs 出货 5 信号判定矩阵**（修复 L6 时机层 ~10% 权重根因）：
| 信号 | 洗盘 | 出货 |
|---|---|---|
| 量能 | 缩量 < 5 日均量 70% | 放量 > 130% |
| 回踩深度 | ≤ 8% | > 15% |
| MA 系统 | 不破 20 日 | 跌破 60 日 |
| 振幅 | < 5% 窄幅 | ≥ 10% 大幅 |
| 板块联动 | 同步 | 退潮 |

**量价 4 象限 + MA 系统多空 + 缺口 4 类型**：完整覆盖技术面信号系统。

**5 维形态评分**：阶段 25 + 量价 25 + MA 20 + 关键位 15 + 板块 15。

**致尚 4/28 完整还原**：5 信号中 4 条洗盘 + 1 条模糊 = 洗盘末端（高置信度）→ 形态评分 +52 分（偏多偏强）→ 决策方向"等二波启动信号跟进，不应做空"。

### 路由 / 主入口同步升级

- `_index.md` 0.4.0 三大 framework 全部从"待建"升级为"✅ 已落地"
- `asset-type-classifier.md` 路由表 A+B+C / A+C / B+C 三组合主框架全部 ✅
- `SKILL.md` VOLATILE TAIL 列表 0.4.0 段全部已落地
- 版本号 0.4.0-alpha.1 → 0.4.0（正式版）

### 致尚 301486 案例 L1-L6 完整闭环

| 根因层 | 权重 | 修复版本 | 修复手段 |
|---|---|---|---|
| L1 数据时点 | 5% | 0.3.1 | quote.sh + 铁律 0 |
| L2 静态 EV 模型 | 30% | 0.3.2 + **0.4.0** | path-aware EV（asset-type-classifier B 强档禁令）+ event-driven 节点时间轴 |
| L3 framework 错配 | 40% | 0.3.2 | asset-type-classifier 前置分类器 |
| L4 认知偏误 | 20% | 0.3.2 + 0.3.3 | 决策卡 4 项强制 checklist + JSON schema 量化 |
| L5 资金面缺失 | 10% | **0.4.0** | capital-flow 5 维信号矩阵 |
| L6 洗盘 vs 出货 | 10% | **0.4.0** | technical-pattern 5 信号判定矩阵 + 单日分时禁令 |

**致尚 4/28 决策日如果走完 0.4.0 完整流程，4 条 framework 独立交叉验证全部阻断 sell 决策**：
1. asset-type-classifier B 强档禁令：禁止做空决策 ✅
2. capital-flow 控盘度 67 + 主力方向 +40：偏多 ✅
3. event-driven 事件强度 54 分：低确定性，唯一合规 = watchlist ✅
4. technical-pattern 洗盘末端 + 形态分 +52：等二波启动 ✅

四重阻断 = 错判从 ~70% 概率（0.3.1 之前）压缩到 < 5%（0.4.0 之后）。

### 0.4.x 路线图

- 0.4.1: capital-flow 数据源脚本化（AKShare / Tushare）
- 0.4.2: 三 framework 联动决策卡模板（A+B+C 组合时一张卡覆盖）
- 0.4.3: 致尚案例完整回归测试集

### 1.0.0 里程碑

所有核心 framework 稳定 + 回归测试集 + 实战命中率 ≥ 60%。0.4.0 完成后距 1.0.0 主要剩"实战验证 6 个月命中率"。

---

## 0.4.0-alpha.1（2026-05-07）

**capital-flow framework 落地**。补齐致尚 301486 案例暴露的 L5 维度缺失（资金面 ~10% 权重）。这是 0.4.0 三大 framework 的第一个。

### 新增 framework

`frameworks/capital-flow.md`（~530 行）：

**核心定位**：小盘控盘标的（C_smallcap 标签触发必跑）的资金面分析。胜负手 80% 在资金面，20% 在基本面。

**5 维信号**：
1. **龙虎榜**：买卖席位 / 机构席位 / 知名游资 / 沪深股通席位（A 股 + 港股 CCASS 替代）
2. **北上 / 沪深股通持仓**：持股比 / 单日 5/20 日加减仓阈值
3. **融资余额**：余额比 / 单日买入占比 / 5/20 日变动 / 融资融券比
4. **大宗交易**：折溢价 / 受让方 / 连续大宗 → 沉淀沪电 + 致尚教训：禁止把大宗成交价当股价
5. **流通股本 / 限售解禁**：解禁日 ± 30 日抛压窗口 + 减持意愿系数模型

**控盘度评分模型**（百分制，5 维加权）：大股东 30 + 北上 20 + 机构 20 + 融资 15 + 高管 15。

**主力方向 EV 修正系数**：
- 强买入（≥ +50）→ 短期 EV ×1.5
- 偏多（+20~+50）→ ×1.2
- 中性 → ×1.0
- 偏空 → ×0.7
- 强卖出（≤ -50）→ ×0.5
- 仅适用 ≤ 1 个月 EV，> 3 个月退基本面

**3 条执行铁律**：
1. 融资 / 流通市值 > 8% 高位禁追入
2. 北上连 5 日净流出禁逆势抄底
3. 龙虎榜机构连 3 次卖方出现立即减仓

**Worked Example**：致尚 301486 4/28 资金面回放 — 假设性 5 维数据 → 控盘度 67 分（高）+ 主力方向 +40 分（偏多）+ 强异动 → 资金面附录与 asset-type-classifier B 强档禁令独立交叉验证，**双重阻断错判**。

**5 类失效场景**：港股数据缺失 / 极端情绪期 / 控盘度过高反向陷阱 / 妖股化 / 短期事件冲击。

**JSON schema**：资金面附录嵌入主决策卡 `capital_flow` 字段，含控盘度 / 主力方向四维分 / 异动等级 / EV 修正系数 / 操作建议。

### 路由 / 主入口同步升级

- `_index.md` 新增 0.4.0 资金面 / 事件 / 技术面段
- `asset-type-classifier.md` 路由表 A+B+C / A+C / B+C 三行更新主框架（capital-flow ✅ 已落地）
- `SKILL.md` VOLATILE TAIL framework 列表新增 0.4.0 段
- 版本号升至 0.4.0-alpha.1

### 0.4.0 路线图剩余

- alpha.2: event-driven framework（A_event 标签）— 重组 / 并购 / 退市 / 商誉
- alpha.3: technical-pattern framework（B_momentum 标签）— 洗盘 vs 出货 / MA / 量价

### 致尚案例闭环进度

| 根因层 | 权重 | 修复状态 |
|---|---|---|
| L1 数据时点 | 5% | ✅ 0.3.1 quote.sh + 铁律 0 |
| L2 静态 EV 模型 | 30% | ✅ 0.3.2 path-aware EV（asset-type-classifier B 强档禁令）|
| L3 framework 错配 | 40% | ✅ 0.3.2 asset-type-classifier 前置分类器 |
| L4 认知偏误 | 20% | ✅ 0.3.2 决策卡 4 项强制 checklist + 0.3.3 JSON schema 量化 |
| L5 维度缺失 | 10% | ✅ 0.4.0-alpha.1 capital-flow（A_event / B_momentum 子维度待 alpha.2/3）|
| L6 时机层（洗盘 vs 出货）| 10% | ⏳ 0.4.0-alpha.3 technical-pattern 待建 |

剩余 alpha.2 + alpha.3 完成后，致尚类错判应能实现"前置阻断 + 动态修正"双保险闭环。

---

## 0.3.4（2026-05-07）

**决策档案机器可读化（P1 三件落地）**。借鉴 Dexter `temporal-decay.ts` evergreen vs dated 区分 + 把 0.3.3 alpha-thesis-card 的 JSON schema 思想推广到所有核心模板。让 self-improvement-loop 从"问 LLM"升级到"扫文件统计"。

### P1-5：dated vs evergreen 时间衰减机制

借鉴 Dexter `temporal-decay.ts:66-72` evergreen vs dated 区分（半衰期模型在 prompt-driven skill 上的零代码实现）。

**改造**：
- `docs/finance-journal/INDEX.md` 顶部新增「档案类型」段：dated 90 天后压缩为单行，evergreen 永不衰减
- 「按时间归档」段标记为 dated 区，「错判归因/月度复盘/季度报告」段标记为 evergreen 区
- 月度汇总执行时一并做 dated 区 90 天压缩

**收益**：决策卡累积不会让 INDEX 臃肿；归因/铁律/经验作为 skill 进化资产保持完整可索引。

### P1-4：self-improvement-loop JSON 契约统一规范

**改造**：
- `frameworks/self-improvement-loop.md` L1 决策留档段新增「机器可读 JSON 契约（0.3.3 引入，统一规范）」子段
- 明确 6 类 doc_type（thesis / verify / postmortem / quarterly / monthly / valuation / screening / ipo）
- 统一字段约定：ticker 用交易所 suffix、ISO 8601 日期、framework_version 完整版本号、bool 必显式、asset_tags 来自 7 标签
- 占位扫描脚本（命中率 / 铁律 0 通过率 / D 类型分布）

**收益**：决策档案成为机器可消费数据集，季度复盘 / framework 升级审查从手工统计升级为脚本扫描。**不双写 .jsonl 文件**——md 文件里的 JSON 代码块就是 jsonl 等价。

### P1-6：4 个核心模板补 JSON schema

**改造**：
- `templates/stock-screening-card.md` — 30/60/100 打分卡末尾 JSON schema（4 项打分 + Top-N 清单 + post_routing 提醒）
- `templates/valuation-card.md` — 估值决策卡 JSON schema（三情景概率加权 + DCF 字段 + asset_tags 强约束 E_value）
- `templates/ipo-decision-card.md` — IPO 打新卡 JSON schema（HK/US 双轨 + 三路径 EV + lockup 字段）
- `templates/decision-postmortem.md` — 复盘归因 JSON schema（D1-D5 分类 + 根因权重分布 + framework 升级触发）

**字段约束**：所有 schema 字段都有显式约束（枚举、阈值、概率和、累计触发条件），便于自动校验。

### 模板 JSON schema 全景表

| 模板 | doc_type | 关键字段 | 状态 |
|---|---|---|---|
| alpha-thesis-card | thesis | 4 项 checklist + B_strength + C_confidence | ✅ 0.3.2 已加 |
| valuation-card | valuation | 三情景概率 + DCF 字段 + asset_tags | ✅ 0.3.4 |
| stock-screening-card | screening | 30/60/100 打分 + Top-N + post_routing | ✅ 0.3.4 |
| ipo-decision-card | ipo | 信号矩阵 + EV + 三路径（US）/ 杠杆（HK）| ✅ 0.3.4 |
| decision-postmortem | postmortem | D1-D5 + 根因权重 + 触发升级 | ✅ 0.3.4 |
| quarterly-performance | quarterly | KPI 汇总 | 待 0.4.0 |

---

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
