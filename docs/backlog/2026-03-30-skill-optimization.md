---
priority: P2
status: open
---

# Diagram + Deep-Research Skill 优化

基于 2026-03-30 综合评估（Diagram 8.75/10, Deep-Research 7.9/10），记录待优化事项。

---

## Diagram（8.75 → 9+）

- [x] **P1** 补充漏斗图、瀑布图等常用商业图表（2026-03-30 完成）
- [x] **P2** 模板去重 — 31 个模板抽取公共渲染逻辑为 shared module（2026-03-30 完成）
- [ ] **P3** 布局引擎统一评估 — Dagre 和 ELK 并存是否必要

## Deep-Research（7.9 → 9）

- [ ] **P0** 建立报告质量自动检测（结构完整性、引用格式、假设验证表、T1/T2 来源比例）
- [ ] **P1** 统一图表生成体系 — 用 Diagram skill 替代独立的 matplotlib/graphviz，消除两套设计系统 + 114MB Python 依赖
- [ ] **P2** 增加"评估/诊断"独立报告模板
- [ ] **P3** 搜索结果缓存机制，减少重复调研的网络依赖
