# Deep Research 信源矩阵架构决策复盘

> 日期：2026-04-20
> 关联：`docs/specs/2026-04-20-deep-research-sources-industry-audit.md` / `docs/plans/2026-04-20-deep-research-sources-plan.md` / PR #16
> 决策人：用户 + Claude（本次会话）

---

## 背景

P1 backlog 原计划"为每个行业建一份完整 YAML（互联网 / 金融 5 子块 / 学术）"。本次会话启动后做了两轮 sub-agent 调研（8 个 agent / 131 findings），调研过程中识别出原方案的根本性缺陷，最终落地精简版 A 架构。

## 原方案问题

执行原方案的过程中，陆续暴露 3 个根本问题：

1. **穷举不可能**：互联网技术有无穷子域（Next.js / Rust / K8s / 向量数据库 / AI Agent …），每周出新框架。YAML 永远追不上。
2. **快速腐烂**：本次调研直接抓到 3 例——IEX Cloud 2024-08 停服 / Polygon.io 被 Massive 收购 / Papers with Code 并入 HuggingFace。即使精心维护，3 个月一次 refresh 也跟不上变化节奏。
3. **AI 赛道悖论**：AI/LLM 是当下 80% 心智份额的赛道，但靠硬编码清单覆盖不到位——大厂官博稳定（OK）但 Agent 框架/编码工具/评测榜单一季度一变（不 OK）。

用户的关键质疑：**"配置死数据源，是不是一个好的想法"**—— 这个问题直接推翻了原架构假设。

## 决策过程

### 方案对比

| 方案 | 核心做法 | 问题 |
|------|---------|------|
| **原版 A** | 每行业完整 YAML（15-20 条/份），包含 LLM 都知道的主流源 | 穷举爆炸 + 腐烂快 + AI 赛道覆盖不到 |
| **方案 B** | 拆 2-3 个子域 YAML（AI/云/通用） | 子域粒度仍追不上新框架 |
| **方案 C** | 不做 YAML，完全靠 `_source_heuristics.md` 动态识别 | 放弃了本次调研发现的冷门权威（BIS / 中债登 / OpenAlex） |
| **精简版 A**（最终） | 只收"LLM top-of-mind 没有的冷门权威"+ blacklist + heuristics | ✅ |

### 关键洞察

在用户与 Claude 的来回讨论中，逐步提炼出两条**可复用原则**：

1. **LLM top-of-mind 测试**：判断一个源要不要进 YAML，问"不看 YAML，sub-agent 能想到吗"—— 能想到的不进，LLM 自己就知道 SEC EDGAR / FRED / arXiv，硬编码进去是浪费维护量。
2. **blacklist 是 YAML 体系最大价值**：LLM 自己识别 SEO 内容农场 / AI 洗稿站 / 转引聚合站的准确率低，显式黑名单比改 prompt 更可靠。CSDN / 东财股吧 / 雪球 / 金色财经这类 10 年不会变的负向标记，正好弥补 LLM 的盲区。

### 最终架构（3 层）

```
Layer 1: blacklist.yaml（全域共享，最高优先级）    ← 最大价值
Layer 2: finance.yaml / academic.yaml（冷门权威 10-15 条）
Layer 3: _source_heuristics.md（互联网/AI 走这条，不穷举）
```

## 放弃了什么

- **不再做 `internet-tech.yaml`**（技术赛道变化太快，穷举不可能）
- **不再做 `ai-ml.yaml`**（虽然是热门，但维护跟不上）
- 接受在某些情况下 sub-agent 会重复摸索那些"LLM 知道但我们没沉淀"的源（判断这是可接受的代价）

## 实施产物

- 6 份 sources/ 配置：`_schema.yaml` / `blacklist.yaml` / `_source_heuristics.md` / `_router.md` / `finance.yaml` / `academic.yaml`
- SKILL.md 升到 1.6.0：1.2 加载闸门 + 2.1 Lead 注入 + 2.4 回传字段
- 5 个回归用例 / `docs/tests/deep-research-sources.md`
- PR #16 已 merge 到 main

## 踩坑记录

### 坑 1：互联网技术 round 1 调研方向偏了

第一轮 7 个 sub-agent 的 prompt 都强调"最权威/一手/监管认可"，导致互联网技术 sub-agent 自动过滤掉了 **开发者向的免费 API**（yfinance / AKShare / Finnhub / CCXT 等）。用户一语点破"想获取股票 K 线这些从哪拿"——发现漏了**量化开发者视角**。

**教训**：prompt 的"权威性"偏见会系统性地漏掉"开发者向"源。以后设计调研 prompt 时要显式涵盖多视角（权威视角 / 开发者视角 / 消费者视角）。

补救：round 2 专派一个 sub-agent（sub-08）补量化 API 维度。

### 坑 2：互联网技术是多子域合集，不是"一个行业"

用户第二个点醒："AI 这个当前互联网技术领域，基本上一个都没体现"。诊断到位——互联网技术不是一个行业，是多个细分赛道合集（AI/云原生/前端/数据库/移动……）。任何"互联网技术 YAML"都是劣质抽象。

**教训**：做行业分类时要问"这个类别的权威源是有限集合吗？"——金融（监管+交易所+央行数量固定）答案是"是"，可以做 YAML；技术（每周新框架）答案是"否"，只能做 heuristics。

### 坑 3：死配置的价值要按领域判断

本次会话早期我（Claude）默认死配置都是好想法。用户反问后重新评估，意识到：

| 领域 | 死配置价值 | 原因 |
|------|----------|------|
| blacklist | **最高** | 识别规则 LLM 不准 + 变化慢 |
| 金融/学术权威源 | 中 | 权威源集中且稳定 |
| 互联网/AI | 低 | 变化快 + 穷举爆炸 |

**教训**：遇到"是否要固化成配置"的选择时，先评估该领域的**权威源稳定性**和**穷举可行性**，不能一刀切。

## 可复用经验

1. **"LLM top-of-mind 测试"**是判断"要不要沉淀为配置"的通用标准——适用于任何 skill 的配置文件设计
2. **blacklist 比 whitelist 价值更高**——LLM 对正向源识别不差，但对负向源（SEO 站/洗稿站）识别弱
3. **Prompt 里的评价维度会系统性过滤结果**——做 "最权威" 类调研时，要显式标注"多视角覆盖"
4. **调研过程中用户的反问 > Claude 的自验证**——用户 2 次关键反问（"死数据是否好"/"AI 为什么没有"）推翻了早期假设，Claude 自己 verify 时不会意识到

## 后续监控

- **3 个月后 refresh 节点**（2026-07-20 左右）：检查 IEX/Polygon/PMC 等 rot_indicator 条目是否需更新
- **实战验证**（子任务 10）：下次真实调研任务触发，观察 YAML/heuristics 是否生效
- 验证合格后：本次 P1 需求标 done 并二次复盘
