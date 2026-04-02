---
priority: P2
status: open
---

# Deep-Research Skill 质量优化（7.9 → 9）

基于 2026-03-30 综合评估，从 Diagram 优化 backlog 中拆分出来。

---

- [x] **P0** 建立报告质量自动检测（结构完整性、引用格式、假设验证表、T1/T2 来源比例）
- [x] **P1** 统一图表生成体系 — 用 Diagram skill 替代独立的 matplotlib/graphviz（已完成，现调用画图 skill 生成 PNG）
- [ ] **P2** 增加"评估/诊断"独立报告模板
- ~~**P3** 搜索结果缓存机制~~ — dropped：AI 上下文本身记忆已搜内容，实际重复概率极低，投入产出不值
