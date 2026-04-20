# Deep Research 信源矩阵回归测试

> 验证 deep-research skill 1.6.0 新增的信源矩阵加载逻辑（_router.md / YAML / heuristics）。
> 每次 YAML 体系改动后全量回归。

## 前置条件

- deep-research skill 版本 ≥ 1.6.0
- `references/sources/` 目录含：`_schema.yaml` / `blacklist.yaml` / `_source_heuristics.md` / `_router.md` / `finance.yaml` / `academic.yaml`

## 执行方式

每个用例运行时，观察 sub-agent 派发 prompt 中是否正确注入了对应 YAML/heuristics 内容，并检查回传 JSON 的 `whitelist_hits` / `heuristic_hits` / `blacklist_avoided` 字段。

---

## 用例 1：技术/AI 命题（走 heuristics，不加载 YAML）

**命题**：调研 Next.js 15 新特性和性能改进

**预期路由**：
- 闸门 1：命题调研（非具体查询）
- 闸门 2：无金融/学术关键词 → 加载 `_source_heuristics.md`
- 闸门 3：加载 `blacklist.yaml`

**预期加载**：
```
heuristics: true
yaml_loaded: [blacklist.yaml]
```

**预期 findings 特征**：
- ≥ 2 个 P1 一手源：`nextjs.org/blog`、`github.com/vercel/next.js/releases`、`vercel.com/blog`
- ≥ 1 个 P3 社区：HN
- `heuristic_hits.p1_official` ≥ 2
- `blacklist_avoided` 可能含 `csdn.net`（若搜索时被识别）

**不应出现**：
- `whitelist_hits` 字段（因为没加载 YAML）
- findings 中引用 csdn.net / 掘金搬运类

---

## 用例 2：A 股命题（加载 finance.yaml）

**命题**：A 股食品饮料板块 Q3 业绩分化原因分析

**预期路由**：
- 闸门 1：命题调研
- 闸门 2：匹配「A 股 / 业绩」关键词 → 加载 `finance.yaml`
- 闸门 3：加载 `blacklist.yaml`

**预期加载**：
```
yaml_loaded: [finance.yaml, blacklist.yaml]
heuristics: false（或 fallback 加载）
```

**预期 findings 特征**：
- `whitelist_hits` ≥ 2（命中 finance.yaml 的冷门权威）
- 预期命中：申万宏源行业指数 / BaoStock / 中债登（若涉及利率分析）
- **不应**出现在 findings：东方财富股吧 / 雪球（blacklist hard）
- `blacklist_avoided` 含至少 1 个域

**合格标准**：
- 白名单命中率 ≥ 2 条
- 零 blacklist hard 条目出现在引用列表

---

## 用例 3：具体查询（跳过白名单，Lead 自查）

**命题**：React useEffect 的依赖数组怎么写

**预期路由**：
- 闸门 1：**具体查询**（关键词"怎么写"+ 单一正确答案场景）→ 跳过 YAML 加载
- 不走 Multi-Agent（Scaling Rules "简单事实"）

**预期行为**：
- Lead 直接 WebFetch `react.dev/reference/react/useEffect`
- 不 spawn sub-agent
- 不生成调查拓扑文件（或生成最小版本）

**合格标准**：
- 未加载任何 YAML（除了 blacklist 可能仍加载但无实际影响）
- 搜索次数 ≤ 3
- 报告简短，无完整"调查拓扑"段

---

## 用例 4：AI/LLM 赛道（走 heuristics，AI 子域推导）

**命题**：2026 年大模型评测榜单对比（LMArena / Artificial Analysis / LiveBench）

**预期路由**：
- 闸门 1：命题调研
- 闸门 2：无金融/学术关键词 + AI 关键词 → 加载 `_source_heuristics.md` + 本命题所属 AI 子域推导示例
- 闸门 3：加载 `blacklist.yaml`

**预期 findings 特征**：
- 命中 heuristics 推导的 AI 评测源：`lmarena.ai` / `artificialanalysis.ai` / `livebench.ai` / `swebench.com`
- `heuristic_hits.p2_authoritative` ≥ 3（评测榜单属 P2）
- 可能含 P3 HN + HF Papers

**不应出现**：
- 引用任何中文"某某大模型评测分析"SEO 站
- CSDN/金色财经 等 blacklist

---

## 用例 5：学术/生物医学命题（加载 academic.yaml）

**命题**：近两年 LLM 在生物医学文本挖掘领域的研究综述

**预期路由**：
- 闸门 1：命题调研
- 闸门 2：匹配「研究 / 综述」关键词 → 加载 `academic.yaml`
  - 跨领域（AI + 医学）可同时加载 `_source_heuristics.md`
- 闸门 3：加载 `blacklist.yaml`

**预期 findings 特征**：
- `whitelist_hits` ≥ 2：命中 OpenAlex / bioRxiv / PMC / OpenReview
- 冷门权威覆盖：至少 2 个 LLM 不会主动想到的源（如 OpenAlex、bioRxiv 新移交 openRxiv 后的实际状态）
- 同时命中 heuristics：arXiv（LLM 自己就知道，不在 academic.yaml 里）

**合格标准**：
- academic.yaml 白名单命中 ≥ 2
- arXiv + PubMed 作为对照组出现在 findings（证明白名单与 heuristics 互补）

---

## 汇总：合格阈值

整套 5 个用例跑完后，合格条件：

| 指标 | 阈值 |
|------|------|
| 用例 1 heuristic_hits.p1_official | ≥ 2 |
| 用例 2 whitelist_hits | ≥ 2 |
| 用例 2 blacklist_avoided | ≥ 1 |
| 用例 3 搜索次数 | ≤ 3 |
| 用例 4 heuristic_hits.p2_authoritative | ≥ 3 |
| 用例 5 whitelist_hits | ≥ 2 |
| 任何用例引用 hard blacklist 条目 | 0 次 |

---

## 回归记录

| 日期 | 版本 | 通过率 | 记录 |
|------|------|--------|------|
| TBD | 1.6.0 | - | 首次跑前 |

每次 YAML 改动后手工跑一遍，填入此表。
