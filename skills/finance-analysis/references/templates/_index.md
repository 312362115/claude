# Templates 索引

> 可直接填的决策卡 / 监控表模板。

## 核心决策 templates（0.1.0）

| Template | 关联 Framework | 用途 |
|----------|--------------|------|
| [ipo-decision-card.md](./ipo-decision-card.md) | hk-ipo-arbitrage | **打新决策卡**（T-1 晚填，T0 执行） |
| [alpha-thesis-card.md](./alpha-thesis-card.md) | alpha-generation + command-driven-analysis | **个股投资论点卡**（7 问法 + bear case + 证伪条件） |

## 辅助执行 templates（0.1.0，可选）

> ⚠️ 这些是执行节奏辅助，skill 不主动触发。用户想用定时器自己配。

| Template | 关联 Framework | 用途 |
|----------|--------------|------|
| [ai-daily-checkup.md](./ai-daily-checkup.md) | ai-thematic-investing | 日度多源扫描 + 警报触发（可选） |
| [ai-monthly-checkup.md](./ai-monthly-checkup.md) | ai-thematic-investing | 月度 8 层系统扫描（可选） |

## 占位扩展（TODO）

| Template | 关联 Framework | 版本目标 |
|----------|--------------|---------|
| earnings-deep-dive.md | alpha-generation + command-driven 套路 C | 0.2.0 — 10-Q 深度解读（透过表象找里层信号） |
| policy-impact-map.md | command-driven 套路 B | 0.2.0 — 政策影响地图 |
| industry-chain-mapping.md | ai-thematic-investing | 0.2.0 — 产业链推演图（≥ 2 跳） |
| ipo-watchlist.md | alpha-generation | 0.2.0 — 顶级 IPO 监控清单 |
| stock-pitch.md | stock-selection（待落地） | 0.3.0 — 个股 Buy/Sell 提案 |
| ipo-post-mortem.md | hk-ipo-arbitrage | 0.2.0 — 打新事后复盘 |

## 使用方式

1. 调用 skill 时，Lead 根据命题加载对应 framework + template
2. 填写 template 到 `docs/research/YYYY-MM-DD-<subject>-<type>.md`
3. 执行决策
4. 事后补复盘段，归档到 `docs/decisions/`

## 输出格式铁律

所有 template 最终输出决策卡，必须包含：
- **动作**：买 / 卖 / 持 / 观望
- **目标价** + **止损价** + **仓位**
- **时间维度**：日内 / 短期 / 中期 / 长期
- **EV 或评分计算**
- **执行计划**（具体动作 + 触发条件）
- **风险提示 + 免责**
