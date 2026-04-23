# Spec：finance-analysis skill 0.2.0 — Framework 扩展

> **关联**：backlog `docs/backlog/2026-04-20-finance-analysis-skill.md` / plan `docs/plans/2026-04-23-finance-analysis-0.2.0-plan.md`

---

## 一、背景与动机

**提出方**：用户（2026-04-23 对焦）
**约束**：跟随 finance-analysis skill 0.1.0 → 0.2.0 路线图；无外部 deadline；此轮 4 个 framework 一次交付

最近 12 个 commit 在 `command-driven-analysis.md` 里沉淀了大量认知升级：
- 股市是**预期驱动**，不是当前业绩（东山精密重估案例）
- **情景分析 + 概率加权**是估值正确方法（取代静态 PE 对标）
- **时间维度可预测性**（短期不测、长期可测）
- 4 条铁律 + 递归下钻

这些方法论需要承接到专门的估值/选股 framework 里，否则主入口会继续膨胀（现已 1316 行），而"怎么算估值"这种高频命题仍然 fallback 到通用推演，结论质量不稳定。

---

## 二、现状分析

### 当前 framework 矩阵

| 命题 | 对应 framework | 覆盖情况 |
|------|--------------|---------|
| "XX 股值不值买？" | command-driven-analysis + alpha-generation | ⚠️ 部分覆盖，缺估值专用流程 |
| "XX 股现在贵不贵？" | command-driven-analysis | ⚠️ 只有主入口提及，无统一执行模板 |
| "从 A 股科技股里选 3 只？" | alpha-generation | ⚠️ 方法论层，无可执行筛选清单 |
| "DoorDash 打不打？" | hk-ipo-arbitrage（误用） | ❌ 美股规则不同，会给错结论 |
| "AI 赛道哪家好？" | ai-thematic-investing | ✅ 已覆盖 |
| "港股 X 打不打？" | hk-ipo-arbitrage | ✅ 已覆盖 |

### 现有 framework 长度校准

```
command-driven-analysis.md   1316 行  ← 主入口（含主方法论大量沉淀）
ai-thematic-investing.md      555 行
alpha-generation.md           478 行
hk-ipo-arbitrage.md           389 行
self-improvement-loop.md      382 行
```

_index.md 原写"800-1500 行"从未达到。**校准后实际指标：400-600 行/framework**。

### 痛点

1. **估值命题**：每次都要重新组织"情景分析 + 概率加权"的论述结构，无模板
2. **选股命题**：alpha-generation 讲"5 执行差"方法论，但用户触发"帮我筛出 X 只"时缺清单化产出
3. **美股 IPO**：用 HK 规则判美股会误导（暗盘机制、首日锁仓、定价机制、披露文件全不同）
4. **templates 缺口**：valuation-card / stock-screening-card 未落地，决策卡不统一

---

## 三、调研与备选方案

### Framework 1：valuation-relative（相对估值）

**核心问题**：用 PE/PS/PB 和同业对比，XX 股现在贵不贵？合理区间多少？

**关键设计决策**：
- **不做静态 PE 对标**：承接"股市是预期驱动"认知，引入**前瞻 PE（Forward PE）**和**情景分析**
- **对标池构建**：不是拉名单，而是按"商业模型同质度 + 成长阶段同步"筛 3-5 家真对标
- **三情景 + 概率加权**作为核心输出（乐观/中性/悲观），不给单点目标价

**决策树骨架**：
```
命题：XX 股相对估值如何
├─ Step 1：商业模型分类 → 决定用 PE / PS / PB 哪个主估值
├─ Step 2：对标池构建（3-5 家，通过"同模型+同阶段"两重过滤）
├─ Step 3：对标的 PE/PS/PB 分布 + 中位数
├─ Step 4：三情景下 XX 股的 forward EPS/Revenue
├─ Step 5：三情景 × 合理 PE → 目标市值 × 概率加权 → 期望价
├─ Step 6：加主题溢价因子（1.0-1.5x，有明确触发条件）
└─ Step 7：输出"隐含预期位置"+ 盈亏比
```

**Worked Example**：**东山精密**（现价 186 元 vs 概率加权 100-140 元）— 复用 command-driven-analysis 里的沉淀，展示"静态 PE 248x 思维错在哪 / 正确做法产出什么"

**长度估算**：500-600 行（决策树 + 公式 + Worked Example 完整推导）

---

### Framework 2：valuation-dcf（DCF 估值）

**核心问题**：成长期公司用 PE/PS 失真，怎么用 DCF 算？

**关键设计决策**：
- **只讲三情景 DCF，不讲单点 DCF**：单点 DCF 输入假设过敏感，没有意义
- **关键假设透明化**：营收增长（3/5/10 年分段）/ 毛利率演进 / WACC / 终值倍数
- **敏感性分析必选**：必须列"关键假设变 ±10% 对应股价 ±X%"
- **不算到小数点后 N 位**：决策导向，给区间不给精确值

**决策树骨架**：
```
命题：XX 成长股合理价
├─ Step 1：判断适用性（成长期 + 现金流为正或近正 + 可预测性 T+24）
├─ Step 2：收入假设（三情景：乐观/中性/悲观，5 年显式预测 + 终值）
├─ Step 3：利润率演进路径（毛利率阶梯 + 经营杠杆）
├─ Step 4：自由现金流 = EBIT × (1-tax) + D&A - CapEx - ΔWC
├─ Step 5：WACC 确定（beta + risk-free + equity premium）
├─ Step 6：终值倍数（Gordon 或出口倍数）
├─ Step 7：三情景 NPV × 概率权重 → 期望价
└─ Step 8：敏感性分析（WACC/营收增速/终值倍数 各 ±10%）
```

**Worked Example**：**NVDA 2023 成长期 DCF**（或 **TSLA 2020-2021 高成长期**）— 展示"关键假设怎么给 / 三情景差多少 / 敏感性在哪"

**长度估算**：500-600 行

---

### Framework 3：stock-selection（选股简化版）

**核心问题**：从某赛道/某池子里，用可执行流程筛出 N 只待研究股

**关键设计决策**：
- **定位 alpha-generation 的可执行简化版**（已确认）
- **4 步筛选器**：赛道 → 龙头 → 质量 → 成长
  - 赛道筛：符合主题 / 非夕阳 / 可验证 TAM
  - 龙头筛：市占率 Top 3 或有明确"Layer 卡位"
  - 质量筛：ROE > 阈值 / 现金流健康 / 无大额商誉
  - 成长筛：近 3 年营收/利润复合增速 + 前瞻指引
- **产出"待研究清单"**，不直接产出买入清单（保留深度研究环节）
- **必须输出 30/60/100 打分**，排序给出 Top-N

**决策树骨架**：
```
输入：赛道关键词 + 池子（如 "A 股 AI 算力" 或 "纳斯达克 100"）
├─ Step 1：赛道边界定义（明确"什么算属于这个赛道"）
├─ Step 2：候选集构建（从交易所 / 指数成分股 / 产业链图谱扫）
├─ Step 3：4 步筛选（赛道 / 龙头 / 质量 / 成长，每步可筛掉 50%+）
├─ Step 4：30/60/100 分打分（每个维度 25 分）
├─ Step 5：排序输出 Top-N 待研究清单
└─ Step 6：对每只 Top 标注"下一步研究方向"（估值 / 产业链位置 / 催化剂）
```

**Worked Example**：**CATL**（从"A 股动力电池"筛出：赛道龙头 + ROE + 成长全绿，vs 同行国轩/欣旺达分数差异）— 展示 4 步筛选的具体动作

**长度估算**：400-500 行（方法论层较薄，核心是可执行清单）

---

### Framework 4：us-ipo-arbitrage（美股 IPO）

**核心问题**：美股 IPO 首日能不能打、中长期怎么判？规则和港股差多少？

**关键设计决策**：
- **对照港股写差异**，不重新讲一遍 IPO 基础
- **核心差异点**：
  - 定价机制（簿记建档 vs 绿鞋机制）
  - 披露文件（S-1 / 424B4 vs HK 招股书）
  - 首日机制（无暗盘 / 无孖展 / 开盘价由 NYSE specialist 撮合）
  - 锁仓期（Lock-up 180 天 vs 港股无统一规则）
  - 打新渠道（IB / 富途等券商分配 vs HK 一人一手）
- **ev 模型调整**：美股散户基本分不到，所以 EV 算的是"首日追涨 / 等回调 / 长期持有"三种路径比较，不是"打不打"

**决策树骨架**：
```
命题：XX 美股 IPO（如 DoorDash / Coinbase）
├─ Step 1：S-1 核心数据提取（营收/亏损/用户数/商业模型）
├─ Step 2：定价区间评估（承销商底价 vs 提价次数 → 投资人需求温度）
├─ Step 3：Lockup 180 天后流通量 → 抛压时点预判
├─ Step 4：首日机制风险（开盘价 vs 盘中价差，常见 20-50% 跳空）
├─ Step 5：三条路径对比：
│   ├─ 路径 A：不参与首日，等 Lockup 后回调（多数情况 EV 更高）
│   ├─ 路径 B：首日追涨（高风险，仅当极热需求时）
│   └─ 路径 C：长期持有（≥2 年，回归基本面）
└─ Step 6：输出路径选择 + 触发条件 + 止损位
```

**Worked Example**：**DoorDash（2020-12）** 或 **Coinbase（2021-04）** — 公开案例，展示首日跳空 + Lockup 抛压 + 一年后价格对比

**长度估算**：500-600 行

---

### 备选方案（已放弃）

| 方案 | 结论 | 原因 |
|------|------|------|
| 延后 us-ipo 到 0.5.0 | ❌ 放弃 | _index.md 原设计把它和估值/选股列为 0.2.0 姐妹篇；一起做运行时更连贯（询问用户已确认） |
| 每 framework 写到 800-1500 行 | ❌ 放弃 | 现有 framework 从未达到，强行拉长会注水 + 重复 command-driven-analysis |
| stock-selection 做价值/成长两种 | ❌ 放弃 | 边界模糊，选了 "alpha-generation 简化版" 定位 |
| stock-selection 合并到 alpha-generation | ❌ 放弃 | 用户已明确要单独 framework |

---

## 四、决策与取舍

### 核心决策

1. **4 个 framework 一起交付**（valuation-relative / valuation-dcf / stock-selection / us-ipo-arbitrage），版本升 0.2.0
2. **长度 400-600 行/framework**（校准现状，不追求 _index.md 原规范的 800-1500 行）
3. **主要 Worked Example 复用最近讨论案例**（东山精密 / NVDA / TSLA / CATL / 群核 0068.HK）；美股 IPO 必要时补公开案例（DoorDash / Coinbase）
4. **stock-selection = alpha-generation 可执行简化版**（4 步筛选器 + 30/60/100 打分）
5. **us-ipo 独立 framework**，不扩展 hk-ipo（规则差异足够独立成篇）

### 放弃了什么

- **DCF 精细化**：不追求工程化 DCF 模型，只给三情景 + 敏感性方法论
- **选股自动化**：stock-selection 不做"一键扫全市场"（那是 Tier 2 能力），只给 4 步筛选清单
- **历史案例回溯**：不做 10 个案例混排，每个 framework 聚焦 1 个核心 Worked Example
- **中美 IPO 统一 framework**：规则差异太大，不硬塞

### 遗留风险

1. **context 压力**：4 个 framework 同时推进，一轮对话可能 token 压力大
   - **缓解**：按 framework 分 4 个 commit，每个独立 review
2. **Worked Example 数据回溯**：DoorDash / Coinbase 的 S-1 和首日走势需要准确
   - **缓解**：写入前用 WebSearch 确认关键数据点
3. **方法论重复**：valuation-relative 和 valuation-dcf 都会用到"情景分析 + 概率加权"
   - **缓解**：统一引用 command-driven-analysis 的小节，不重复展开；两 framework 聚焦各自独特流程

---

## 五、技术方案

### 5.1 文件清单

```
skills/finance-analysis/
├── SKILL.md                                    [改] 版本号 0.2.0 + 路线图表更新
├── VERSION                                     [改] 0.1.0 → 0.2.0
├── CHANGELOG.md                                [改] 新增 0.2.0 段落
└── references/
    ├── frameworks/
    │   ├── _index.md                           [改] 占位扩展表移除已完成项
    │   ├── valuation-relative.md               [新] 500-600 行
    │   ├── valuation-dcf.md                    [新] 500-600 行
    │   ├── stock-selection.md                  [新] 400-500 行
    │   └── us-ipo-arbitrage.md                 [新] 500-600 行
    └── templates/
        ├── _index.md                           [改] 补 2 个新 template
        ├── valuation-card.md                   [新] ~200 行
        └── stock-screening-card.md             [新] ~200 行

docs/
└── tests/
    └── finance-analysis-0.2.0.md               [新] 5+ 回归用例
```

### 5.2 每个 framework 的 9 要素规范（严格执行）

```
1. 核心定位（适用 / 不适用场景）
2. 决策树（末端可执行动作）
3. 量化信号（每节点可观测阈值）
4. EV 或评分模型（至少 1 个数学模型）
5. Worked Example（真实案例完整推导）
6. 失效场景（何时本 framework 不适用）
7. 执行纪律（最容易翻车的环节）
8. 相关 template 指向
9. Disclaimer（方法论 ≠ 预测）
```

### 5.3 与现有 framework 的衔接

```
命题路由（command-driven-analysis 里更新）：
"XX 股值不值"          → valuation-relative（主）+ valuation-dcf（辅）
"合理价区间"           → valuation-relative 或 valuation-dcf（看商业模型）
"从 XX 赛道筛 N 只"    → stock-selection
"美股 IPO / DoorDash"  → us-ipo-arbitrage
```

### 5.4 SKILL.md 更新要点

- frontmatter 版本号 0.1.0 → 0.2.0
- 路线图表格：0.2.0 从"待做"改为"✅ 本版"
- 主入口段落简要提及新 framework 能力
- 触发词按需补充（可能需要加"合理估值 / DCF / 筛选 / 美股 IPO / DoorDash"等）

### 5.5 回归测试（docs/tests/finance-analysis-0.2.0.md）

**至少 5 个用例**：
1. 相对估值命题：用东山精密实例验证三情景 + 概率加权产出
2. DCF 命题：用 NVDA/TSLA 任一验证敏感性分析完整
3. 选股命题：用 "A 股 AI 算力" 验证 4 步筛选 + 打分输出
4. 美股 IPO 命题：用 DoorDash / Coinbase 验证 S-1 + Lockup + 三路径对比
5. 跨 framework 组合：如 "CATL 现在值不值" 触发 valuation-relative + stock-selection 组合加载

---

## 六、风险与边界

### 风险

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| context 压力导致后续 framework 质量下降 | 中 | 高 | 分 4 commit，每个独立 review，中间可中止 |
| Worked Example 历史数据记错 | 中 | 中 | 写入前 WebSearch 验证关键数据点 |
| 方法论重复（两 valuation framework） | 中 | 低 | 聚焦差异：relative 讲对标池 + 静态市场比较；dcf 讲未来现金流折现 |
| 4 个都做完但用户觉得有冗余 | 低 | 中 | review 检查点设在 spec + plan，不到 framework 写完才发现 |

### 不做

- fund-analysis / bond-analysis / event-driven / technical（0.3.0+）
- 回测工具 / 量化筛选工具（Tier 2，不在本 skill）
- 期权策略 / 日内技术分析（定位不符）
- 中美 IPO 对比通用 framework（各自独立即可）

### 边界

- 只做"决策框架"和"方法论"，不替用户做投资决策（所有 framework 必须有 Disclaimer）
- 数据源复用 deep-research 的 finance.yaml + blacklist.yaml，不在本 skill 内重复沉淀源
- 不做定时触发 / 自动扫描（skill 定位手动触发）

---

## 七、验收标准（对齐 backlog）

- [ ] 4 个 framework 文件落地，长度 400-600 行（±100 浮动可接受）
- [ ] 每个 framework 包含 9 要素
- [ ] 2 个新 template（valuation-card / stock-screening-card）落地
- [ ] docs/tests/finance-analysis-0.2.0.md 含 5+ 回归用例
- [ ] SKILL.md / VERSION / CHANGELOG / frameworks/_index.md / templates/_index.md 同步更新
- [ ] 所有 Worked Example 数据已校对
- [ ] 不破坏 0.1.0 现有 framework 的引用关系（命题路由向下兼容）
