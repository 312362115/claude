# Frameworks 路由表

> SKILL.md 触发后，先进 **command-driven-analysis.md** 主流程识别命题类型，然后调用对应辅助 framework。

## 主入口（必读）

| Framework | 定位 |
|-----------|------|
| **[command-driven-analysis.md](./command-driven-analysis.md)** | **主入口**。定义 3 大核心价值（数据深度/分析深度/透过表象预判未来）+ 4 类命题（个股/政策/事件/主题）+ 执行检查单 |

## 辅助 framework（0.1.0-0.2.0）

### 核心分析 / 决策

| Framework | 适用场景 | 被谁调用 | 版本 |
|-----------|---------|---------|------|
| [hk-ipo-arbitrage.md](./hk-ipo-arbitrage.md) | 港股 IPO 首日套利 | 套路 A 涉及打新时 | 0.1.0 |
| [us-ipo-arbitrage.md](./us-ipo-arbitrage.md) | 美股 IPO（三路径 EV 比较 / Lockup 抛压） | 套路 A + 套路 C 美股 IPO 命题 | 0.2.0 |
| [alpha-generation.md](./alpha-generation.md) | 10x 股 + 顶级 IPO 早期捕捉（5 执行差） | 套路 A 长期持有 / 套路 D 主题 | 0.1.0 |
| [ai-thematic-investing.md](./ai-thematic-investing.md) | AI 革命主题（8 层产业链 + 趋势启动识别） | 套路 D 主题 / 套路 A AI 标的 | 0.1.0 |
| [self-improvement-loop.md](./self-improvement-loop.md) | skill 自我迭代 4 层闭环（决策留档/验证/归因/升级） | 每次分析后 / "复盘"触发词 | 0.1.0 |

### 估值 / 选股

| Framework | 适用场景 | 被谁调用 | 版本 |
|-----------|---------|---------|------|
| [valuation-relative.md](./valuation-relative.md) | 相对估值（三情景 + 概率加权 + 主题溢价 + 隐含预期位置） | 套路 A 估值命题（PE/PS/PB 对标） | 0.2.0 |
| [valuation-dcf.md](./valuation-dcf.md) | DCF 估值（三情景 + 敏感性 + 交叉验证） | 套路 A 成长股 / 独家商业模型 | 0.2.0 |
| [stock-selection.md](./stock-selection.md) | **自下而上**：选股筛选（4 步筛 + 30/60/100 打分 + Top-N 清单） | 套路 D 主题 → Top-N 清单 | 0.2.0 |
| [top-down-selection.md](./top-down-selection.md) | **自上而下**：宏观→行业→板块→赛道池（Fed 预期 + 周期阶段 + 五年规划） | 宏观命题 / 板块配置 / 行业轮动 | 0.3.0 |
| [fund-analysis.md](./fund-analysis.md) | **基金 / ETF 分析**：管理人 + α/β + 夏普 / 回撤 + 持仓归因 + 费率流动性 | 选基金 / ETF 对比 / 组合配置 | 0.3.0 |
| [bond-analysis.md](./bond-analysis.md) | **债券分析**：久期 + 信用 + 利差三维 + 可转债（股性/债底/溢价）+ TLT 等债券 ETF | 债券配置 / 债基选择 / 固收决策 | 0.3.0 |

## Integrations

| Integration | 定位 |
|-------------|------|
| [../integrations/local-data-stack.md](../integrations/local-data-stack.md) | 可选增强：对接本地 PG + Python 量化栈（Tier 2 能力） |

## 占位扩展（TODO，按需迭代）

### 事件 / 技术面
| Framework | 场景 | 版本目标 |
|-----------|------|---------|
| event-driven.md | 财报 / 政策 / 并购事件交易 | 0.4.0 |
| technical.md | 技术面（支撑压力 / 趋势 / 量价） | 0.4.0 |

### 宏观 / 加密
| Framework | 场景 | 版本目标 |
|-----------|------|---------|
| macro-overlay.md | 宏观择时（利率 / 汇率 / 大宗） | 0.4.0 |
| crypto-thematic.md | 加密货币主题投资 | 0.5.0 |

## 路由规则

Lead agent 接到命题时：

1. **匹配关键词** → 加载对应 framework
2. **跨 framework 组合**（一个命题可能触发多个）：
   - "港股打新 + 中长期持有" → `hk-ipo-arbitrage` + `alpha-generation`
   - "AI 选股 + 估值分析" → `stock-selection` + `valuation-relative` + `ai-thematic-investing`
   - "美股 IPO 分析"（如 DoorDash / Coinbase）→ `us-ipo-arbitrage` + `valuation-dcf`
   - "成长股估值"（如 NVDA）→ `valuation-dcf` + `valuation-relative`（交叉验证）
   - "MiniMax / Zhipu IPO 分析" → `hk-ipo-arbitrage` + `alpha-generation` + `ai-thematic-investing`
   - "从 XX 赛道筛 N 只" → `stock-selection` → 每只 `valuation-relative` / `valuation-dcf`
   - **"哪些行业值得投 / 宏观配置"** → `top-down-selection`（主）→ 推荐赛道池 → `stock-selection`
   - **"降息预期下怎么配板块"** → `top-down-selection`（§4.1.2 加息降息预期）
   - **"十五五规划利好哪些赛道"** → `top-down-selection`（§4.5.1 中长期结构性政策）
   - **"主题 + 宏观叠加判断"** → `top-down-selection` + `ai-thematic-investing`（基础锚 + 主题超配）
   - **"基金 / ETF 选哪只"** → `fund-analysis`（主）+ `top-down-selection`（赛道锚）
   - **"TLT / 国债 / 债券能买吗"** → `bond-analysis` + `top-down-selection`（利率预期）
   - **"可转债分析"** → `bond-analysis` §7 + `valuation-relative`（正股估值）
   - **"复盘 / 命中率 / 归因"** → 套路 E（不走命题分析，见 SKILL.md）
3. **未匹配**（框架缺失）→ fallback 到 `alpha-generation.md` 的通用方法论

## Framework 写作规范（新增 framework 时遵循）

每个 framework 必须包含：

1. **核心定位**：适用 / 不适用场景
2. **决策树**：末端是可执行动作，不是"完整理解"
3. **量化信号**：每个节点是可观测阈值（不是主观判断）
4. **EV 或评分计算**：至少有一个数学模型
5. **执行纪律**：最容易翻车的环节写清楚
6. **Worked Example**：至少 1 个真实案例验证
7. **失效场景**：何时这套方法不适用
8. **相关 template**：决策卡 / 监控表指向 `templates/`
9. **诚实 disclaimer**：方法论不等于预测

**长度**：一个 framework 一般 400-600 行（过短不深入，过长读者退出）。0.1.0 / 0.2.0 实测均在此区间。

## 已落地版本

- **0.1.0**：command-driven-analysis（主入口，承接所有认知基础）+ hk-ipo-arbitrage / alpha-generation / ai-thematic-investing / self-improvement-loop
- **0.2.0**：valuation-relative / valuation-dcf / stock-selection / us-ipo-arbitrage（估值 + 选股 + 美股 IPO 补全）
- **0.3.0**：top-down-selection + fund-analysis + bond-analysis（自上而下 / 基金 / 债券三块补齐）+ self-improvement-loop Phase 2（decision-postmortem + quarterly-performance 模板 + 套路 E 路由 + INDEX 守护检查）

**不做**：
- 日内技术分析（和决策导向定位不符）
- 期权策略（本 skill 专注股票/债券/基金/IPO）
- SPAC DeSPAC（规则完全不同，退 event-driven 0.4.0）
