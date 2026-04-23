# finance-analysis 0.2.0 回归测试

> 验证 0.2.0 新增 4 个 framework（valuation-relative / valuation-dcf / stock-selection / us-ipo-arbitrage）+ 2 个 template（valuation-card / stock-screening-card）的加载、输出、跨 framework 协作是否正确。
>
> 每次 skill 改动后全量回归。

---

## 前置条件

- finance-analysis skill 版本 ≥ 0.2.0
- `skills/finance-analysis/references/frameworks/` 含：valuation-relative.md / valuation-dcf.md / stock-selection.md / us-ipo-arbitrage.md
- `skills/finance-analysis/references/templates/` 含：valuation-card.md / stock-screening-card.md
- `skills/finance-analysis/references/frameworks/_index.md` 已更新辅助 framework 表

## 执行方式

- 每个用例以"命题输入"形式触发 skill
- 观察 Lead agent 加载的 framework 清单、输出格式、是否匹配预期
- 失败项回到对应 framework 修复

---

## 用例 1：相对估值命题（东山精密）

**命题**：帮我分析东山精密（002384）现在 186 元值不值得买

**预期路由**：
- 套路 A（个股分析）
- 加载 `valuation-relative`（主）+ `command-driven-analysis`（主入口认知）+ `valuation-dcf`（可选交叉验证）

**预期加载信号**：
```
framework_loaded: [command-driven-analysis, valuation-relative]
templates_loaded: [valuation-card, alpha-thesis-card]
```

**预期输出字段**（决策卡必含）：
- [ ] 多业务分拆（PCB + 索尔思光模块）
- [ ] 对标池 3-5 家（沪电 / 中际旭创 / 鹏鼎 / 生益 / 永鼎 任一组合）
- [ ] 三情景 forward 业绩（乐观/中性/悲观 + 概率权重 + 合理 PE + 合理股价）
- [ ] 概率加权期望价 ≈ 73 元（基础）
- [ ] 主题溢价因子 1.3-1.5x
- [ ] 加权合理股价（含溢价）100-140 元
- [ ] 隐含预期位置：> 100% 乐观 + 主题溢价（155%）
- [ ] 盈亏比 ≈ 负 1:3
- [ ] 决策：减仓 40-50%
- [ ] 止损 150
- [ ] 反面证据 ≥ 3 条

**失败判定**：
- 给出单点目标价而非三情景 → 违反"预期驱动"核心认知
- 未做多业务分拆 → 违反铁律 -0.5
- 对标 < 3 家 → 违反铁律 -1
- 建议全仓买入（不减仓）→ 逻辑错位

---

## 用例 2：DCF 估值命题（NVDA 2023）

**命题**：2023-05 时 NVDA $285 合理吗？用 DCF 给我算一下

**预期路由**：
- 套路 A（个股分析）
- 加载 `valuation-dcf`（主）+ `valuation-relative`（交叉验证）+ `ai-thematic-investing`（AI 主题锚）

**预期加载信号**：
```
framework_loaded: [valuation-dcf, valuation-relative, ai-thematic-investing]
templates_loaded: [valuation-card（§6 DCF 字段）]
```

**预期输出字段**：
- [ ] 适用性判断（成长期 / FCF 正 / 模式成熟 → 通过）
- [ ] 三情景营收假设（乐观 +47% / 中性 +35% / 悲观 +21% 5Y CAGR）
- [ ] 三情景利润率演进（毛利率 65-75%）
- [ ] WACC 从 Rf + β × ERP 推导（≈ 13.5%）
- [ ] 终值 Gordon 或出口倍数（交叉验证偏差 < 20%）
- [ ] 三情景 NPV 每股（乐观 $520 / 中性 $260 / 悲观 $118）
- [ ] 概率加权期望股价 ≈ $310
- [ ] 敏感性分析 4 参数（毛利率 ±10% 接近红线）
- [ ] 和相对估值交叉验证（DCF $310 vs relative $300，差 3% ✓）
- [ ] 决策：买入小仓 2-3%
- [ ] 止损 $200

**失败判定**：
- 单点 DCF 未做三情景 → 违反"三情景必须"
- 敏感性分析缺失 → 无法判断假设质量
- WACC 拍脑袋给（如直接 10%）→ 必须推导
- 终值单一方法未交叉 → 违反 "Gordon / 出口倍数交叉"

---

## 用例 3：选股命题（A 股 AI 算力）

**命题**：从 A 股 AI 算力股里帮我筛出 Top 3

**预期路由**：
- 套路 D（主题/赛道命题）
- 加载 `stock-selection`（主）+ `ai-thematic-investing`（Layer 卡位辅助）

**预期加载信号**：
```
framework_loaded: [stock-selection, ai-thematic-investing]
templates_loaded: [stock-screening-card]
```

**预期输出字段**：
- [ ] 赛道边界定义（"AI 算力"含义 + 包含/排除）
- [ ] 候选集构建（通过 Step 0 自动发现方法，至少 8-15 只）
- [ ] Step 1 赛道筛通过数 + 筛掉率
- [ ] Step 2 龙头筛通过数（每只标注市占率 / Layer 卡位）
- [ ] Step 3 质量筛（4 项全过）
- [ ] Step 4 成长筛
- [ ] 30/60/100 打分表（四维各 25 分，每个子项有数据依据）
- [ ] Top-3 清单（按总分降序）
- [ ] 每只附"下一步研究方向" + "Core / Satellite 标注"

**失败判定**：
- 产出"买入清单"而非"待研究清单" → 逻辑错位
- 某一步未筛掉 50%+ → 阈值没发挥作用
- 质量 4 项被放宽到 2 项 → 违反红线
- Top-3 直接给目标价 → 越俎代庖（应走估值 framework）
- 未标注 Core / Satellite → 仓位结构信息缺失

---

## 用例 4：美股 IPO 命题（DoorDash 2020-12）

**命题**：DoorDash 2020-12 IPO，发行价 $102，首日开盘 $182，打不打？怎么操作？

**预期路由**：
- 套路 A + 套路 C（事件驱动）
- 加载 `us-ipo-arbitrage`（主）+ `valuation-dcf`（路径 C 长期估值）+ `command-driven-analysis`（S-1 下钻）

**预期加载信号**：
```
framework_loaded: [us-ipo-arbitrage, valuation-dcf, command-driven-analysis]
templates_loaded: [ipo-decision-card（US 扩展）]
```

**预期输出字段**：
- [ ] S-1 核心数据（营收 $2.9B / 净亏损 $149M / 外卖 50%+）
- [ ] 定价区间评估（初始 $75-85 → 提价 2 次 → 最终 $102 = 极热）
- [ ] Lockup 180 天抛压评分（解锁规模 / 日均成交 = 强压力）
- [ ] 首日跳空预估（+70-90%，实际 +85%）
- [ ] **三路径 EV 详细比较**：
  - [ ] 路径 A（等 Lockup 回调）EV 估算
  - [ ] 路径 B（首日追涨）EV 估算
  - [ ] 路径 C（长期持有 2Y）EV 估算
- [ ] 路径选择 + 触发条件
- [ ] 止损 + 仓位 + 时间维度
- [ ] 和港股 IPO 机制差异对照（至少 3 点）

**失败判定**：
- 用 HK IPO 套路（孖展 / 暗盘 / 一人一手）→ 方法论错
- 未做三路径 EV 比较 → 核心方法论缺失
- 建议首日追涨 +85% 跳空 → 违反"首日跳空 > 60% EV 为负"
- Lockup 抛压没评估 → 美股独有的可预测事件未使用

---

## 用例 5：跨 framework 组合（"CATL 现在值不值买"）

**命题**：CATL 300750 现在值不值得重仓买？

**预期路由**：
- 套路 A（个股分析）
- 加载 `valuation-relative` + `valuation-dcf`（成长股交叉）+ `stock-selection`（判断龙头地位）+ `alpha-generation`（5 执行差）+ `command-driven-analysis`（主入口）

**预期加载信号**：
```
framework_loaded: [command-driven-analysis, valuation-relative, valuation-dcf, stock-selection, alpha-generation]
templates_loaded: [valuation-card, alpha-thesis-card]
```

**预期输出字段**：
- [ ] 行业地位（选股 framework 确认全球龙头 37% 市占率 + Layer 卡位）
- [ ] 相对估值（对标 LG Energy / Samsung SDI / Panasonic / BYD 电池业务）
- [ ] DCF 估值（成长期，三情景 + 敏感性）
- [ ] 两方法交叉验证（差异应 < 30%）
- [ ] 主题溢价（新能源车主线 → 1.2-1.3x）
- [ ] 5 执行差评估（精度 / 时点 / 仓位 / 持有 / 顶点）
- [ ] 决策卡 + 仓位建议（5-8% Core）
- [ ] 关键催化剂（麒麟量产 / 钠电商业化 / 海外工厂）

**失败判定**：
- 只用相对估值不做 DCF 交叉 → 成长股必做双方法
- 加载顺序错（先 DCF 后 relative）→ 对标池依赖 relative 先启动
- 未识别"龙头地位" → 需要 stock-selection 做龙头 Layer 判断
- 没给仓位结构（Core vs Satellite）→ 缺执行指引

---

## 用例 6：失效场景验证（"MiniMax 港股 IPO 估值"）

**命题**：MiniMax（假设）即将在港股上市，DCF 能给合理价吗？

**预期路由**：
- 套路 A（个股分析） + 套路 C（IPO）
- 加载 `valuation-dcf`（尝试）+ `valuation-relative`（无对标退回）+ `hk-ipo-arbitrage`

**预期行为**：
- valuation-dcf 的 §8.1 失效场景识别：早期亏损 + 模式未经历完整周期 → DCF 可算但置信度低
- valuation-relative 的 §8.1 失效场景识别：全球 pure-play LLM 无对标 → 不用相对估值
- **退路**：
  1. DCF 给定性情景（乐观/中性/悲观），标注"估值置信度低，IPO 短期交易为主"
  2. 用 hk-ipo-arbitrage 做短期套利评估
  3. 不给长期持有建议（路径 C 不适用）

**预期输出字段**：
- [ ] 明确标注"估值不适用"或"置信度低"
- [ ] 不硬凑对标池（美股同类或其他 AI 公司都不构成真对标）
- [ ] 不给单点目标价
- [ ] 给出"IPO 短期套利 + 长期观察 T+12M"的分层策略

**失败判定**：
- 硬套 DCF 给具体价格（假设太多失真）
- 用"美股 AI Lab" 作为对标池（商业模型和市场不同）
- 不识别失效场景，按常规 framework 走

---

## 用例 7：Direct Listing 边界（Coinbase 2021-04）

**命题**：Coinbase COIN 2021-04 直接上市，参考价 $250，首日开盘 $381，打不打？

**预期路由**：
- 套路 A + 套路 C
- 加载 `us-ipo-arbitrage`（主，§9.2 Direct Listing 分支）+ `valuation-dcf`（加密公司估值）

**预期行为**：
- us-ipo-arbitrage §9.2 识别：Direct Listing，无 Lockup 或极短 Lockup
- 路径 A 简化为"等待风险偏好变化 / 估值回归"，不是 T+180 Lockup
- 流通量从 T0 就接近全流通，首日波动更大
- 仓位上限降低

**预期输出字段**：
- [ ] 明确识别"Direct Listing" 非传统 IPO
- [ ] 说明无 Lockup 对路径 A 的影响
- [ ] 不用 IPO 区间提价评估（无初始区间）
- [ ] 给出"首日波动观察 + T+30 / T+90 分批"方案
- [ ] 强调宏观判断（加密周期 + 加息周期）

**失败判定**：
- 把 Direct Listing 当传统 IPO 套 → 规则错
- 建议追涨首日 $381 → 高位 FOMO
- 不考虑宏观周期 → 2021-04 加息预期已抬头

---

## 用例 8：自上而下宏观驱动命题（0.3.0 补充）

**命题**：现在 Fed FFR 5.25%，美股哪些行业值得投？

**预期路由**：
- 跨套路 D + 宏观配置
- 加载 `top-down-selection`（主）+ `ai-thematic-investing`（主题叠加）→ 推荐赛道池 → `stock-selection` Top-N

**预期加载信号**：
```
framework_loaded: [top-down-selection, ai-thematic-investing, stock-selection]
```

**预期输出字段**：
- [ ] 市场定位（美股）+ 主锚（Fed / 美元 / 美经济）
- [ ] **加息降息预期扫描**（CME FedWatch / Fed Dot Plot / 2Y-10Y 曲线）
- [ ] 宏观 5 维扫描（利率 / 通胀 / 经济 / 地缘 / 政策）
- [ ] 周期阶段判断（"繁荣尾部 → 衰退前夜 过渡期"）
- [ ] 板块评分 + 配置权重
- [ ] **主题 vs 宏观博弈**（AI 主题超配修正）
- [ ] 核心超配 / 战术平配 / 防御底仓 / 避雷 四档清单
- [ ] 交棒 stock-selection 筛个股

**失败判定**：
- 只看当前利率不看预期 → 违反"股市炒预期"最高原则
- 纯宏观思维忽视 AI 主题 → 错过超额收益
- 不做周期阶段判断就给配置 → 无锚
- 配置权重合计不到 100% 或单板块超 50% → 违反纪律

---

## 用例 9：五年规划 / 政策驱动命题（A 股）

**命题**：十五五规划即将发布（2026-03 两会），哪些 A 股赛道值得提前布局？

**预期路由**：
- 套路 B（政策事件）+ 套路 D（赛道）
- 加载 `top-down-selection`（§4.5.1 中长期结构性政策 + §4.5.4 政策前瞻节奏）

**预期输出字段**：
- [ ] 市场定位（A 股 → 政策驱动权重提高）
- [ ] 政策监管维度专门扫描（§4.5.1 / §4.5.2 / §4.5.4）
- [ ] **"股市炒预期"**应用：T-6 到 T0 是买入甜蜜点
- [ ] 可预判的十五五战略方向（新质生产力 / 制造升级 / 绿色低碳 / 供应链安全）
- [ ] 每个方向给 2-3 个候选赛道
- [ ] 配置权重 + 执行时点（建议 2025-Q4 起分批建仓）
- [ ] 政策落地后 T+3 / T+12 / T+24 兑现节奏

**失败判定**：
- 等规划正式发布才动手 → 追高（预期已 price in）
- 不跟踪"政府工作报告 / 中央经济工作会议 / 征求意见稿"信号 → 错过前瞻窗口
- 把 2021 双减经验套到所有 A 股政策 → 不区分结构性 vs 节奏性
- 一次定 5 年配置不调整 → 违反"预期滚动更新"

---

## 汇总检查表

每次回归后统计：

| 项 | 状态 |
|---|------|
| 4 个新 framework 都能被正确触发 | [ ] |
| 2 个新 template 都能正确产出 | [ ] |
| 跨 framework 组合加载顺序正确 | [ ] |
| 失效场景能识别并退路 | [ ] |
| 决策卡 9 要素齐全（每次输出） | [ ] |
| 反面证据 ≥ 3 条 | [ ] |
| 悲观概率 ≥ 20% | [ ] |
| 所有 Worked Example 数据不矛盾 | [ ] |
| Disclaimer 齐全 | [ ] |

---

## 后续扩展

**0.3.0 时补充用例**：
- fund-analysis 基金分析命题
- bond-analysis 债券命题

**1.0.0 里程碑**：
- 20 个真实命题回归集
- 每个用例含实际跑分结果（LLM-as-judge rubric）
- 6 个月命中率统计（self-improvement-loop）

---

## 版本 / 变更记录

| 日期 | 变更 |
|------|------|
| 2026-04-23 | 首版（0.2.0）。7 个用例覆盖 4 个新 framework + 跨 framework 组合 + 失效场景 |
