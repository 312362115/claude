# finance-analysis 0.2.0 开发计划

## 关联

- 方案：`docs/specs/2026-04-23-finance-analysis-0.2.0-frameworks.md`
- backlog：`docs/backlog/2026-04-20-finance-analysis-skill.md`（P1，status=in-progress）

## 总览

```
M1 相对估值（valuation-relative + valuation-card）     1 commit
M2 DCF 估值（valuation-dcf，复用 valuation-card）      1 commit
M3 选股（stock-selection + stock-screening-card）      1 commit
M4 美股 IPO（us-ipo-arbitrage）                        1 commit
M5 收尾（SKILL + VERSION + CHANGELOG + _index + 测试） 1 commit
```

每个 milestone 独立 commit + 可中止，避免 context 压力累积。

---

## 子任务

### M1 — 相对估值 framework

- [x] 1. 写 `frameworks/valuation-relative.md`
  - 做什么：相对估值 framework（9 要素完整）
  - 涉及：`skills/finance-analysis/references/frameworks/valuation-relative.md`（新建，500-600 行）
  - 核心内容：商业模型分类 → 对标池构建 → 三情景 × 合理 PE → 概率加权 → 主题溢价 → 隐含预期位置
  - Worked Example：东山精密（复用 command-driven-analysis 沉淀）
  - 验收：
    - [ ] 9 要素齐全（核心定位 / 决策树 / 量化信号 / EV 评分 / Worked Example / 失效场景 / 执行纪律 / 相关 template / Disclaimer）
    - [ ] 长度 500-600 行
    - [ ] 决策树末端是可执行动作（输出决策卡）
    - [ ] Worked Example 数据和 command-driven-analysis 里的东山精密段落一致（不矛盾）

- [x] 2. 写 `templates/valuation-card.md`
  - 做什么：估值决策卡，通用模板（覆盖相对估值 + DCF 三情景）
  - 涉及：`skills/finance-analysis/references/templates/valuation-card.md`（新建，~200 行）
  - 核心字段：三情景表格 / 概率权重 / 期望价 / 盈亏比 / 隐含预期位置 / 关键假设列表 / 敏感性（DCF 用）/ 买卖触发
  - 验收：
    - [ ] 一张卡适配两个估值 framework（valuation-relative 和 valuation-dcf）
    - [ ] 包含空白填写版（用户可复制使用）
    - [ ] 提供 1 个填充示例（东山精密）

- [x] 3. M1 commit
  - commit msg：`feat(finance-analysis): 0.2.0 M1 - valuation-relative framework + valuation-card`

---

### M2 — DCF 估值 framework

- [x] 4. 写 `frameworks/valuation-dcf.md`
  - 做什么：DCF 估值 framework（三情景 + 敏感性必选）
  - 涉及：`skills/finance-analysis/references/frameworks/valuation-dcf.md`（新建，500-600 行）
  - 核心内容：适用性判断 → 三情景收入假设 → 利润率演进 → FCF 公式 → WACC → 终值 → NPV 概率加权 → 敏感性 ±10%
  - Worked Example：NVDA 2023 成长期 DCF 或 TSLA 2020-2021（write 前 WebSearch 核对关键数据）
  - 验收：
    - [ ] 9 要素齐全
    - [ ] 长度 500-600 行
    - [ ] 敏感性分析段不可省
    - [ ] 和 valuation-relative 的重叠内容用引用代替重复展开
    - [ ] 明确"什么情况应该用 DCF，什么情况不应该用"（适用性判断）

- [x] 5. 扩展 `valuation-card` 增加 DCF 专用字段（如 WACC / 终值倍数 / 敏感性表格）
  - 做什么：在 M1 的 valuation-card 基础上加 DCF 专属段
  - 涉及：`skills/finance-analysis/references/templates/valuation-card.md`（改）
  - 验收：DCF 填充示例（NVDA 或 TSLA）跑通，三情景 + 敏感性完整

- [x] 6. M2 commit
  - commit msg：`feat(finance-analysis): 0.2.0 M2 - valuation-dcf framework + valuation-card 扩展`

---

### M3 — 选股 framework

- [x] 7. 写 `frameworks/stock-selection.md`
  - 做什么：alpha-generation 可执行简化版，4 步筛选器 + 30/60/100 打分
  - 涉及：`skills/finance-analysis/references/frameworks/stock-selection.md`（新建，400-500 行）
  - 核心内容：赛道边界 → 候选集构建 → 4 步筛（赛道/龙头/质量/成长）→ 30/60/100 打分 → Top-N 输出
  - Worked Example：CATL（"A 股动力电池"筛选，对比国轩/欣旺达的得分差异）
  - 验收：
    - [ ] 9 要素齐全
    - [ ] 长度 400-500 行
    - [ ] 4 个筛选节点每个都有可观测阈值（不是主观判断）
    - [ ] 明确和 alpha-generation 的边界（alpha 讲方法论，本 framework 讲可执行流程）
    - [ ] 产出"待研究清单"而非"买入清单"，保留深度研究环节

- [x] 8. 写 `templates/stock-screening-card.md`
  - 做什么：选股筛选卡（候选集 → 4 步筛结果 → 30/60/100 打分表 → Top-N）
  - 涉及：`skills/finance-analysis/references/templates/stock-screening-card.md`（新建，~200 行）
  - 验收：
    - [ ] 空白版 + CATL 填充示例各 1
    - [ ] 打分表四维度（赛道 25 / 龙头 25 / 质量 25 / 成长 25）

- [x] 9. M3 commit
  - commit msg：`feat(finance-analysis): 0.2.0 M3 - stock-selection framework + stock-screening-card`

---

### M4 — 美股 IPO framework

- [x] 10. 写 `frameworks/us-ipo-arbitrage.md`
  - 做什么：美股 IPO framework，对照港股写差异
  - 涉及：`skills/finance-analysis/references/frameworks/us-ipo-arbitrage.md`（新建，500-600 行）
  - 核心内容：S-1 核心数据 → 定价区间评估 → Lockup 抛压 → 首日机制 → 三路径对比（不参与等 Lockup / 首日追涨 / 长期持有）
  - Worked Example：DoorDash（2020-12）或 Coinbase（2021-04），需写入前 WebSearch 核对：发行价 / 首日开盘价 / 首日收盘价 / Lockup 到期日价格 / 一年后价格
  - 验收：
    - [ ] 9 要素齐全
    - [ ] 长度 500-600 行
    - [ ] 和 hk-ipo-arbitrage 的差异点列清晰（表格对照）
    - [ ] EV 计算调整为"三路径期望值比较"，不是"打不打"
    - [ ] Worked Example 数据经核对准确

- [x] 11. M4 commit
  - commit msg：`feat(finance-analysis): 0.2.0 M4 - us-ipo-arbitrage framework`

---

### M5 — 收尾（SKILL + 版本 + 测试 + 索引）

- [x] 12. 更新 SKILL.md（版本 + 路线图 + 触发词 + 命题路由）
  - 涉及：`skills/finance-analysis/SKILL.md`
  - 做什么：
    - frontmatter `version: 0.2.0`
    - 路线图表格 0.2.0 从"待做"→"✅ 本版"
    - 4 类命题表补充新 framework 的触发条件
    - 触发词按需补充（"合理估值 / DCF / 筛选 / 美股 IPO / DoorDash / Coinbase"）
  - 验收：
    - [ ] 版本号一致
    - [ ] 路由表能指向新 framework
    - [ ] 触发词能捕获估值/选股/美股 IPO 命题

- [x] 13. 更新 VERSION / CHANGELOG
  - 涉及：`skills/finance-analysis/VERSION`（改 0.1.0 → 0.2.0），`CHANGELOG.md`（新增 0.2.0 段落）
  - 验收：CHANGELOG 含 4 个新 framework + 2 个新 template + 回归测试说明

- [x] 14. 更新 frameworks/_index.md 和 templates/_index.md
  - 涉及：
    - `frameworks/_index.md`（占位扩展表移除 4 个已完成项 + 辅助 framework 表新增 4 行）
    - `templates/_index.md`（新增 2 个 template 入口）
  - 验收：
    - [ ] 占位扩展表只保留 0.3.0+ 未做项
    - [ ] 辅助 framework 表按命题分类标注新 framework 适用场景

- [x] 15. 写回归测试
  - 涉及：`docs/tests/finance-analysis-0.2.0.md`（新建）
  - 做什么：5+ 用例覆盖 4 个新 framework + 1 个跨 framework 组合
  - 验收：每个用例有前置条件 / 输入命题 / 预期加载 framework / 预期输出字段

- [x] 16. M5 commit
  - commit msg：`feat(finance-analysis): 0.2.0 - SKILL + 版本 + 索引 + 回归测试`

---

## 里程碑

| 里程碑 | 子任务 | 交付物 |
|-------|--------|--------|
| M1 | 1-3 | valuation-relative framework + valuation-card |
| M2 | 4-6 | valuation-dcf framework + valuation-card DCF 扩展 |
| M3 | 7-9 | stock-selection framework + stock-screening-card |
| M4 | 10-11 | us-ipo-arbitrage framework |
| M5 | 12-16 | SKILL + VERSION + CHANGELOG + _index + 回归测试 |

总计 16 子任务，5 个 commit。

## 执行纪律

1. **每个 milestone 结束立即 commit**，不积累
2. **每个 Worked Example 写入前 WebSearch 核对数据**（特别是历史价格、财报数字）
3. **9 要素逐项过清单**，缺一项不算完成
4. **M2 开始前做一次 context 评估**，压力大则新开一轮会话
5. **M5 收尾时全量跑回归用例，失败项回到对应 framework 修复**

## 不在本 plan 范围

- 0.3.0+ 的 fund-analysis / bond-analysis / event-driven / technical
- Tier 2 本地量化栈对接（已有 integrations/local-data-stack.md）
- SKILL.md 大改（本轮只增量调整，大改留到 1.0.0 稳定期）

## 风险与备选

- **风险 1**：framework 中间发现重大认知缺失，需要重写
  - 缓解：M1 完成时先让用户 review，定方向再滚 M2-M4
- **风险 2**：Worked Example 数据核对失败（找不到可靠源）
  - 缓解：备选案例清单（每个 framework 准备 2 个候选，主案例不行换备选）
- **风险 3**：context 过载导致后半段 framework 质量下降
  - 缓解：每个 milestone 独立，可以换会话继续；跨会话用 task-execute 追踪
