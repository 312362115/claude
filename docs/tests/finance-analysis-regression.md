# finance-analysis 回归测试集

> 用真实金融案例验证 framework 升级不退化。每次 framework 升级（0.4.x / 0.5.0 / 1.0.0）必须跑全量回归。
>
> **核心案例**：致尚科技 301486 — 0.3.0-0.3.1 错判（skip 后 6 日 +22.7%）→ 0.4.0 完整 6 层闭环修复。
>
> **回归原则**：每个用例给出"输入数据 + 期望 framework 输出 + 实际 framework 输出"，CI 化前先手工跑。

---

## 用例 1：致尚科技 301486 @ 2026-04-28（基准测试用例）

### 1.1 输入数据（决策日 4/28 实测）

| 维度 | 数据 |
|---|---|
| 决策日 | 2026-04-28 |
| 当前价 | 202.86（4/28 收盘）|
| 总市值 | ~261 亿（按总股本 1.29 亿股）|
| 流通市值 | **174 亿**（实测，capital-flow.sh 输出）|
| 总股本 / 流通股本 | 1.29 亿 / 0.7245 亿 |
| 流通比 | 56.3% |
| 30 日累计涨幅 | +33.38% |
| 60 日涨停次数 | 2 次（1/30 + 4/21）|
| 板块对比 | 创业板指 30 日 +9.65% / 致尚 +33% → 板块/个股 = 29% |
| PE / PB / 换手率 | 666 / 12 / 9.19% |
| 事件状态 | 4/8 停牌筹划恒扬数据收购 → 4/21 复牌 → 5/2 受理 → 反馈意见已回复 |
| 距过会 | ~91 天（T+3 = 7/28）|
| 主营 / 主题 | 消费电子精密件 + AI 算力 + CPO + Switch 2 + 越南 |

### 1.2 期望 framework 输出（0.4.0 后）

#### asset-type-classifier 输出

```json
{
  "tags_triggered": ["A_event", "B_momentum", "C_smallcap"],
  "B_strength": "strong",
  "B_signals_hit": 5,
  "B_signals_breakdown": {
    "B1_30d_cumulative": true,
    "B2_limit_up_count": true,
    "B3_price_vs_ma60": false,
    "B4_sector_lag": true,
    "B5_theme_heat": true,
    "B6_turnover": true
  },
  "C_confidence": "weak_to_medium",
  "asset_profile": "重组+主升浪+小盘",
  "main_framework": ["capital-flow", "event-driven", "technical-pattern"],
  "veto_triggered": ["B_strong_no_short"]
}
```

**期望**：B 强档禁止做空决策。

#### capital-flow 输出

```json
{
  "circulation_market_cap_yi": 174,
  "control_score": 67,
  "control_level": "high",
  "main_direction_total": 40,
  "main_direction_label": "mod_buy",
  "anomaly_level": "strong",
  "ev_modifier": 1.2,
  "operation_recommendation": "follow"
}
```

**期望**：偏多，不应做空。

#### event-driven 输出

```json
{
  "event_type": "restructuring",
  "current_node": "feedback",
  "days_to_next_node": 91,
  "next_node_name": "证监会过会判定",
  "fulfillment_probability": 0.60,
  "event_strength_score": 54,
  "event_strength_tier": "low",
  "path_ev_pct": 1.25,
  "terminal_ev_pct": -5.9,
  "combined_ev_pct": 1.25,
  "operation_recommendation": "watchlist"
}
```

**期望**：低确定性事件 + 路径 EV 正 → watchlist。

#### technical-pattern 输出

```json
{
  "wave_stage": "washing",
  "washing_vs_distribution": {
    "verdict": "washing",
    "washing_signals_hit": 4,
    "distribution_signals_hit": 1,
    "confidence": "high"
  },
  "price_volume": "falling_quiet",
  "ma_system": "bull_alignment",
  "pattern_score": 52,
  "pattern_score_tier": "mod_bull",
  "intraday_pattern_used": false,
  "operation_recommendation": "watch"
}
```

**期望**：洗盘末端偏多 + MA 多头 → watch。

#### combined-decision-card 综合

```json
{
  "consensus": {
    "votes": {"sell": 0, "buy": 0, "hold": 0, "watch": 2, "follow": 1, "watchlist": 1},
    "majority_action": "watchlist-add",
    "confidence": "medium",
    "frameworks_aligned": 3
  }
}
```

**期望最终决策**：`watchlist-add`（**不是 skip / sell**）。

### 1.3 实际历史决策 vs 期望

| 项 | 实际（0.3.1 之前）| 期望（0.4.0 后）|
|---|---|---|
| 4/28 决策动作 | **skip / 卖出** | **watchlist-add** |
| 4 framework 是否独立验证？ | ❌ 仅用 valuation-relative | ✅ 4 framework 全跑 |
| 4/29 → 5/7 实测股价 | +22.7% | 同 |
| 实际偏差 | -22.7%（错判方向反向）| -1% ~ +5%（取决于何时入场观察）|

### 1.4 回归断言（CI 化时用）

```python
# 伪代码 - 0.4.x 工程化时落地
def test_zhishang_2026_04_28():
    inputs = load_yaml("docs/tests/cases/zhishang-2026-04-28.yaml")
    
    # 跑 asset-type-classifier
    classifier_out = run_classifier(inputs)
    assert "A_event" in classifier_out.tags_triggered
    assert "B_momentum" in classifier_out.tags_triggered
    assert "C_smallcap" in classifier_out.tags_triggered
    assert classifier_out.B_strength == "strong"
    assert "B_strong_no_short" in classifier_out.veto_triggered
    
    # 跑 capital-flow
    capflow_out = run_capital_flow(inputs)
    assert capflow_out.control_score >= 60
    assert capflow_out.main_direction_label in ["mod_buy", "strong_buy"]
    assert capflow_out.operation_recommendation in ["follow", "buy", "observe"]
    
    # 跑 event-driven
    event_out = run_event_driven(inputs)
    assert event_out.event_strength_score < 60
    assert event_out.path_ev_pct > 0
    assert event_out.operation_recommendation == "watchlist"
    
    # 跑 technical-pattern
    tech_out = run_technical_pattern(inputs)
    assert tech_out.washing_vs_distribution.verdict == "washing"
    assert tech_out.pattern_score > 30
    assert tech_out.intraday_pattern_used is False  # 铁律
    assert tech_out.operation_recommendation in ["watch", "follow", "hold"]
    
    # 综合决策不能是 sell / skip
    consensus = combine_4_frameworks(classifier_out, capflow_out, event_out, tech_out)
    assert consensus.majority_action not in ["sell", "skip"]
    assert consensus.frameworks_aligned >= 3
```

---

## 用例 2：群核科技 0068.HK 首日 +144%（IPO 套利成功案例）

### 2.1 输入数据

| 维度 | 数据 |
|---|---|
| 上市日 | 2025-04-17 |
| 招股价 | 18.60 HKD |
| 首日开盘 | ~28 HKD |
| 首日收盘 | 45.40 HKD（+144%）|
| 公开超额倍数 | 100+ 倍 |
| 暗盘表现 | +180% |
| 信号矩阵评分 | 129/140 = S 级 |

### 2.2 期望输出（hk-ipo-arbitrage 0.1.0）

- 决策动作：`ipo`（10x 孖展）
- 单手预期 EV：+1230 HKD
- 期望首日卖出价：开盘秒成
- 实际验证：开盘 20.70 → 20.50 秒成交 → 单手盈利 5690 HKD

### 2.3 回归断言

```python
def test_qunhe_ipo_2025_04_17():
    inputs = load_yaml("docs/tests/cases/qunhe-2025-04-17.yaml")
    out = run_hk_ipo_arbitrage(inputs)
    assert out.signal_score.tier == "S"
    assert out.signal_score.total >= 110
    assert out.decision_action == "ipo"
    assert out.ev_calculation.expected_value_hkd_or_usd > 0
```

---

## 用例 3：沪电股份血泪案例（铁律 0 触发用例）

### 3.1 输入数据

| 维度 | 数据 |
|---|---|
| 决策日 | 2026-04-24 |
| WebSearch 引用股价 | "85 元"（来自研报片段，未标日期）|
| 实际当时股价 | ~104 元 |
| 错判原因 | 用 WebSearch 的历史股价当当前价 |

### 3.2 期望（0.3.1 后）

- 触发铁律 0：必跑 quote.sh 校准
- 决策卡 checklist `data_calibration.passed = true` 当且仅当：
  - `quote_script_ran = true`
  - `data_timestamp` 在决策日 ± 1 个交易日内
  - `stale_data_used = false`

### 3.3 回归断言

```python
def test_huadian_iron_law_zero():
    inputs = {"web_search_price": 85, "decision_date": "2026-04-24"}
    
    # 不跑 quote.sh 应直接 fail checklist
    decision_card_a = build_decision_card_skip_quote(inputs)
    assert decision_card_a.checklist.data_calibration.passed is False
    assert decision_card_a.process_violation is True
    
    # 跑 quote.sh 后应 pass
    quote_result = run_quote_script("sz002463")
    decision_card_b = build_decision_card_with_quote(inputs, quote_result)
    assert decision_card_b.checklist.data_calibration.passed is True
    assert abs(decision_card_b.current_price - 104) < 5  # 真实股价附近
```

---

## 用例 4：东山精密 002384（valuation-relative 框架成功案例）

### 4.1 输入数据

| 维度 | 数据 |
|---|---|
| 决策日 | 2026-04-22 |
| 当前价 | 28.50 |
| 三情景目标价 | 22 / 32 / 42（bear/base/bull）|
| 概率分布 | 0.20 / 0.50 / 0.30 |
| 期望价 | 32.20（+12.98% EV）|
| 标签 | E_value（稳态价值股）|

### 4.2 期望输出（valuation-relative 0.2.0）

- asset-type-classifier 仅触发 E_value
- 不触发 A / B / C 标签
- 走 valuation-relative 主框架
- 决策动作：buy（EV +12.98% 大于阈值 +10%）
- 止损：22 / 最大亏损 -22.8%

### 4.3 回归断言

```python
def test_dongshan_valuation_relative():
    inputs = load_yaml("docs/tests/cases/dongshan-2026-04-22.yaml")
    
    # asset-type-classifier 应仅触发 E_value
    cls = run_classifier(inputs)
    assert "E_value" in cls.tags_triggered
    assert "A_event" not in cls.tags_triggered
    assert "B_momentum" not in cls.tags_triggered
    
    # valuation-relative 三情景概率必须和为 1
    val = run_valuation_relative(inputs)
    total_prob = sum(s["probability"] for s in val.scenarios.values())
    assert abs(total_prob - 1.0) < 0.001
    
    # EV 计算正确
    expected = sum(s["probability"] * s["target_price"] for s in val.scenarios.values())
    assert abs(val.expected_price - expected) < 0.5
    assert val.ev_pct > 10  # 触发 buy 阈值
```

---

## 用例 5：NVDA 2023-Q1 财报（事件驱动 / 透过表象成功案例）

### 5.1 输入数据

| 维度 | 数据 |
|---|---|
| 财报日 | 2023-05-24 |
| 表层数据 | Revenue Beat |
| 中层数据 | Data Center YoY +14% |
| **里层数据** | **Q2 Guidance $11B（+55% jump）→ HBM 供应锁死** |

### 5.2 期望输出（command-driven-analysis 0.1.0 + ai-thematic-investing）

- 触发 3 层信息拆解
- 识别"指引跳空"信号
- 推断"HBM 供应锁死"产业链含义
- 输出：T+3 / T+6 / T+12 / T+24 预判

### 5.3 回归断言

```python
def test_nvda_2023_q1_layered_signals():
    inputs = load_yaml("docs/tests/cases/nvda-2023-q1.yaml")
    
    # 3 层信息拆解
    out = run_layered_analysis(inputs)
    assert out.surface_layer.detected is True
    assert out.middle_layer.detected is True
    assert out.deep_layer.detected is True
    
    # 关键信号识别
    assert "guidance_jump" in out.deep_layer.signals
    assert out.deep_layer.signals["guidance_jump"]["next_quarter_pct"] > 0.50
    
    # 4 时点预判全部填写
    assert all(out.predictions[t].is_specific for t in ["T+3", "T+6", "T+12", "T+24"])
```

---

## 用例 6：致尚 4/29 单日分时形态错判（technical-pattern 铁律）

### 6.1 输入数据

| 维度 | 数据 |
|---|---|
| 当日 | 2026-04-29 |
| 收盘 | 217.70（+7.32%）|
| 分时形态 | 9:35 高 219.89 / 14:00 高 219.99 / 尾盘走弱 |
| 量能 | 27 亿（巨量）|
| 板块 | AI 链 +2.51% 同步 |

### 6.2 期望输出（technical-pattern 0.4.0）

- `intraday_pattern_used` 必须 `false`（铁律）
- 多日 K 线判定：4/28 → 4/29 价升 + 量增 + MA 突破 + 板块同步 = 二波启动 ✅
- 不应判定为"出货"

### 6.3 回归断言

```python
def test_zhishang_intraday_pattern_ban():
    inputs = load_yaml("docs/tests/cases/zhishang-2026-04-29.yaml")
    
    # 跑 technical-pattern
    out = run_technical_pattern(inputs)
    
    # 铁律：intraday_pattern_used 必须为 false
    assert out.intraday_pattern_used is False
    
    # 多日 K 线判定应识别二波启动
    assert out.wave_stage == "second_wave"
    assert out.price_volume == "rising_with_volume"
    assert out.ma_system == "bull_alignment"
    assert out.pattern_score > 50  # 偏多偏强
    assert out.operation_recommendation in ["add", "follow", "hold"]
    
    # 不应输出 exit / trim
    assert out.operation_recommendation not in ["exit", "trim"]
```

---

## 回归运行机制

### 当前阶段（0.4.0）：手工回归

每次 framework 升级后，手工跑 6 个用例，对比期望输出：

```bash
# 手工跑用例 1
echo "=== Case 1: 致尚 2026-04-28 ==="
echo "1. asset-type-classifier 期望：A+B+C, B 强档, watchlist-add"
echo "2. capital-flow 期望：control 67, mod_buy"
echo "3. event-driven 期望：score 54 低, watchlist"
echo "4. technical-pattern 期望：洗盘末端 +52, watch"
echo "→ 综合：watchlist-add（不是 skip / sell）"
```

### 0.4.x 工程化阶段：CI 化

待 0.4.3 落地：
1. 用例数据存 `docs/tests/cases/*.yaml`
2. framework 输出脚本化（asset-type-classifier.py / capital-flow.py / ...）
3. pytest 跑断言
4. CI on PR 自动验证

### 1.0.0 里程碑：实战命中率验证

- 跑全量回归 ≥ 6 个用例 全部通过
- 实战 6 个月：60+ 决策，命中率 ≥ 60%
- 错判分布：D5 认知盲点占比 < 30%
- 路径 EV vs 终点 EV 模型对比：路径 EV 真实命中率高于终点 EV

---

## 用例增加规则

每次实战错判 → **新增回归用例**：

| 错判 | 用例 | 验证目标 |
|---|---|---|
| 致尚 2026-04-28 → 5/7 | 用例 1 | 0.4.0 闭环 6 层根因 |
| 群核 2025-04-17 | 用例 2 | hk-ipo-arbitrage 信号矩阵 |
| 沪电 2026-04-24 | 用例 3 | 铁律 0 数据校准 |
| 东山 2026-04-22 | 用例 4 | valuation-relative 三情景 |
| NVDA 2023-Q1 | 用例 5 | 透过表象 / 3 层信息拆解 |
| 致尚 2026-04-29 | 用例 6 | technical-pattern 单日分时禁令 |
| _未来错判_ | 用例 N | 对应 framework 修复 |

**铁律**：错判 → 归因 → framework 升级 → 新增回归用例 → 升级前后跑全量回归确保不退化。这是 self-improvement-loop 的工程化出口。

---

## 与其他文档的关系

- `frameworks/self-improvement-loop.md` — 4 层闭环理论
- `templates/decision-postmortem.md` — 错判归因模板
- `docs/finance-journal/INDEX.md` — 决策档案索引
- `docs/finance-journal/postmortem/` — 实战错判归因（每个错判生成一份归因 → 沉淀为新回归用例）

---

## Disclaimer

回归测试集是**防止 framework 退化**的工具，不是"保证未来必对"。

**核心局限**：
- 历史用例不能代表所有未来场景
- 6 个用例覆盖度有限，需持续扩充
- 期望输出是"按当前认知应该输出的"，认知本身可能有误（需持续校准）

**使用纪律**：
1. 每次 framework 升级强制跑全量回归
2. 任一用例期望输出变化 = 必须在 CHANGELOG 显式标注 "BREAKING: regression case X expected output changed"
3. 实战错判 = 新增用例（不允许"忘了"）
4. 0.4.x 阶段优先工程化用例 1（致尚）+ 用例 6（4/29 分时禁令），其他用例可保持手工
