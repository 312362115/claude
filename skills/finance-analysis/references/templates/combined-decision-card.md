# 组合决策卡（Combined Decision Card）

> **A + B + C 组合标签触发**（重组 + 主升浪 + 小盘）的标的专用决策卡。
>
> 一张卡覆盖 4 framework 输出：asset-type-classifier + capital-flow + event-driven + technical-pattern。
>
> **核心价值**：4 framework **独立交叉验证**——任一 framework 阻断 = 决策方向受限。**这是 0.4.0 致尚案例完整闭环的实战出口**。

---

## 何时使用本模板

**触发条件**（asset-type-classifier 输出满足以下任一）：
- ✅ A + B + C 三标签全触发（致尚画像）
- ✅ A + C 双标签 + B 弱档边缘
- ✅ B + C 双标签 + A 待披露

**不适用**：
- ❌ 仅单一标签触发 → 走对应 framework 单卡（alpha-thesis-card / valuation-card 等）
- ❌ E_value / F_cyclical 主导 → 走 valuation-relative + valuation-dcf
- ❌ D_ipo 锁仓期 → 走 hk/us-ipo-arbitrage

---

## 决策卡模板（copy 使用）

```markdown
# 组合决策卡：<Ticker> <名称>  YYYY-MM-DD

## 0. 决策前置 checklist（必须 4 项全过）

- [ ] **铁律 0：数据时点校准**
  - 跑 `scripts/quote.sh <code>` 抓实时股价
  - 跑 `scripts/capital-flow.sh <code>` 抓基础信息 + 5 维数据源
  - 当前价 ___ / 数据时点 ___ / 当日涨跌% ___

- [ ] **标的类型分类**（asset-type-classifier 输出）
  - 触发标签：[ ] A_event [ ] B_momentum [ ] C_smallcap
  - B 强度：[ ] 弱（2 信号）[ ] 中（3-4）[ ] **强（5-6）**
  - C 判定置信度：[ ] 强（C2 流通市值实测）[ ] 弱（仅 C1 总市值估算）
  - 标签组合画像：___（如"重组+主升浪+小盘"）

- [ ] **反向论证**（最强双向，各 ≥ 100 字）
  - 最强 Bull Case：___
  - 最强 Bear Case：___
  - 最弱一环：___

- [ ] **认知偏误自检**（任一 ✅ 必须停下重审）
  - [ ] 用基本面反推"市场错了"？
  - [ ] 用单日盘面 / 分时形态判断主力意图？（B 强档下高危）
  - [ ] 用静态 EV 评估事件驱动 / 主升浪标的？（A/B 标签下高危）
  - [ ] 用沉淀的"经验"做事后合理化？

---

## 1. 标的基本信息

- 代码：xxx.xx
- 当前价：xxx（YYYY-MM-DD HH:MM 实时）
- 总市值 / 流通市值：xxx 亿 / xxx 亿
- 流通比：xx%
- PE / PB / 换手率：xxx / xxx / xx%
- 行业 / 主题：xxx
- 计划持有期：xxx
- 仓位上限：x%（A+B+C 组合标的强建议 ≤ 5%）

---

## 2. asset-type-classifier 输出

### 2.1 7 标签扫描结果

| 标签 | 触发？ | 强度 / 置信度 | 关键数据 |
|---|---|---|---|
| A_event | ✅/❌ | — | 事件类型 + 时间窗口 |
| B_momentum | ✅/❌ | 弱/中/强（X/6） | 30 日累计涨幅 / 涨停次数 / 板块对比 |
| C_smallcap | ✅/❌ | 强/弱（C2/C1）| 流通市值 + 流通比 |
| D_ipo | ✅/❌ | — | 上市时间 |
| E_value | ✅/❌ | — | ROE / 营收稳态 |
| F_cyclical | ✅/❌ | — | 行业属性 |
| G_turnaround | ✅/❌ | — | 拐点信号 |

### 2.2 路由结果

- 主框架：capital-flow + event-driven + technical-pattern（三件套）
- 辅框架：ai-thematic-investing / alpha-generation
- 必看维度：资金面 / 技术面 / 事件节奏
- **强制禁令**：
  - B 强档 → 禁止做空决策
  - A 标签 → 禁止用静态 EV 做主决策
  - 静态估值（valuation-relative / DCF）仅作参考锚

---

## 3. capital-flow 资金面附录

### 3.1 控盘度评分（百分制，5 维加权）

| 维度 | 权重 | 实测 | 得分 |
|---|---|---|---|
| 大股东 + 一致行动人持股 | 30 | xx% | xx |
| 北上 / 沪深股通持股 | 20 | xx% | xx |
| 公募 / 私募 / 险资机构 | 20 | xx% | xx |
| 融资余额 / 流通市值 | 15 | xx% | xx |
| 高管 + 员工持股 | 15 | xx% | xx |
| **总分** | **100** | — | **xx** |

→ **控盘等级**：极高（≥80）/ 高（60-80）/ 中（40-60）/ 低（<40）

### 3.2 主力方向得分（4 维）

| 维度 | 得分 | 数据 |
|---|---|---|
| 龙虎榜（±30）| ±xx | 近 30 日上榜 X 次 / 机构席位净 ±X / 净买额 xx 万 |
| 北上（±25）| ±xx | 5/20 日累计 ±X% / 持股比 xx% |
| 融资（±25）| ±xx | 5 日变动 ±X% / 余额比 xx% |
| 大宗（±20）| ±xx | 折溢价 X% / 受让方类型 |
| **总分** | **±xx** | — |

→ **主力方向**：强买（≥+50）/ 偏多 / 中性 / 偏空 / 强卖（≤-50）

### 3.3 异动等级 + EV 修正

- 异动等级：强 / 中 / 弱 / 无
- EV 修正系数：×0.5 / ×0.7 / ×1.0 / ×1.2 / ×1.5（仅 ≤ 1 月 EV）
- **资金面操作建议**：buy / follow / observe / exit / skip

---

## 4. event-driven 事件附录

### 4.1 事件类型 + 时间轴

| 字段 | 内容 |
|---|---|
| 事件类型 | 重组 / 并购 / 退市 / 商誉 / 对赌 / 实控人 / 监管 |
| 当前节点 | 停牌 / 复牌 / 预案 / 受理 / 反馈 / 过会 / 完成 |
| 距下一节点 | xx 天 |
| 下一节点名 | xxx |

### 4.2 5 维事件强度评分

| 维度 | 权重 | 得分 |
|---|---|---|
| 事件确定性 | 30 | xx |
| 控股股东支持度 | 20 | xx |
| 标的方资质 | 20 | xx |
| 时间窗口 | 15 | xx |
| 风险对冲 | 15 | xx |
| **总分** | **100** | **xx** |

→ **事件强度**：高（≥80）/ 中（60-80）/ 低（40-60）/ 不确定（<40）

### 4.3 路径 EV vs 终点 EV

```
节点 1（如复牌）: P=xx% × 反应=±x% = ±x.x%
节点 2（如预案）: P=xx% × 反应=±x% = ±x.x%
...
节点 N（如完成）: P=xx% × 反应=±x% = ±x.x%

路径 EV（任意节点高点）: ±x.x%
终点 EV（最后节点）: ±x.x%
合并 EV = max(路径, 终点) = ±x.x%
```

### 4.4 黑天鹅清单（必查 6 项）

- [ ] 监管口风突变 / 窗口指导叫停
- [ ] 反竞争方案出现
- [ ] 标的方关键人员离职 / 失联
- [ ] 控股股东司法冻结 / 限制消费
- [ ] 财务造假 + 审计辞任
- [ ] 业绩对赌方主体注销 / 资产剥离

任一触发 → **立即清仓**。

→ **事件操作建议**：buy / watchlist / skip / sell

---

## 5. technical-pattern 形态附录

### 5.1 主升浪阶段定位

- 当前阶段：启动 / 加速 / **洗盘** / 二波 / 顶部
- 阶段时长：xx 天
- 距下一阶段切换信号：xxx

### 5.2 洗盘 vs 出货 5 信号判定

| 信号 | 洗盘特征 | 出货特征 | 实测 | 判定 |
|---|---|---|---|---|
| 量能 | 缩量 | 放量 | xx% | ✅/❌ |
| 回踩深度 | ≤8% | >15% | xx% | ✅/❌ |
| MA 系统 | 不破 20 日 | 跌破 60 日 | 当前位 | ✅/❌ |
| 振幅 | <5% | ≥10% | xx% | ✅/❌ |
| 板块联动 | 同步 | 退潮 | 同步 / 退潮 | ✅/❌ |

→ **判定**：洗盘 (X:Y) / 出货 (X:Y) / 模糊（3:2 等待下日确认）

### 5.3 量价 + MA + 关键位

- 量价配合：价升量增 / 价升量缩 / 价跌量增 / 价跌量缩
- MA 系统：多头排列 / 金叉 / 纠缠 / 死叉 / 空头排列
- 关键支撑：5 日 MA = xxx / 20 日 MA = xxx / 60 日 MA = xxx
- 关键压力：前期高点 = xxx / 缺口下沿 = xxx

### 5.4 5 维形态评分

| 维度 | 权重 | 得分 |
|---|---|---|
| 主升浪阶段定位 | 25 | ±xx |
| 量价配合 | 25 | ±xx |
| MA 系统 | 20 | ±xx |
| 关键技术位 | 15 | ±xx |
| 板块强度 | 15 | ±xx |
| **总分** | **100** | **±xx** |

→ **形态等级**：强多（≥+60）/ 偏多 / 中性 / 偏空 / 强空（≤-60）
→ **形态操作建议**：add / follow / hold / watch / trim / exit

---

## 6. 4 framework 交叉验证表 ⭐（核心）

| Framework | 输出方向 | 关键数据 | 与"sell"决策相容？ | 与"buy"决策相容？ |
|---|---|---|---|---|
| asset-type-classifier | A+B+C 博弈型 | B 强档 / C 弱判定 | ❌ B 强档禁令 | ⚠️ 需事件分 ≥60 |
| capital-flow | 偏多 +40 | 控盘 67 / 主力偏多 | ❌ 主力方向反向 | ⚠️ 需异动等级强 |
| event-driven | watchlist | 事件分 54（低）/ 路径 EV +1.25% | ❌ 路径 EV 正 | ❌ 事件分 < 60 |
| technical-pattern | 洗盘末端偏多 | 形态分 +52 / MA 多头 | ❌ 量价 / MA 反向 | ⚠️ 需突破压力位 |

### 决策一致性矩阵

| 数 framework 同向 | sell 决策 | buy 决策 | hold/watch | skip |
|---|---|---|---|---|
| 4 个全部支持 | ✅ 高置信 | ✅ 高置信 | — | — |
| 3 个支持 | ⚠️ 中置信 | ⚠️ 中置信 | — | — |
| 2 个支持 | ❌ 不允许 | ❌ 不允许 | ✅ | ✅ |
| 1 个或 0 | ❌ 不允许 | ❌ 不允许 | — | ✅ 默认 |

**铁律**：A+B+C 组合标的 sell / buy 决策**必须 ≥ 3 framework 同向支持**，否则只能 hold / watchlist / skip。

---

## 7. 综合决策（合议结论）

| 项 | 数值 |
|---|---|
| 4 framework 投票汇总 | sell: x / buy: x / hold: x / watch: x / skip: x |
| **最终决策** | **buy / hold / trim / sell / skip / watchlist-add** |
| 决策置信度 | 高（4 同向）/ 中（3 同向）/ 低（≤ 2 同向）|
| 上行目标 | xxx（基于路径 EV 高点）|
| 止损价 | xxx（基于 60 日 MA / 关键支撑）|
| 仓位建议 | x% |
| 持有期 | x 天 / 月 / 年 |

---

## 8. 执行计划

- T+0：xxx
- T+1 ~ T+5：xxx
- 加仓触发：xxx（具体信号 + 价位）
- 减仓触发：xxx（具体信号 + 价位）
- 清仓触发：xxx（黑天鹅 / 跌破 60 日 MA / 4 framework ≥ 3 个转向）

---

## 9. 验证日程

- [ ] T+3（YYYY-MM-DD）：4 framework 重新评估，重点看 [事件节点 / 主升浪阶段切换]
- [ ] T+6（YYYY-MM-DD）：[事件兑现 / 业绩 / 解禁等关键节点]
- [ ] T+12（YYYY-MM-DD）：[长期兑现验证]

---

## 10. 综合 JSON 输出（必填，0.4.0 引入）

```json
{
  "doc_type": "combined",
  "ticker": "301486.SZ",
  "decision_date": "2026-04-28",
  "decision_action": "watchlist-add",
  "framework_version": "finance-analysis 0.4.0",
  "asset_type_classifier": {
    "tags_triggered": ["A_event", "B_momentum", "C_smallcap"],
    "B_strength": "strong",
    "B_signals_hit": 5,
    "C_confidence": "weak",
    "asset_profile": "重组+主升浪+小盘",
    "main_framework": ["capital-flow", "event-driven", "technical-pattern"]
  },
  "capital_flow": {
    "circulation_market_cap_yi": 174,
    "control_score": 67,
    "control_level": "high",
    "main_direction_total": 40,
    "main_direction_label": "mod_buy",
    "anomaly_level": "strong",
    "ev_modifier": 1.2,
    "operation_recommendation": "follow"
  },
  "event_driven": {
    "event_type": "restructuring",
    "current_node": "feedback",
    "days_to_next_node": 91,
    "fulfillment_probability": 0.60,
    "event_strength_score": 54,
    "event_strength_tier": "low",
    "path_ev_pct": 1.25,
    "terminal_ev_pct": -5.9,
    "combined_ev_pct": 1.25,
    "black_swan_triggered": false,
    "operation_recommendation": "watchlist"
  },
  "technical_pattern": {
    "wave_stage": "washing",
    "washing_vs_distribution": {"verdict": "washing", "washing_signals_hit": 4, "confidence": "high"},
    "price_volume": "falling_quiet",
    "ma_system": "bull_alignment",
    "pattern_score": 52,
    "pattern_score_tier": "mod_bull",
    "intraday_pattern_used": false,
    "operation_recommendation": "watch"
  },
  "consensus": {
    "votes": {"sell": 0, "buy": 0, "hold": 1, "watch": 2, "follow": 1},
    "majority_action": "watchlist-add",
    "confidence": "medium",
    "frameworks_aligned": 3,
    "veto_triggered": ["B_strong_no_short", "event_score_below_60_no_buy"]
  },
  "checklist": {
    "data_calibration": {"passed": true},
    "asset_type_classifier": {"passed": true},
    "reverse_argumentation": {"passed": true},
    "cognitive_bias_check": {"passed": false, "any_high_risk_triggered": true}
  },
  "all_passed": false,
  "process_violation": false
}
```

---

## 11. 免责声明

本组合决策卡基于公开信息量化分析，4 framework 输出独立交叉验证。

**核心局限**：
- 即便 4 framework 全部同向，单次决策仍可能错（黑天鹅 / 数据滞后 / 监管突变）
- 4 framework 输出基于 0.4.0 版本，不同版本结论可能不同
- A+B+C 组合标的本质高方差，仓位建议 ≤ 5%

不构成投资建议。最终决策需结合个人风险偏好、资金结构、组合分散度。
```

---

## 致尚 4/28 完整填充示例（worked example）

按本模板回填致尚 301486 4/28 决策日的 4 framework 输出，**得到的最终决策应为 watchlist-add（不是 skip）**。

详见 `frameworks/asset-type-classifier.md` §5 Worked Example + `frameworks/capital-flow.md` §6 + `frameworks/event-driven.md` §7 + `frameworks/technical-pattern.md` §8 各自的致尚案例填充。

**核心数据**：
- 4 framework 全部产出 → 4 个独立 JSON
- 综合 JSON 投票：sell 0 / buy 0 / hold 1 / watch 2 / follow 1
- veto 触发：B 强档禁止做空 + 事件分 < 60 禁止 buy
- **最终决策：watchlist-add**（避开 4/28 实际做出的 skip 错判 + 后续 6 日 +22.7% 反向）

---

## 使用纪律

1. **填不满 4 framework 不作决策**：缺任一 framework = 跳到 watchlist 默认
2. **A+B+C 组合标的仓位上限 ≤ 5%**：高方差标的小仓位试探
3. **每周强制重判**：4 framework 状态可能快速变化（事件节点 / 主升浪阶段切换 / 资金流向逆转）
4. **决策卡归档到 `docs/finance-journal/`**：随 git 提交，不只存 memory
5. **复盘时按 4 framework 各自归因**：错判时定位是哪条 framework 出错（self-improvement-loop 套路 E）
