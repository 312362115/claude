# Changelog — deep-research

## 1.6.0 (2026-04-20)
- 新增：行业信源矩阵（精简版 A 架构）
  - 新建 `references/sources/` 目录体系：
    - `_schema.yaml`（YAML 格式规范 + 腐烂标记字段）
    - `blacklist.yaml`（全域共享黑名单，hard/soft 分级 + patterns 通用识别规则）
    - `_source_heuristics.md`（一手源识别启发式，互联网/AI 走这条）
    - `_router.md`（命题 → 路径判断：白名单启用闸门 + 关键词匹配 + 预算倾斜）
    - `finance.yaml`（精选 15 条 LLM top-of-mind 没有的冷门权威）
    - `academic.yaml`（精选 10 条）
  - 架构决策：不做 internet-tech.yaml 和 ai-ml.yaml（穷举不可能 + 快速腐烂），改走启发式
- 改造：SKILL.md 集成信源矩阵
  - 1.2 末尾追加"加载信源矩阵"子节（3 闸门 + 预算分配）
  - 2.1 Lead Agent 职责新增"注入信源矩阵"：派发 sub-agent 时 prompt 附带 blacklist + 对应领域 YAML + heuristics
  - 2.4 回传 JSON 新增字段：`whitelist_hits` / `heuristic_hits` / `blacklist_avoided`

## 1.5.0 (2026-04-20)
- 新增：调查拓扑透明化（P0 第 5 条收尾）
  - 新增 2.5 调查拓扑记录协议：Lead Agent 维护 `/tmp/research-topology-<timestamp>.json`，记录 sub-agent 派发/预算/递归层级/放弃线索
  - 2.1 Lead Agent 职责追加"维护拓扑记录文件"
  - 5.2 报告结构末尾新增"调查拓扑"段模板（指标表 + sub-agent 分解 + 放弃线索）
  - 报告头"调研深度"改写为"派发 N 个 sub-agent，最深 L 层"
  - 6.1 质量自检新增检查 5（调查拓扑段完整性 + 数字对齐自动回填）
  - 原 2.5 搜索执行 → 2.6；2.6 页面抓取 → 2.7；2.7 信息记录 → 2.8；2.8 信息验证 → 2.9

## 1.4.0 (2026-04-20)
- 重构：第二步"多跳信息搜集"改造为 Orchestrator-Subagent 架构（对齐 Anthropic 官方 Research）
  - 新增 2.1 Multi-Agent 执行模型：Lead Agent 规划整合 + Sub-agent 并行深挖
  - 新增 2.2 迭代式深挖 + 节点级 Fork 触发规则（替代固定 3 层广度优先）
  - 新增 2.3 Scaling Rules：按命题复杂度强制预算（简单/对比/复杂/超深度）
  - 新增 2.4 Sub-agent 压缩回传协议：强制 JSON 格式 + Filesystem Pattern
  - 原 2.3/2.4/2.5 顺延为 2.6/2.7/2.8
- 新增：简单事实查询禁止开 Multi-Agent 红线（Token 成本约 15x chat）
- 改进：1.7 对齐输出从"搜索深度"改为"命题复杂度 + 执行预算 + Token 预估"

## 1.3.0 (2026-04-02)
- 修复：整体 review — 交叉引用、术语一致性、frontmatter 更新
- 新增：核心结论增加置信度标注（高/中/低）

## 1.2.0 (2026-03-28)
- 改进：假设形成前增加快速扫描步骤，消除"无调研先假设"问题
- 修复：质量自检补充手动检查项 + 修复硬编码计数
- 新增：Step 6 质量自检 — 自动检测报告结构/引用/假设/来源支撑

## 1.1.0 (2026-03-22)
- 修复：禁止手动截图 + 术语规范
- 重构：清理 Graphviz 依赖 — 图表生成统一对齐 Diagram skill
- 新增：报告支持可选 HTML 格式输出 — 图表内嵌、富样式、自包含

## 1.0.0 (2026-03-15)
- 初始版本：方法论升级 — 假设驱动+内外数据结合+来源分级+多层输出
- 报告模板+分析框架拆分为独立文件，运行时按需加载
