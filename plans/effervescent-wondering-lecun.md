# 交易规则体系补全 — 实现计划

## Context

当前 A 股短线交易系统的核心规则层有多处缺陷。本计划分两部分补全：
- **Part A (Task 1-6)**：基础能力补全 — 信号修复、持仓追踪、风控执行、仓位校验、动态止损、盈亏配对
- **Part B (Task 7-12)**：交易高手体系融入 — 基于养家心法、弱转强策略等，增强情绪周期、赚钱效应量化、龙头联动、赢面评估

专注盘后分析场景（不做盘中监控）。交割单每日手动上传。

**执行顺序**：1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12

---

# Part A: 基础能力补全

## Task 1: 修复龙头低吸信号（Signal 2）

**问题**：`signals.py:44` 检查 `large_buy_orders >= 3`，但该字段在 `stock_picker.py:130` 硬编码为 0，信号永远不触发。

**方案**：用 `缩量回踩 + MACD金叉 + RSI超卖` 组合替代。

**改动**：
- `src/trading/signals.py`: 将 `large_buy_orders >= 3` 替换为 `pullback_volume_ratio < 0.5 AND macd_golden_cross AND rsi < 40`；更新 reason 为"缩量回踩+MACD金叉+RSI超卖"
- `src/trading/stock_picker.py`: `build_stock_ctx()` 中添加 `rsi = compute_rsi(closes, 14)`，移除 `large_buy_orders`；删除 `check_near_miss_signals()` 函数；更新 `scan_candidates()` 和 `analyze_single_stock()` 中的调用
- `src/trading/strategy_engine.py`: `AVAILABLE_FIELDS` 中添加 `{"field": "rsi", "label": "RSI", "type": "number", "min": 0, "max": 100}`
- `src/trading/db.py`: `_seed_default_strategies()` 更新 `leader_dip` 模板条件，加入 `pullback_volume_ratio`、`macd_golden_cross`、`rsi` 条件；添加 `_migrate_leader_dip_strategy(conn)` 迁移函数
- `tests/test_signals.py`: 更新龙头低吸测试用例，用新条件替换 `large_buy_orders`

---

## Task 2: 持仓追踪（基于交割单）

**问题**：系统没有"当前持仓"概念。

**方案**：从 `delivery_orders` 表按代码聚合买卖数量差得到当前持仓；调 `get_stock_brief()` 获取现价算浮盈。

**改动**：
- **新建** `src/trading/holdings.py`:
  - `get_current_holdings(db_path)` → 聚合 delivery_orders，SQL: `GROUP BY code HAVING buy_qty > sell_qty`
  - `get_holding_pnl(holdings)` → 对每个持仓调 `fetch_with_fallback("get_stock_brief")` 获取现价
  - `get_holding_detail(code)` → 单只股票全部交易流水
- `src/trading/api.py`: 添加 `GET /api/holdings`、`GET /api/holdings/{code}`
- `frontend/src/api/client.ts`: 添加 `HoldingItem`、`HoldingsResponse` 类型
- `frontend/src/pages/DashboardPage.tsx`: 添加 HoldingsCard 组件
- **新建** `tests/test_holdings.py`

---

## Task 3: 买卖自动配对和已实现盈亏

**问题**：trades 表的 pnl 需手动填写。

**方案**：FIFO 配对 delivery_orders 的买卖记录。

**改动**：
- `src/trading/holdings.py` 添加:
  - `match_trades_fifo(code)` → FIFO 队列匹配
  - `calculate_realized_pnl(code)` → 单股已实现盈亏
  - `calculate_all_realized_pnl()` → 全部股票
- `src/trading/api.py`: 添加 `GET /api/holdings/realized-pnl`、`GET /api/holdings/{code}/matched-trades`
- `frontend/src/api/client.ts`: 添加相应类型
- `tests/test_holdings.py`: 添加 FIFO 配对测试

---

## Task 4: 风控自动执行

**问题**：`check_risk_limits()` 只是信息查询端点，从不自动执行。

**改动**：
- `src/trading/db.py`: 新增 `risk_status` 表
- **新建** `src/trading/risk_manager.py`:
  - `compute_risk_metrics(db_path)` → 从 trades + holdings 算日盈亏/周回撤/月回撤/连亏
  - `get_risk_status(db_path)` → can_trade + violations + risk_level
  - `save_risk_status(db_path)` → 持久化
- `src/trading/scheduler.py`: `run_daily_job()` 添加 Step 5
- `src/trading/api.py`: `GET /api/risk/status`
- `frontend/src/pages/DashboardPage.tsx`: 风控徽章（绿/黄/红）+ 警告横幅
- **新建** `tests/test_risk_manager.py`

---

## Task 5: 动态止损 / 移动止盈

**问题**：只有固定 7%/10% 止损。

**止损规则**：盈利 ≥20%→回撤8%止盈，≥10%→回撤5%，≥5%→保本+2%，<5%→固定止损。

**改动**：
- `src/trading/config.py`: 添加 `DYNAMIC_STOP` 常量
- `src/trading/db.py`: 新增 `trade_alerts` 表
- `src/trading/signals.py`: 添加 `compute_dynamic_stop()`
- `src/trading/scheduler.py`: `run_daily_job()` 添加 Step 6 — 遍历持仓扫描
- `src/trading/api.py`: `GET /api/alerts`、`PATCH /api/alerts/{id}`
- `frontend/src/pages/DashboardPage.tsx`: AlertsPanel 组件
- **新建** `tests/test_dynamic_stop.py`

---

## Task 6: 仓位校验

**问题**：仓位矩阵从不校验。

**改动**：
- `src/trading/position.py`: 添加 `validate_position()` → `{valid, warnings}`
- `src/trading/api.py`: `POST /api/trades` 买入时校验 + `POST /api/position/validate`
- `frontend/src/pages/JournalPage.tsx`: 买入确认对话框
- `tests/test_position.py`: 新增测试

---

# Part B: 交易高手体系融入

## Task 7: 赚钱效应指数

**来源**：养家心法 — "除成交量外基本什么指标都不看"，本质看赚钱效应。

**问题**：当前情绪周期判断仅基于温度趋势（5日温度均值），过于粗糙，无法反映市场真实的赚钱/亏钱效应。

**方案**：新增赚钱效应指数（Profit Effect Index），综合量化市场短线赚钱难度。

**指标定义**：
```
赚钱效应指数 = (
    涨停数权重 × 涨停数得分 +          # 涨停家数越多赚钱效应越强
    连板高度权重 × 最高连板得分 +        # 市场高度反映龙头空间
    炸板率权重 × (1 - 炸板率得分) +     # 炸板率越低越健康
    首板次日溢价权重 × 溢价率得分 +      # 打板次日能赚钱
    跌停数权重 × (1 - 跌停数得分)       # 跌停越少亏钱效应越弱
)
```

**改动**：
- **新建** `src/trading/profit_effect.py`:
  - `calculate_profit_effect(overview, zt_pool) -> dict`: 计算当日赚钱效应各分项和总分(0-100)
    - `limit_up_score`: 涨停数→得分映射（<10→0, 10-30→线性, 30-60→线性, >60→90-100）
    - `max_board_height`: 最高连板数→得分（1板→20, 3板→50, 5板→80, 7+板→100）
    - `failed_board_rate`: 炸板数/涨停数→得分（<10%→100, 10-30%→线性, >30%→0）
    - `next_day_premium`: 昨日首板今日平均溢价→得分（>5%→100, 0-5%→线性, <0→0）
    - `limit_down_penalty`: 跌停数→反向得分
  - `get_profit_effect_history(days, db_path) -> list[dict]`: 查询历史数据
- `src/trading/db.py`: 扩展 `market_temp_history` 表添加 `profit_effect_score`、`max_board_height`、`failed_board_rate`、`next_day_premium` 列（迁移）
- `src/trading/scheduler.py`: Step 1 中计算并持久化赚钱效应指数
- `src/trading/api.py`: `GET /api/market/profit-effect` 返回最近N日赚钱效应指数
- `frontend/src/api/client.ts`: 添加类型
- `frontend/src/pages/DashboardPage.tsx`: 赚钱效应仪表盘（与温度并列显示）
- **新建** `tests/test_profit_effect.py`

---

## Task 8: 情绪周期增强

**来源**：养家心法 — 情绪周期是交易的核心；攻击波概念（每一个攻击波酝酿一波赚钱效应）。

**问题**：当前 `_infer_sentiment()` 在 `scheduler.py:212` 仅用温度值做简单if/else判断，无法识别攻击波、转换信号。

**方案**：基于赚钱效应指数（Task 7 产出）重新实现多层情绪周期判断。

**情绪周期模型**：
```
冰点 → 修复 → 升温 → 高潮 → 分歧 → 退潮 → 冰点（循环）
```

每阶段判断条件（基于赚钱效应指数 PEI 和趋势）：
- **冰点**：PEI < 20 且连续3日下降
- **修复**：PEI 20-35 且从冰点回升（PEI > 前日）
- **升温**：PEI 35-55 且连续2日上升
- **高潮**：PEI > 55 且连续2日上升或持平
- **分歧**：前日为高潮/升温但当日 PEI 下降 ≥10
- **退潮**：PEI 连续2日下降且从高位(>50)回落

每阶段操作建议（养家原则）：
- **冰点**：空仓或极轻仓，等待转机
- **修复**：试探性买入超跌龙头，小仓
- **升温**：加仓主线龙头，中仓
- **高潮**：追涨强势股，可大仓，但警惕分歧
- **分歧**：减仓，只留核心龙头
- **退潮**：清仓或做超跌反弹

**攻击波识别**：
- 连续 PEI 上升的天数 = 一个攻击波
- 攻击波结束标志：PEI 连续2日下降
- 记录攻击波长度和强度

**强转弱信号**（养家：龙头缩量加速后放量分歧）：
- 市场最高板缩量加速涨停 + 次日放量分歧（换手率突增）
- PEI 从 >60 单日跌 >15

**弱转强信号**：
- PEI 从 <20 连续2日上升 >10
- 涨停数突然增加 >50%

**改动**：
- **新建** `src/trading/sentiment.py`:
  - `classify_sentiment_stage(pe_history) -> dict`: 基于近5日 PEI 判断当前阶段
  - `detect_attack_wave(pe_history) -> dict`: 识别攻击波
  - `detect_transition_signals(pe_history, zt_data) -> list[dict]`: 检测强转弱/弱转强信号
  - `get_operation_advice(stage, market_state) -> dict`: 每阶段操作建议
- `src/trading/scheduler.py`: Step 1 后调用情绪分析，结果存入 `market_temp_history`
- `src/trading/api.py`: 重构 `GET /api/market/sentiment`，使用新模块替代旧逻辑
- `frontend/src/pages/DashboardPage.tsx`: 升级情绪周期展示（攻击波可视化 + 操作建议）
- **新建** `tests/test_sentiment.py`

---

## Task 9: 弱转强信号（新买入信号）

**来源**：弱转强策略实战 — 捕捉资金对个股定价的纠错机会。

**问题**：当前只有4种买入信号，缺少弱转强这一高爆发力信号。

**方案**：新增 Signal 5: 弱转强，含三种子类型。

**三种弱转强子类型**：

1. **趋势弱转强**：
   - 20/30日均线向上
   - 回踩期缩量至均量60%以下
   - 突破时放量≥30%
   - MA5 金叉 MA10

2. **连板弱转强**（高标分歧转强）：
   - 前日为连板股（≥2板）
   - 前日炸板或大幅回调（跌幅>3%）
   - 今日重新封板或大涨（>5%）
   - 板块内有跟风股同步走强

3. **反包弱转强**：
   - 前日放量下跌（换手率>8%）
   - 今日放量上涨反包前日阴线
   - 量比 > 1.5
   - 所属板块有其他个股同步走强

**改动**：
- `src/trading/config.py`: `SignalType` 枚举添加 `WEAK_TO_STRONG = "弱转强"`
- `src/trading/signals.py`: 添加弱转强信号检测逻辑（三种子类型），在 `check_buy_signals()` 中增加 Signal 5 检查（适用于强势和震荡偏强市场）
- `src/trading/stock_picker.py`: `build_stock_ctx()` 中添加弱转强所需字段：
  - `prev_day_change_pct`: 前一日涨跌幅
  - `prev_day_turnover`: 前一日换手率
  - `volume_change_ratio`: 今日成交量/昨日成交量
  - `ma20_bullish`: MA20是否多头
  - `sector_strength`: 板块内跟涨股比例
- `src/trading/db.py`: `_seed_default_strategies()` 添加 `weak_to_strong` 模板策略
- `src/trading/strategy_engine.py`: `AVAILABLE_FIELDS` 添加新字段
- `tests/test_signals.py`: 添加弱转强三种子类型测试

---

## Task 10: 龙头动态监控

**来源**：养家心法 — "龙头涨停后板块小弟不跟涨=危险信号"；"缩量加速→放量分歧是转折点"。

**问题**：当前龙头识别是静态评分，无法检测龙头失效、切换和转折信号。

**方案**：增加龙头联动度、失效检测、切换信号。

**指标定义**：
- **联动度** = 龙头涨停当日，同板块涨幅>3%的个股数 / 板块总个股数
  - ≥50%: 强联动
  - 30-50%: 一般联动
  - <30%: 弱联动（龙头独行，危险）
- **缩量加速转折** = 连续2日缩量涨停 → 次日放量（量比>2）+ 涨跌幅<3% → 转折信号
- **龙头切换信号** = 旧龙头出现分歧/跌停 + 同板块新标的首次涨停

**改动**：
- `src/trading/leader_detect.py`: 添加函数：
  - `calculate_leader_cohesion(leader_code, sector_stocks) -> float`: 联动度计算
  - `detect_leader_failure(leader_history) -> dict`: 龙头失效检测
  - `detect_leader_switch(old_leader, sector_zt_stocks) -> dict`: 龙头切换
- `src/trading/scheduler.py`: 每日任务 Step 3 增强 — 对当日涨停池中的连板股计算联动度
- `src/trading/db.py`: 扩展 `ai_results` 或新建 `leader_monitor` 表存储联动度历史
- `src/trading/api.py`: `GET /api/leaders/monitor` — 返回龙头状态（联动度、失效风险、切换信号）
- `frontend/src/pages/DashboardPage.tsx` 或 `SectorsPage.tsx`: 龙头监控卡片
- **新建** `tests/test_leader_monitor.py`

---

## Task 11: 赢面评估系统

**来源**：养家心法 — "赢面60%以下观望，90%以上满仓"；仓位与赢面对应。

**问题**：当前仓位矩阵是市场状态×信号强度的静态查表，不考虑具体标的的胜率和空间。

**方案**：计算每个候选股的"赢面"，基于历史同类信号胜率×风险收益比，动态调整仓位建议。

**赢面公式**：
```
赢面 = 胜率 × 上涨空间系数 / 下跌空间系数

胜率 = 历史同类信号的盈利笔数 / 总笔数（最近3个月）
上涨空间 = min(板块龙头空间, 同类历史平均涨幅, 技术目标位)
下跌空间 = 止损距离（动态止损价 vs 当前价）
```

**仓位映射（养家规则）**：
- 赢面 < 60%: 建议观望
- 赢面 60-70%: 小仓（10-20%）
- 赢面 70-80%: 中仓（20-40%）
- 赢面 80-90%: 大仓（40-60%）
- 赢面 > 90%: 满仓（60-100%）

**改动**：
- **新建** `src/trading/win_rate.py`:
  - `calculate_signal_win_rate(signal_type, months=3, db_path) -> dict`: 从历史交易统计同类信号胜率
  - `estimate_upside(stock_ctx, sector_data) -> float`: 估算上涨空间
  - `estimate_downside(entry_price, stop_price) -> float`: 估算下跌空间
  - `calculate_win_probability(signal_type, stock_ctx, sector_data, db_path) -> dict`: 综合赢面
  - `get_position_by_win_prob(win_prob) -> dict`: 赢面→仓位建议映射
- `src/trading/stock_picker.py`: `scan_candidates()` 中为每个候选股添加赢面评估
- `src/trading/api.py`: 在选股结果中附加赢面和仓位建议
- `frontend/src/pages/StockPickerPage.tsx`: 显示赢面评分和仓位建议
- **新建** `tests/test_win_rate.py`

---

## Task 12: 盘前检查清单增强

**来源**：养家心法 — "预判热点→试错→加仓→离场"流程；daily_checklist 表已存在但无自动填充。

**问题**：`daily_checklist` 表已建但从未有逻辑填充，盘前计划完全手动。

**方案**：调度器自动生成次日检查清单，结合 AI 角色出具操作计划。

**检查清单内容**：
1. **市场状态**：温度、情绪周期阶段、操作建议
2. **主线板块**：连续3日排名前5的板块
3. **龙头候选**：当前活跃龙头 + 联动度 + 生命周期
4. **待止损持仓**：当前持仓中触发动态止损的标的
5. **风控状态**：can_trade、violations
6. **赢面排名**：赢面 >60% 的候选股Top5
7. **明日关注**：AI 角色生成的买入/卖出计划

**改动**：
- **新建** `src/trading/checklist.py`:
  - `generate_daily_checklist(db_path) -> dict`: 汇总上述 7 项
  - `save_checklist(checklist, db_path)`: 存入 daily_checklist 表
- `src/trading/scheduler.py`: `run_daily_job()` 最后一步调用 `generate_daily_checklist()`
- `src/trading/api.py`: `GET /api/checklist/today`、`GET /api/checklist/{date}`
- `frontend/src/api/client.ts`: 添加类型
- **新建** `frontend/src/pages/ChecklistPage.tsx` 或在 DashboardPage 中添加清单卡片
- **新建** `tests/test_checklist.py`

---

## 新增/修改文件汇总

| 文件 | 操作 | 涉及 Task |
|------|------|-----------|
| `src/trading/holdings.py` | 新建 | 2, 3 |
| `src/trading/risk_manager.py` | 新建 | 4 |
| `src/trading/profit_effect.py` | 新建 | 7 |
| `src/trading/sentiment.py` | 新建 | 8 |
| `src/trading/win_rate.py` | 新建 | 11 |
| `src/trading/checklist.py` | 新建 | 12 |
| `src/trading/signals.py` | 修改 | 1, 5, 9 |
| `src/trading/stock_picker.py` | 修改 | 1, 9, 11 |
| `src/trading/strategy_engine.py` | 修改 | 1, 9 |
| `src/trading/config.py` | 修改 | 5, 9 |
| `src/trading/position.py` | 修改 | 6 |
| `src/trading/leader_detect.py` | 修改 | 10 |
| `src/trading/db.py` | 修改 | 1, 4, 5, 7, 9, 10 |
| `src/trading/scheduler.py` | 修改 | 4, 5, 7, 8, 10, 12 |
| `src/trading/api.py` | 修改 | 2-12 |
| `frontend/src/api/client.ts` | 修改 | 2-12 |
| `frontend/src/pages/DashboardPage.tsx` | 修改 | 2, 4, 5, 7, 8, 10, 12 |
| `frontend/src/pages/JournalPage.tsx` | 修改 | 6 |
| `frontend/src/pages/StockPickerPage.tsx` | 修改 | 11 |
| `frontend/src/pages/SectorsPage.tsx` | 修改 | 10 |
| `tests/test_signals.py` | 修改 | 1, 9 |
| `tests/test_holdings.py` | 新建 | 2, 3 |
| `tests/test_risk_manager.py` | 新建 | 4 |
| `tests/test_dynamic_stop.py` | 新建 | 5 |
| `tests/test_position.py` | 修改 | 6 |
| `tests/test_profit_effect.py` | 新建 | 7 |
| `tests/test_sentiment.py` | 新建 | 8 |
| `tests/test_leader_monitor.py` | 新建 | 10 |
| `tests/test_win_rate.py` | 新建 | 11 |
| `tests/test_checklist.py` | 新建 | 12 |

## 关键设计决策

1. **持仓即时计算**：`get_current_holdings()` 每次查询 delivery_orders 聚合，不建持仓表
2. **风控状态持久化**：risk_status 每日写入，连亏计数需跨日追踪
3. **仓位校验是建议性的**：返回 warnings，用户可覆盖
4. **动态止损每日批处理**：调度器 18:00 扫描
5. **FIFO 配对按需计算**：不建配对表
6. **赚钱效应指数是情绪周期的基础**：Task 7 → Task 8 强依赖
7. **赢面评估需要历史数据积累**：初期胜率数据不足时使用默认值
8. **盘前清单汇总不产生新数据**：只聚合其他模块的产出

## 验证方式

1. `uv run python -m pytest tests/ -v` — 全部测试通过
2. `cd frontend && npm run build` — 前端构建成功
3. 手动验证：导入交割单 → Dashboard 显示持仓 → 调度器触发 → 风控/止损/赚钱效应/情绪/清单 全链路更新
