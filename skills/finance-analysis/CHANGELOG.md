# Changelog — finance-analysis

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
