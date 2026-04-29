---
priority: P1
status: done
spec: （简版，直接在本 backlog 内联）
plan: （简版，M1 一次交付）
retro: docs/decisions/2026-04-23-finance-analysis-0.3.0-retro.md
closed_at: 2026-04-23
---

# top-down-selection framework（自上而下选股）

## 背景

finance-analysis 0.1.0 + 0.2.0 完成后，选股路径主要是**自下而上**：
- `stock-selection.md` 入口是"已知赛道 + 池子"→ 4 步筛 → Top-N
- `ai-thematic-investing.md` 入口是"已知主题（AI）"→ 8 层产业链

**缺口**：用户不知道该看哪个赛道时，无法从宏观出发决定"现在该重仓哪些行业 / 板块"。

典型命题：
- "现在 Fed 利率 5% 环境下，哪几个行业值得投？"
- "M2 扩张期该超配哪些板块？"
- "通胀上行周期哪些赛道受益？"
- "特朗普关税政策下哪些行业受损 / 受益？"
- "A 股牛市初期应该怎么配置板块？"

这些命题需要从宏观变量出发，一直推到赛道 / 个股清单。

## 目标

新增 `frameworks/top-down-selection.md`：**宏观 → 行业 → 板块 → 赛道池**，输出"值得看的赛道清单"，交棒给 `stock-selection.md` 做个股筛选。

## 核心设计

```
[输入] 宏观命题
  ↓
Step 1 宏观变量扫描（5 维）
  ↓
Step 2 周期阶段判断（扩张 / 繁荣 / 衰退 / 复苏 / 滞胀 5 档）
  ↓
Step 3 行业轮动映射（不同阶段受益 / 受损行业）
  ↓
Step 4 板块评分（每个行业下的细分板块，用现价 vs 合理估值打分）
  ↓
Step 5 输出"推荐赛道池"+ 配置权重建议
  ↓
（交棒给 stock-selection）
```

### 宏观 5 维

1. **货币政策**：利率（Fed FFR / 央行 OMO / LPR / HKMA）+ 流动性（M2 / SLF / 逆回购）+ 资产负债表
2. **通胀 + 大宗商品**：CPI / PPI / 原油 / 铜 / 黄金
3. **经济周期**：GDP / PMI / 就业 / 消费 / 投资数据
4. **地缘政治**：贸易战 / 关税 / 制裁 / 供应链安全
5. **政策监管**：消费刺激 / 股市政策 / 特定行业规管（A 股尤其重要）

### 市场适配

- **美股**：Fed 驱动 + 美国经济周期 + 财政赤字 + 美元指数
- **港股**：美联储 + 内地政策 + HKMA 联系汇率 + 南向资金
- **A 股**：央行货币政策 + 经济周期 + 政策监管 + 外资 / 内资情绪
- **跨市场**：美元周期 / 加息降息 / 地缘冲击 → 全球联动

### 周期阶段 → 板块轮动

```
复苏期（利率低 + PMI 回升）：消费 / 周期股 / 金融启动
扩张期（利率稳 + 经济增长）：成长股 / 制造业 / 科技
繁荣期（利率升 + 通胀升）：能源 / 工业金属 / 银行
衰退期（利率降 + 经济差）：必需消费 / 医疗 / 公用事业
滞胀期（利率高 + 经济差）：黄金 / 能源 / 必需消费
```

## 不在本轮范围

- **板块到个股的深度研究**：交棒 `stock-selection`
- **具体估值计算**：交棒 `valuation-*`
- **自建经济数据库**：Tier 2 能力，不本轮做
- **量化择时**：非决策导向，不做

## 验收标准

- [ ] `frameworks/top-down-selection.md` 落地（400-600 行，9 要素齐全）
- [ ] 含宏观 5 维扫描 + 5 周期阶段 + 行业轮动映射表
- [ ] 跨市场适配（A / 港 / 美 各自宏观锚）
- [ ] Worked Example：选一个真实宏观时点做完整推演（建议 "2024-2025 高利率周期下美股板块配置"）
- [ ] 明确和 stock-selection / ai-thematic-investing 的边界和协作
- [ ] SKILL.md / _index.md 加入新 framework
- [ ] 回归测试补 1-2 个宏观驱动命题用例

## 版本归属

作为 finance-analysis 0.3.0 第一项（原 0.3.0 计划是基金 + 债券，现追加本项）。

## 关联

- finance-analysis 0.2.0 backlog：`docs/backlog/2026-04-20-finance-analysis-skill.md`
- 前置认知：`command-driven-analysis.md` §"股市是预期驱动" + §"时间维度可预测性"
- 下游 framework：`stock-selection.md`（入口交棒）
- 平行 framework：`ai-thematic-investing.md`（主题驱动 vs 宏观驱动）

## 进度

- 2026-04-23：启动，backlog 创建
- 下一步：直接写 framework，一次 commit 交付
