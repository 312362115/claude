# Finance Journal Index

> 金融决策记录索引。所有投资决策卡 / 验证报告 / 错判归因的入口。
>
> **维护规则**：新建决策、状态变更、完成验证、做完归因 → 立即更新本文件。
>
> **关联 skill**：`finance-analysis` skill 的 self-improvement-loop framework。

---

## 状态标记

| 标记 | 含义 |
|------|------|
| `[?]` | watchlist — 观察中，未入场 |
| `[~]` | active — 持仓中 |
| `[x]` | closed — 已平仓，正收益退出 |
| `[!]` | stopped-out — 触发止损退出 |
| `[-]` | skip — 决定不做（也要留档） |
| `~~...~~` | dropped — 决策取消 |

## 动作标签

| 标签 | 含义 |
|------|------|
| `buy` | 首次买入 / 建仓 |
| `add` | 加仓 |
| `trim` | 减仓 |
| `sell` | 清仓 |
| `hold` | 继续持有（定期确认） |
| `skip` | 分析后决定不做 |
| `watchlist-add` | 加入观察池 |
| `ipo` | 打新决策 |
| `fund` | 基金申赎 |

---

## 当前持仓 / 观察（Active Portfolio）

<!-- 所有 [~] active 和 [?] watchlist 决策列这里 -->
<!-- 格式：- [状态] [标的+动作](文件名) — 一句话描述（日期 / 现价 / 目标 / 止损）-->

<!-- 示例（空表示暂无）：
- [~] [NVDA buy](2026-05-22-NVDA-buy.md) — 2026-05-22 @ $285，目标 $520，止损 $200
- [?] [0700.HK watchlist](2026-04-20-0700HK-watchlist.md) — 等 Q2 财报
-->

（暂无 active 决策）

---

## 按时间归档

### 2026

#### 2026-04

<!-- 按日期降序 -->

（暂无决策卡）

---

## 待验证队列（To Verify）

<!-- 所有"验证日程到期但未完成"的项目 -->
<!-- skill 触发"复盘持仓"时扫这里 -->

（暂无到期验证）

---

## 错判归因清单（Postmortem）

<!-- 所有已完成归因的错判决策（链接到 postmortem/ 子目录）-->
<!-- 格式：- [D1/D2/D3/D4/D5] [标的](postmortem/YYYY-MM-DD-<ticker>-<D类型>.md) — 一句话教训 -->

### 按错判类型统计

| 类型 | 累计次数 | 累计后触发 framework 升级 |
|------|---------|------------------------|
| D1 数据源盲区 | 0 | 至 3 次触发升级 data-sources |
| D2 分析深度不够 | 0 | 至 3 次触发升级 command-driven / valuation |
| D3 预判不具体 | 0 | 至 3 次触发强化 template 可证伪性 |
| D4 执行纪律失控 | 0 | 至 3 次触发升级 alpha-generation |
| D5 认知盲点 | 0 | 至 3 次触发补主题 / 行业启发式 |

---

## 月度复盘

<!-- 每月最后一周用户可触发"月度复盘"，生成此类文件 -->
<!-- 格式：- [YYYY-MM](monthly/YYYY-MM.md) — 当月决策数 / 命中率 / 错判数 / 升级点 -->

（暂无）

---

## 季度 / 年度报告

<!-- 每季 / 每年的命中率报告，对应 self-improvement-loop framework KPI -->
<!-- 格式：- [YYYY-QN](quarterly/YYYY-QN.md) / [YYYY](yearly/YYYY.md) -->

（暂无）

---

## 维护指引

### 什么时候更新本 INDEX

| 事件 | 更新位置 |
|------|---------|
| 新建决策卡 | "当前持仓 / 观察" + "按时间归档" |
| 决策状态变更（active → closed 等） | 改状态标记 |
| 完成 T+3 / T+6 / T+12 / 终局 验证 | "待验证队列"移除 + 原卡勾选 |
| 发生错判并归因 | "错判归因清单"追加 + 累计次数 +1 |
| 累计 3 次同类错判 | 触发 framework 升级提醒 |
| 月底 | 生成 "月度复盘"并加入索引 |
| 季度末 / 年末 | 生成 "季度 / 年度报告" |

### 触发词对应动作

| skill 触发词 | INDEX 操作 |
|-------------|----------|
| "复盘持仓" | 扫"待验证队列" → 批量生成验证 |
| "复盘 <ticker>" | 按标的搜本 INDEX → 加载对应卡 + 数据 |
| "错判归因" | 追加"错判归因清单" + 累计次数 |
| "framework 升级审查" | 检查累计次数表，任一 ≥ 3 列出对应错判案例 |
| "命中率统计" | 从本 INDEX + 月度文件汇总计算 |

### 目录结构（所有金融分析产出集中在此）

```
docs/finance-journal/
├── INDEX.md                            ← 本文件（统一索引）
│
├── YYYY-MM-DD-<ticker>-<动作>.md        ← L1 决策卡（扁平）
├── YYYY-MM-DD-<ticker>-verify-T+N.md   ← L2 验证报告（扁平）
│
├── postmortem/                         ← L3 错判归因 + 成功经验复盘
│   ├── YYYY-MM-DD-<ticker>-<D类型>.md       # 错判
│   └── YYYY-MM-DD-<ticker>-success.md       # 成功经验
│
├── research/                           ← 命题分析报告（未产出决策 / 深度研究）
│   └── YYYY-MM-DD-<ticker>-analysis.md
│
├── monthly/                            ← 月度汇总
│   └── YYYY-MM.md
│
└── quarterly/                          ← 季度 / 年度命中率
    └── YYYY-QN.md
```

**原则**：金融分析相关所有产出全部集中在 `docs/finance-journal/`，不分散到 `docs/decisions/`（后者是 CLAUDE.md 的项目开发复盘目录）。
