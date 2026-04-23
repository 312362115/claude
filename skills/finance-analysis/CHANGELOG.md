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
