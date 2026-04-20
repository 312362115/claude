# Deep Research 信源矩阵落地计划（精简版 A）

## 关联
- 方案：`docs/specs/2026-04-20-deep-research-sources-industry-audit.md`
- backlog：`docs/backlog/2026-04-20-deep-research-multi-agent.md`（P1）

## 核心原则

**只收"LLM top-of-mind 里没有的冷门权威"**。判断标准：不看 YAML，sub-agent 能想到吗？能想到的不进。

架构：3 层
- **Layer 1**：`blacklist.yaml`（全域共享，最高价值）
- **Layer 2**：`finance.yaml` + `academic.yaml`（只收冷门权威，各 10-15 条）
- **Layer 3**：`_source_heuristics.md`（互联网/AI/新兴产业走这条，不穷举）

## 子任务

- [ ] 1. 建目录 + 格式规范
  - 做什么：创建 `references/sources/` 目录，写 `_schema.yaml` 定义 YAML 字段格式
  - 涉及：`references/sources/_schema.yaml`（新建）
  - 验收：schema 覆盖 name / domain / url / scores / access_method / tier_suggestion / notes / rot_indicator 字段，给出示例

- [ ] 2. `blacklist.yaml`（最高优先级）
  - 做什么：沉淀本次调研发现的黑名单 + 通用 SEO 模式
  - 涉及：`references/sources/blacklist.yaml`（新建）
  - 验收：至少包含 CSDN / 东财股吧 / 雪球 / 金色财经 / 掘金（搬运部分）/ "必涨/神预言"类，每条带 reason + category；含至少 2 条 patterns 通用规则

- [ ] 3. `_source_heuristics.md`（一手源识别启发式）
  - 做什么：写给 sub-agent 的启发式规则——没有白名单领域（互联网/AI）如何识别一手源
  - 涉及：`references/sources/_source_heuristics.md`（新建）
  - 验收：包含一手源优先级排序、必避规则、AI/LLM 赛道推导示例（至少 3 个）、互联网技术推导示例（至少 3 个）

- [ ] 4. `_router.md`（路由规则）
  - 做什么：定义命题 → 路径判断逻辑
  - 涉及：`references/sources/_router.md`（新建）
  - 验收：含白名单启用闸门（具体查询 vs 命题调研）、关键词匹配规则、预算倾斜比例（70/20/10）

- [ ] 5. `finance.yaml`（精简版，10-15 条）
  - 做什么：收录 LLM 不知道的冷门权威金融源
  - 涉及：`references/sources/finance.yaml`（新建）
  - 验收：条目数 10-15 个，每条通过"LLM top-of-mind 测试"；包含 BIS / 中债登 / CFETS / Fiscal Data / SAFE / 上清所 / HKEX SDI / CCASS / Tardis.dev / BaoStock / Finnhub 等

- [ ] 6. `academic.yaml`（精简版，10-15 条）
  - 做什么：收录 LLM 不知道的冷门权威学术源
  - 涉及：`references/sources/academic.yaml`（新建）
  - 验收：条目数 10-15 个；包含 OpenAlex / bioRxiv / ChemRxiv / OpenReview / CrossRef / ACM DL 全 OA / SSRN / OSF Preprints 等

- [ ] 7. 改造 deep-research skill 加载逻辑
  - 做什么：在 SKILL.md 1.2（判断调研类型）之后加一步"加载路由"，在 2.1（Lead Agent 职责）里加一步"向 sub-agent 派发时附带白名单"
  - 涉及：`skills/deep-research/SKILL.md`（改）
  - 验收：
    - 新增 1.3 "加载信源矩阵"小节（命题 → router → 加载 YAML/heuristics）
    - 2.1 Lead Agent 职责加 "向 sub-agent 派发时在 prompt 附上 blacklist + 对应领域 YAML + heuristics"
    - 2.4 回传协议加字段 `whitelist_hits`（使用了几个白名单源）
    - CHANGELOG 升 1.6.0

- [ ] 8. 改造 sub-agent prompt 模板
  - 做什么：Lead Agent 派发 sub-agent 时，prompt 自动注入 YAML + heuristics + blacklist 内容
  - 涉及：`skills/deep-research/SKILL.md` 的 2.1/2.4 章节
  - 验收：prompt 模板明确标注 "必爬清单（白名单）"、"必避清单（黑名单）"、"领域启发式规则"三段

- [ ] 9. 写回归测试
  - 做什么：至少 5 个命题的测试用例，覆盖不同路径
  - 涉及：`docs/tests/deep-research-sources.md`（新建）
  - 验收：
    - 用例 1：命题"调研 Next.js 15 新特性" → 走 heuristics（不加载 YAML）
    - 用例 2：命题"A 股食品饮料板块 Q3 业绩" → 加载 finance.yaml
    - 用例 3：命题"React useEffect 怎么用" → 具体查询，跳过白名单
    - 用例 4：命题"大模型评测对比" → heuristics（AI 推导示例）
    - 用例 5：命题"生物医学 LLM 应用综述" → 加载 academic.yaml
    - 每个用例列出预期白名单加载、预期避开的 blacklist 域

- [ ] 10. 实战验证 + 复盘
  - 做什么：跑一个真实调研任务验证路由/加载/白名单生效，对比改造前后
  - 涉及：在一个实际调研会话中观察 sub-agent 是否用到了 YAML 源、是否避开了 blacklist
  - 验收：
    - 白名单源在 findings 中出现 ≥ 2 个冷门源（说明 YAML 起作用）
    - findings 中无 blacklist 域（说明过滤生效）
    - 整合到 `docs/decisions/2026-XX-XX-sources-v1-retro.md`

## 里程碑

- **M1**（1-2 天）：子任务 1-4 完成 → blacklist + heuristics + router 可用
- **M2**（2-3 天）：子任务 5-6 完成 → finance + academic YAML 落地
- **M3**（1 天）：子任务 7-8 完成 → skill 集成
- **M4**（1 天）：子任务 9-10 完成 → 测试 + 实战验证

总计约 1 周（碎片时间完成）。

## 不在本 plan 范围

- 互联网技术 YAML（放弃，靠 heuristics）
- AI/LLM YAML（放弃，靠 heuristics）
- 20 query 回归集 + LLM-as-judge 评测（P2，单独 plan）
- CitationAgent 独立化（P1 原第 10 条，单独 plan）

## 风险与备选

- **风险 1**：YAML 腐烂——Polygon 被收购、IEX 停服这类事件 3 个月一次
  - 缓解：YAML 条目带 `last_verified` 字段，router 加载时如距今 >90 天给出警告提示用户手工 refresh
- **风险 2**：heuristics 效果不如 YAML——sub-agent 在新领域"找不到"一手源
  - 缓解：子任务 10 实战验证时重点观察，必要时降级为 "需要 YAML 的领域 + 1"
- **风险 3**：路由错判——命题落到错误路径
  - 缓解：子任务 9 的 5 个测试用例强制覆盖边界
