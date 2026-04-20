---
priority: P1
status: open
spec:
plan:
---

# Deep Research Multi-Agent 架构升级 + 行业信源矩阵

## 背景

当前 deep-research skill 产出结论偏浅，经会话讨论定位出根本原因：

1. **架构层面**：采用"固定 3 层广度优先 + 层内并行"拓扑，所有 sub-agent 原始抓取内容都回流到主 agent 整合，主 agent 的 context 被撑爆后必然压缩丢失细节；没有"碰到有趣子问题就 fork 独立 sub-agent 递归深挖"的能力。
2. **数据源层面**：仅依赖公开互联网搜索 + WebFetch 几十个网页下结论，且 agent 会无意识地偏向 SEO 优化的内容农场，放弃权威但排名低的一手源（如学术 PDF、财报、官方文档）。
3. **行业适配缺失**：不同行业权威数据源差异极大（半导体 vs 金融 vs 医疗），当前 skill 没有按行业加载对应白名单的能力。

对标 Anthropic 官方 Research 系统（[官方博客](https://www.anthropic.com/engineering/multi-agent-research-system)），其 Orchestrator-Subagent 架构在内部 eval 上比单 agent 提升 **+90.2%**，且遇到的"agent 偏好 SEO 内容农场"问题与本 skill 完全一致——说明改造方向有业界背书。

## 目标

把 deep-research 从"系统化网页搜集"升级为"专业级 multi-agent 研究引擎"，对齐业界 SOTA 实践。

## 阶段性改造任务

### P0 — Multi-Agent 架构升级（核心）

1. **Orchestrator-Subagent 拓扑改造**
   - Lead Agent：负责 planning + 拆子问题 + synthesis + 判断是否继续深挖
   - Sub-agent：每个拿独立 context window，独立预算，专注一个子问题
   - 废弃"固定 3 层广度优先"模型，改为"按子问题兴趣度动态派发"
   - Lead 在 spawn 前把研究计划写入 Memory（防 context 截断）

2. **Sub-agent 压缩回传协议（强制）**
   - Sub-agent 不得把原始网页内容回传给 Lead
   - 必须返回结构化 JSON：`{ findings, evidence_urls, source_tier, confidence, surprises, gaps }`
   - Evidence 字段只保留关键引文片段（≤100 字）
   - 配合 Filesystem Pattern：大输出存文件，主 agent 按需 Read

3. **Scaling Rules（按复杂度定预算）**
   - 简单事实查询：1 个 sub-agent，3-10 次工具调用
   - 对比类命题：2-4 个 sub-agent，每个 10-15 次
   - 复杂深度研究：10+ 个 sub-agent，按需迭代
   - 每个 sub-agent 必须带 WebSearch / WebFetch 次数上限，超支强制收尾

4. **节点级递归深挖触发规则**
   - 满足以下任一条件，Lead 必须 fork 新 sub-sub-agent：
     - finding.confidence = low 且关系到核心结论
     - 发现 surprises（反直觉线索）
     - evidence 之间矛盾
     - 反面 findings 数量 < 2
     - 关键命题仅有 T2/T3 支撑、未找到 T1

5. **调查拓扑透明化**
   - 报告末尾增加"调查拓扑"段：派发 sub-agent 数、最深递归层级、总搜索次数、放弃的线索
   - 让深度可观测

### P1 — 行业信源矩阵（长期资产）

6. **建立 `references/sources/` 配置目录**
   - 每个行业一个 YAML，字段：`tier_1_sources` / `tier_2_sources` / `academic` / `china_specific` / `blacklist`
   - 新增 `_router.md` 定义命题 → 行业标签的匹配规则
   - 新增 `_schema.yaml` 规范配置文件格式

7. **P1-A 首批 3 个高频行业（1-2 周）**
   - `internet-tech.yaml`（GitHub / HN / arXiv / 信通院 / Stack Overflow）
   - `finance-capital-markets.yaml`（SEC EDGAR / 巨潮 / 港交所披露易 / 财报 PDF）
   - `academic.yaml`（arXiv / Semantic Scholar / PubMed / CNKI）

8. **P1-B 第二批行业（按使用频次补）**
   - 半导体、医疗/生物、消费品、汽车、政策法规、能源
   - 策略：每次调研发现新权威源就回填配置

9. **运行时加载逻辑**
   - 在 `1.2 判断调研类型` 后加一步：命题 → 行业标签识别 → 加载对应 YAML → 生成"必爬清单"
   - 搜索预算倾斜：白名单源 80%，公开搜索兜底 20%
   - 报告附录展示"白名单覆盖率 X/Y"

10. **CitationAgent 独立化**
    - 从 Lead Agent 中剥离，作为独立 agent 在报告完成后运行
    - 专门负责：每条论断追溯到具体源、位置校对、生成引用列表

### P2 — 评测与持续演进

11. **建立 20 query 回归集**
    - 收集 20 个真实调研命题（覆盖不同类型/行业）
    - 每次 skill 改动后跑全量回归，对比前后报告质量

12. **LLM-as-judge 评测脚本**
    - Rubric：factual accuracy / citation accuracy / completeness / source quality / tool efficiency
    - 输出 0.0-1.0 综合分，跟踪改动效果

13. **人工 edge case 测试**
    - 每次大改后跑 3-5 个人工测试，捕捉 LLM judge 发现不了的问题（如 SEO 内容农场偏好）

## 参考

- [Anthropic: How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — 架构原型和踩坑教训来源
- 本次会话记录：deep-research 架构讨论（2026-04-20）
- 前期相关 backlog：`2026-03-29-deep-research-upgrade.md`、`2026-03-31-deep-research-quality.md`

## 验收标准

- **架构**：SKILL.md 明确描述 Orchestrator-Subagent 拓扑，Sub-agent 回传协议有结构化定义
- **信源**：至少 3 个行业 YAML 落地（internet-tech / finance / academic），skill 能按命题自动加载
- **深度**：同一命题对比改造前后，报告中引用的 T1 源数量提升 ≥2x
- **透明**：报告包含调查拓扑 + 白名单覆盖率
- **可度量**：20 query 回归集跑分前后对比有数据留存

## 备注

- 本条需求规模大、跨多个改造点，建议出 spec 时拆成多个 plan（P0 一个 plan、P1 信源一个 plan、P2 评测一个 plan）
- Token 成本提醒：multi-agent 架构大约消耗 15x chat tokens，需在 skill 里加预算提示

## 进度

- **2026-04-20**：完成 P0 第 1-4 条（Orchestrator-Subagent 拓扑 + 压缩回传协议 + Scaling Rules + 节点级触发规则），skill 升级到 1.4.0
  - P0 第 5 条"调查拓扑透明化"（报告末尾附拓扑数据）尚未实施，待后续 P1 改造时一并处理
