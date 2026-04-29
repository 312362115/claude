# 复盘：finance-analysis skill 0.1.0 → 0.3.0 完整迭代 — 2026-04-23

> 关联 backlog：[finance-analysis skill](../backlog/2026-04-20-finance-analysis-skill.md) / [top-down-selection](../backlog/2026-04-23-top-down-selection.md)
> 关联 spec：[0.2.0 frameworks spec](../specs/2026-04-23-finance-analysis-0.2.0-frameworks.md)
> 关联 plan：[0.2.0 plan](../plans/2026-04-23-finance-analysis-0.2.0-plan.md)
> 关联 PR：#17（13 个 commit 从 0.1.0 到 0.3.0）
> 关联分支：`feat/finance-analysis-skill`

---

## 需求概述

- **目标**：从零构建一个覆盖 A / 港 / 美三地投资决策的结构化金融分析 skill，支持股票 / 基金 / 债券 / IPO 打新 / 主题投资 / 宏观配置 / 自我迭代闭环。
- **结果**：
  - 11 个 framework（4923 行方法论）
  - 9 个 template（2262 行）
  - 完整 finance-journal 闭环目录 + INDEX 守护机制
  - 9+ 回归测试用例
  - 总计 ~7500 行沉淀
- **过程顺利度**：⭐⭐⭐⭐（4/5，非常顺利，仅 long-form context 偶有疲态）
- **时间跨度**：2026-04-17 群核 IPO 触发 → 2026-04-23 0.3.0 收官（约 1 周密集）

---

## 做得好的（保持）

### 1. 按版本渐进交付，不求一口气做完
0.1.0 → 0.2.0 → 0.3.0 每个版本边界清晰，每个版本独立交付 + 独立 commit。避免"改 1 个月憋大招"的反模式。

**关键经验**：**单 skill 的迭代版本可以放同一 PR**（PR #17 累计 13 commit 也不拆分），已沉淀到 `feedback_pr_scope.md`。

### 2. 核心原则贯穿全篇
每个 framework 开头都有 🔥 **最高原则** 段，从根本认知层面约束方法论：
- command-driven：股市炒预期 + Alpha 在执行
- valuation-relative/dcf：三情景 + 概率加权
- top-down-selection：预期驱动而非当前数据
- fund-analysis：买管理人不是买排名
- bond-analysis：不是保本，是利率 + 信用的 bet

这让 framework 从"查手册工具"升级成"认知传递"。

### 3. Worked Example 全部真实案例
- 东山精密（0.1.0 / 0.2.0 主线案例）
- NVDA 2023 / 2024（DCF + 踏空归因）
- TSLA / CATL / 群核 0068.HK
- DoorDash 2020 美股 IPO
- TLT 2022-2024 债券周期

真实案例 + 事后回溯 让 framework 可验证 + 可学习，不是空谈。

### 4. 强制可证伪预判（4 维时点）
所有决策卡都要求 T+3 / T+6 / T+12 / T+24 可证伪预判，不是"长期看好"式废话。

### 5. 规范实测校准
`_index.md` 原要求 framework 800-1500 行，实际落地后发现 400-600 行最合理。**主动校准规范**而不是硬凑，避免注水。

### 6. 用户中途补强能迅速吸收
- 用户说"十五五规划"→ 立即补到 top-down §4.5.1
- 用户说"加息降息预期"→ 补 §4.1.2
- 用户说"股市炒预期"→ 顶到"最高原则"
- 用户说"INDEX 应该触发守护检查"→ 立即重构 INDEX 为主动守护节点

方向调整快，不僵化按原计划。

### 7. self-improvement-loop 从"纸面"到"可运转"
- 识别原 framework Phase 2/3 未落地的问题
- 补齐 decision-postmortem + quarterly-performance 两个关键 template
- 加套路 E 路由 + SKILL.md 触发词
- INDEX 主动守护检查机制（4 类扫描）

**这是最有价值的改进**：机制从 4/10 → 8/10 可执行性。

---

## 做得不够好的（优化）

### 1. 前期对焦有反复（但纠正很快）
**现象**：stock-selection vs alpha-generation 的边界曾经模糊过（选股 vs 方法论的边界），让用户选了一次 "stock-selection = alpha-generation 可执行简化版"。

**原因分析**：我在 spec 里假设性地设计边界，没一开始就把"alpha 是方法论 / stock-selection 是可执行流程"这条硬约束写清。

**改进**：**新建 framework 前先列和相邻 framework 的"边界 + 不重复内容"**，不要造重复。

### 2. 长度规范最初没校准
0.2.0 Spec 写了"800-1500 行"（照搬 _index.md 原规范），对焦时才发现实际 framework 都只有 380-555 行。好在对焦 Q1 问了这个，用户选 400-600 校准，避免了注水。

**改进**：**所有规范在新版本引用前要实测校准**，不照搬历史文档。

### 3. finance-journal 目录名反复
先叫 trading-journal → 用户说改名 → 选 finance-journal → 用户又说口误 "docs/trading-journal" 但实际是集中诉求 → 保留 finance-journal。

**原因分析**：命名决策没有充分权衡 "技术准确"（trading）vs "范围完整"（finance，含观望 / 基金配置）。

**改进**：**命名前先列"涵盖范围和排除范围"**，避免中途改名的 sed 重放工作。

### 4. self-improvement-loop 初版机制评估不到位
我最初写 self-improvement-loop.md 时标注 Phase 1 完成，但后来评估发现 Phase 1 的"SKILL.md 加复盘类触发词"根本没做（checklist 勾了但实际没执行）。

**原因分析**：自己给自己打勾有乐观偏差。Phase 2/3 没做还标"进行中"显然不可接受。

**改进**：**Phase checklist 必须有客观证据（文件存在 / 功能可验证）才能打勾**，不能"文档提到了就算"。

### 5. INDEX 守护机制是用户提醒才加的
用户一句"每次更新 INDEX 应该触发检查"才让我意识到 INDEX 应该是主动节点不是被动存储。这应该在设计 self-improvement-loop 时就想到。

**原因分析**：思维停留在"存储"视角，没跳到"守护"视角。

**改进**：**所有 INDEX 类文档都要问"谁来守护它跑起来"**，不能只考虑存储格式。

### 6. 部分 framework 写完没做实战验证
0.3.0 三个 framework 写完就 commit 了，用户跳过了"实战验证"环节。

**风险**：纸面规范的覆盖度≠实际调用的有效性。将来第一次真实触发时可能暴露问题。

**改进**：**至少一个 framework 应该在合并前跑一轮实战验证**，后续 framework 可以复用验证套路。

---

## 通用能力沉淀

### 1. "多 framework skill" 的组织模式

**proven pattern**：
```
SKILL.md （入口 + 触发词 + 命题路由）
├── command-driven-analysis.md （主流程，承接所有根本认知）
├── frameworks/_index.md （路由表 + 版本总结）
├── frameworks/<各专项>.md （每个 framework 9 要素）
├── templates/_index.md （决策卡入口）
├── templates/<各专项>.md （空白 + 填充示例双版）
└── references/integrations/ （可选增强）
```

每个 framework 9 要素：**核心定位 / 决策树 / 量化信号 / EV 评分 / Worked Example / 失效场景 / 执行纪律 / 相关 template / Disclaimer**。

### 2. 闭环机制设计原则

**4 层闭环**：
- L1 留档（纪律层）— 决策卡
- L2 验证（触发层）— 到期自动提醒
- L3 归因（学习层）— 错判归类
- L4 升级（进化层）— 累计触发 framework 修改

**关键**：L2 必须有**守护节点**（INDEX.md 主动扫描），否则依赖用户自律 = 必然失败。

### 3. "方向调整快"是 AI 协作强项

用户多次补强原则时，能在半小时内完成：
- 找到合适插入位置
- 改写多个文件保持一致性
- 更新索引和路由
- commit + push

这是 AI 特别适合的**分布式一致性更新**场景，比人类更适合。

### 4. "套路 A-E" 分类覆盖完整

| 套路 | 输入 | 输出 |
|-----|------|------|
| A 个股 | 股票名 | 决策卡 |
| B 政策事件 | 政策 | 影响标的表 |
| C 公司事件 | 财报 / 并购 | 事件解读 + 跟投清单 |
| D 主题赛道 | 赛道名 | 主题地图 + 标的排序 |
| E 自我迭代 | 历史决策 | 验证 / 归因 / KPI 报告 |

套路 E 和 A-D 是两种模式（分析 vs 闭环），不要混用。

---

## 行动项

### 立即做
- [x] 标 finance-analysis + top-down-selection backlog done
- [x] 更新 INDEX.md
- [x] 写本复盘文档
- [x] memory 沉淀（见下方）
- [ ] commit + push 本次变更

### 短期（未来 1-2 周）
- [ ] 实战跑一轮决策流程（选一个真实命题），验证 skill 能否按预期路由 + 输出
- [ ] 第一次跑出来可能暴露 framework 间衔接问题，做小修
- [ ] 开始填 finance-journal/（可以从补录历史决策开始）

### 中长期（0.4.0）
- [ ] event-driven framework（财报漂移 / 并购套利 / 指数纳入 / 激进投资者跟随）
- [ ] technical framework（支撑压力 / 趋势 / 量价）
- [ ] macro-overlay framework（大类资产配置）

### 长期（1.0.0 里程碑）
- [ ] 20 个真实命题回归集
- [ ] 6 个月实战命中率 ≥ 60%
- [ ] 所有 framework 有"迭代日志"段记录升级历史

---

## 复盘总结

**最大的收获**：一个 skill 从"查手册工具"进化成"认知传递 + 执行闭环"需要三层设计：
1. **方法论层**（framework 内容）
2. **机制层**（finance-journal 目录 + INDEX 守护 + 套路 E 路由）
3. **原则层**（每个 framework 的 🔥 最高原则 段）

缺一层都不完整——只有方法论没机制就无法闭环，只有机制没原则就变成官僚填表，三层齐全才能真正落地。

**给未来 skill 迭代的启示**：
- 每轮版本边界要清晰
- 最高原则段是 skill 灵魂
- Worked Example 必须真实
- 闭环机制必须有守护节点
- PR 以 skill 为范围组织，不按 commit 数拆
- 规范要实测校准，不照搬
