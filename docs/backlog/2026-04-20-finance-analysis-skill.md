---
priority: P1
status: in-progress
spec: docs/specs/2026-04-23-finance-analysis-0.2.0-frameworks.md
plan: docs/plans/2026-04-23-finance-analysis-0.2.0-plan.md
---

# finance-analysis skill（金融分析技能）

## 背景

2026-04-20 从群核科技（0068.HK）首日套利案例 + AI 主题投资讨论中沉淀。原本尝试把金融决策塞进 deep-research，发现方法论根本不同：

| 维度 | deep-research | finance-analysis |
|------|--------------|------------------|
| 核心问题 | "这件事什么情况" | **"买/卖/持？什么价？"** |
| 方法 | 假设-验证-交叉 | **决策树 + EV + 概率纪律** |
| 输出 | 研究报告 | **决策卡 + 目标价 + 止损** |

新建独立 skill 更合理。

## 核心洞察（本次会话沉淀）

从用户的 5 次关键反问中提炼出 **Alpha 执行差**方法论：

1. **精度差**：明牌所有人都有，精细明牌（推 2+ 跳）才是 Alpha
2. **时点差**：苗头期 vs 共识期，窗口只有 6-12 月
3. **仓位差**：明牌敢重仓是真功夫
4. **持有期差**：拿住比买对难 10 倍
5. **顶点识别差**：共识顶 = 卖点

**Alpha 不在发现，在执行**。

## 已落地（0.1.0）

### Skill 骨架
- `SKILL.md`（frontmatter + 触发词 + 决策路由）
- `VERSION` / `CHANGELOG.md`

### Frameworks
- `hk-ipo-arbitrage.md`：港股打新套利（含群核 worked example + EV 计算）
- `alpha-generation.md`：10x 股 + 顶级 IPO 早期捕捉（Alpha 执行差 5 要素）
- `ai-thematic-investing.md`：AI 革命主题投资（8 层产业链 + 趋势启动识别系统 + 月度巡检 90 分钟 checklist）

### Templates
- `ipo-decision-card.md`：打新决策卡
- `_index.md`（frameworks / templates 双路由表）

### 关键设计决策
- 不走 Multi-Agent（金融决策时敏，Lead 直接处理）
- 信源复用 deep-research 的 finance.yaml + blacklist.yaml
- 与 deep-research 的协作：deep-research 出研究报告 → finance-analysis 提取信号 → 决策卡

## 版本路线图

| 版本 | 内容 | 状态 |
|------|------|------|
| 0.1.0 | HK IPO + Alpha Generation + AI 主题 framework | ✅ 本版 |
| 0.2.0 | 估值（相对 + DCF）+ 选股 + 美股 IPO framework | 🚧 进行中（2026-04-23 启动） |
| 0.3.0 | 基金分析 + 债券分析 | 待做 |
| 0.4.0 | 技术面 + 事件驱动 + 宏观择时 | 待做 |
| 0.5.0 | 加密主题 | 待做 |
| 1.0.0 | 所有核心 framework 稳定 + 回归测试集 | 里程碑 |

## 关联资产

### 配对 RSS 数据源（~/workspace/rss）
- rss-daily 仓库已有 AI/币圈/科技源
- 新 backlog：`docs/backlog/2026-04-20-finance-sources-expansion.md`
  - 扩展金融一手源（SEC/HKEX/IR/VC 研报/大公司技术突破）
  - 通过 `daily/YYYY/MM/DD.md` 作为契约被 skill 消费
  - 实现 "日频 Alpha 扫描器"（rss 抓数据 + skill 做决策）

### 关键案例存档
- 群核科技 0068.HK 首日 +144% 完整复盘 → 沉淀进 hk-ipo-arbitrage worked example
- 2023-2024 存储股 HBM 大周期 → 沉淀进 alpha-generation 时点差案例

## 剩余待做

### 近期（0.2.0 节奏）— 2026-04-23 完成 ✅
- [x] `frameworks/valuation-relative.md`（相对估值 PE/PS/PB 对标）— 2026-04-23
- [x] `frameworks/valuation-dcf.md`（DCF 估值 + 情景分析 + 概率加权）— 2026-04-23
- [x] `frameworks/stock-selection.md`（alpha-generation 可执行简化版，4 步筛选器）— 2026-04-23
- [x] `frameworks/us-ipo-arbitrage.md`（美股 IPO，对照港股）— 2026-04-23
- [x] `templates/valuation-card.md`（估值卡，覆盖相对估值 + DCF 三情景）— 2026-04-23
- [x] `templates/stock-screening-card.md`（选股筛选卡）— 2026-04-23
- [x] `docs/tests/finance-analysis-0.2.0.md`（回归用例，7 条）— 2026-04-23
- [x] `templates/alpha-thesis-card.md`（Alpha 论点卡）— 0.1.0 已落地
- [x] `templates/ai-monthly-checkup.md`（月度巡检可填版）— 0.1.0 已落地
- [x] `templates/earnings-deep-dive.md`（10-Q 深度解读）— 0.1.0 已落地

### 中期（0.3.0-0.4.0）
- 基金 / 债券 / 技术面 / 事件驱动 frameworks 逐个落地

### 实战验证（等待触发）
- 下次打新机会 → 用 `ipo-decision-card.md` 实战跑一遍
- 下次重大财报 → 用 earnings-deep-dive（待落地）跑一遍
- 3 个月后回看：AI 月度巡检是否识别到了新趋势启动

## 进度

- **2026-04-20**：完成 0.1.0 骨架
  - 3 份 framework（hk-ipo-arbitrage / alpha-generation / ai-thematic-investing）
  - 1 份 template（ipo-decision-card）
  - 2 份 _index（frameworks / templates）
  - SKILL.md + VERSION + CHANGELOG
  - 本次迭代触发来源：群核科技 0068.HK 2026-04-17 上市 + 用户关于 "Alpha 本质" 的 5 次反问
- **2026-04-20 → 2026-04-22**：0.1.0 追加沉淀（未发版）
  - 新增 4 条 framework（alpha-thesis-card / earnings-deep-dive / ai-daily-checkup / ai-monthly-checkup）+ self-improvement-loop + command-driven-analysis 主入口
  - command-driven-analysis 补入 3 大核心价值 + 4 类命题路由 + 递归下钻 + 股市预期驱动 + 时间维度可预测性 + 4 条铁律
  - 触发来源：东山精密 / NVDA / TSLA / CATL 系列压测反馈
- **2026-04-23**：启动 0.2.0（本轮）
  - 已对焦：4 个 framework（valuation-relative / stock-selection / valuation-dcf / us-ipo-arbitrage），单个 400-600 行
  - us-ipo 由原 0.5.0 提前到 0.2.0（_index.md 设计，同步修正本 backlog 路线图）
  - 下一步：出 spec + plan → 用户 review → 动手
