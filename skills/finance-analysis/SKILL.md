---
name: finance-analysis
version: 0.1.0
last_updated: 2026-04-20
repository: https://github.com/312362115/claude
changelog: skills/finance-analysis/CHANGELOG.md
description: >
  金融分析技能：股票 / 基金 / 债券 / IPO 打新 等投资决策场景的结构化分析。
  核心定位：决策导向（买/卖/持 + 目标价 + 止损），区别于 deep-research 的研究导向。
  核心方法论：决策树 + EV 计算 + 概率纪律，不是假设-验证-交叉。
  首版覆盖：HK IPO 打新套利（群核案例沉淀）；估值/选股/基金/债券/技术面/事件驱动
  作为 framework 占位扩展。
  信源复用：引用 deep-research 的 finance.yaml + blacklist.yaml。
  触发词：打新、IPO 分析、选股、选基金、买入、卖出、止损、
  估值分析、DCF、PE/PS 对比、这股票怎么样、这基金值得买吗、
  财报解读、仓位建议、港股打新、美股 IPO、孖展杠杆、
  首日套利、暗盘。
  即使用户没有明确说"投资"或"金融"，只要意图是
  "在金融资产上做买卖持有决策"，都应触发此技能。
---

# 金融分析（Finance Analysis）

> 不研究"这家公司是什么"，研究"要不要买、什么价买、什么时候卖"。
> 决策驱动 + 量化纪律 + 概率视角。

---

## 核心定位

| 维度 | deep-research | **finance-analysis** |
|------|--------------|---------------------|
| 核心问题 | "这件事什么情况" | **"买/卖/持？什么价？什么时机？"** |
| 方法 | 假设-验证-交叉 | **决策树 + EV 计算 + 概率纪律** |
| 时间 | 较长（一次性） | **盘中/盘前时敏** |
| 输出 | 研究报告 | **决策卡 + 目标价 + 止损 + 仓位** |
| 关键约束 | 信息充分性 | **执行纪律** |

**核心洞察**（从群核 0068.HK 首日 +144% 复盘）：金融决策的胜率不取决于"你知道多少"，取决于"你能不能按量化规则执行"。大多数"预期差"是**纪律差**，不是信息差。

---

## 决策路由（第一步：识别场景）

根据用户命题关键词，路由到对应 framework：

| 关键词 | Framework | 核心产出 |
|-------|-----------|---------|
| 打新 / IPO / 申购 / 孖展 / 暗盘 | `frameworks/hk-ipo-arbitrage.md`（HK）<br>`frameworks/us-ipo-arbitrage.md`（US，TODO） | 打新决策卡 + EV |
| 估值 / 值多少 / PE / PS / DCF / 合理价 | `frameworks/valuation-relative.md`（TODO）<br>`frameworks/valuation-dcf.md`（TODO） | 估值区间 + 目标价 |
| 选股 / 股票怎么样 / 值得买吗 | `frameworks/stock-selection.md`（TODO） | Buy/Hold/Sell + 目标价 |
| 财报 / 业绩 / 季报 | `frameworks/event-driven.md`（TODO） | 事件窗口 + 方向建议 |
| 技术面 / 支撑 / 阻力 / 趋势 | `frameworks/technical.md`（TODO） | 关键价位 + 止损 |
| 基金 / 夏普 / 回撤 / 持仓分析 | `frameworks/fund-analysis.md`（TODO） | 选基 + 风险评估 |
| 债券 / 久期 / 利差 / 信用评级 | `frameworks/bond-analysis.md`（TODO） | 配置建议 |

详见 `references/frameworks/_index.md`。

---

## 信源加载（复用 deep-research）

**不重复造轮子**。金融分析的信源与 deep-research 共享：

- **白名单**：`skills/deep-research/references/sources/finance.yaml`（冷门权威：BIS / 中债登 / CFETS / HKEX SDI / CCASS / Tardis.dev / BaoStock / Finnhub 等）
- **黑名单**：`skills/deep-research/references/sources/blacklist.yaml`（hard 过滤：CSDN / 东财股吧 / 雪球 / 金色财经等）

金融分析独有的"实时行情 API"（Binance / Finnhub / Alpha Vantage / AKShare 等）在 framework 中按场景引用，不在本 skill 重复沉淀。

---

## 核心方法论三原则

### 原则 1：决策树优先于信息收集

金融决策的 KPI 是**行动**（买/卖/持 + 多少仓位 + 什么价），不是**"完整理解"**。每个 framework 必须以决策树开头，末端是可执行动作。

```
命题输入
↓
Framework 路由
↓
决策树（N 个节点，每个节点是可观测信号 + 阈值）
↓
输出决策卡（买/卖/持 + 目标价 + 止损 + 仓位）
```

### 原则 2：EV 计算压过"直觉"

任何决策都要算期望值：

```
EV = Σ (概率 × 收益) - 成本

打新 EV = 中签率 × 单手盈利 - 融资利息
估值 EV = (目标价 - 现价) × 实现概率 - 止损损失 × (1 - 概率)
```

**"感觉会涨"不是决策依据**，"杠杆 10 倍 × 中签率 3% × 单手赚 5490 HKD = EV +1600 HKD / 200 HKD 利息"才是。

### 原则 3：执行纪律胜过分析深度

金融回测和实盘共识：

- **纪律差 > 信息差**：同一个信号，不同人执行结果差 10x
- **执行节点预设**：决策卡必须写明"什么价位买"、"什么价位止损"、"什么信号退出"，不能盘中临时起意
- **不追高 / 不加仓亏损 / 不越线扛单**：3 条铁律，违反一次可能吃掉几个月收益

---

## 决策卡输出格式（所有 framework 通用）

所有 framework 最终输出一张**决策卡**，格式统一：

```markdown
# 决策卡：<标的> <日期>

## 核心决策
- **动作**：买入 | 卖出 | 持有 | 观望
- **目标价**：XX（上行目标，概率 XX%）
- **止损价**：XX（下行止损，严格执行）
- **仓位建议**：总仓位的 X%
- **时间维度**：日内 / 1-30 天 / 1-12 月 / >1 年

## 关键信号（上市前/盘前可见）
| 信号 | 数值 | 阈值 | 判断 |
|------|------|------|------|
| ... | ... | ... | ✅/❌/⚠️ |

## EV 计算
<具体数学>

## 执行计划
- T+0：具体动作
- T+N：触发条件 → 动作

## 风险提示
- 最大亏损场景：...
- 对冲方式：...（若有）

## 免责
本决策卡基于公开信息量化分析，不构成投资建议。最终决策需结合个人风险偏好和资金结构。
```

详见 `references/templates/`。

---

## Framework 加载方式

skill 触发后：

1. **路由**：从命题识别场景关键词 → 加载对应 framework
2. **信源**：加载 deep-research 的 finance.yaml + blacklist.yaml
3. **决策树**：按 framework 的决策树顺序评估信号
4. **输出**：填决策卡模板 → 给用户

**不走 Multi-Agent**：金融决策时敏，Lead 直接 WebSearch + 工具调用 + 决策卡输出。若需要深度公司调研（基本面 / 赛道 / 竞争格局），调用 deep-research skill 作为**前置步骤**，本 skill 负责"从研究结论到决策"的最后一公里。

---

## 与其他 skill 的协作边界

| Skill | 分工 |
|-------|------|
| deep-research | 广度研究、公司/行业/赛道理解、"这是什么" |
| **finance-analysis**（本 skill） | **决策、目标价、止损、仓位、执行纪律** |
| tech-evaluation | 技术选型（非金融） |
| writing | 最终写作（可被本 skill 调用产出长报告） |

典型协作流：
- 简单决策：直接本 skill → 决策卡
- 复杂决策：deep-research 出研究报告 → 本 skill 提取信号 → 决策卡
- 定期复盘：本 skill 决策后，结果记录入 `docs/decisions/` 形成经验库

---

## 版本路线图

| 版本 | 内容 | 状态 |
|------|------|------|
| 0.1.0 | HK IPO 打新 framework + 群核案例 + 决策卡 template | ✅ 本版 |
| 0.2.0 | 股票估值（相对估值 + DCF）+ 选股 framework | 待做 |
| 0.3.0 | 基金分析（夏普 / 最大回撤 / 持仓归因） | 待做 |
| 0.4.0 | 债券分析（久期 / 信用 / 利差） | 待做 |
| 0.5.0 | 技术面 + 事件驱动 | 待做 |
| 1.0.0 | 所有核心 framework 稳定 + 回归测试集 | 里程碑 |
