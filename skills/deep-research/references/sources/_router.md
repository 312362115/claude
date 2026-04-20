# 信源矩阵路由规则（_router.md）

> 本文档定义 deep-research skill 如何根据命题决定：**加载哪份信源 YAML / 是否走启发式 / 搜索预算如何分配**。
>
> 加载时机：deep-research skill 的第 1.3 节（在"判断调研类型"和"现状摸底"之间）。

---

## 决策流程

```flow
命题输入
↓
闸门 1：是"具体查询"还是"命题调研"？
↓
→ 具体查询（API 用法/命令参数/bug 复现）→ Lead 自查官方 docs → 跳过 YAML 加载
↓ 命题调研
闸门 2：关键词匹配行业标签
↓
→ 金融类 → 加载 finance.yaml
→ 学术类 → 加载 academic.yaml
→ 技术/AI/新兴产业 → 加载 _source_heuristics.md
↓
闸门 3：无论走哪条路径，都加载 blacklist.yaml
↓
进入第二步 Multi-Agent 调研
```

---

## 闸门 1：具体查询 vs 命题调研

### 具体查询特征（跳过 YAML）

- 关键词：**"怎么用 / 怎么写 / 参数是什么 / 为什么报错 / API 用法"**
- 目标是**单一正确答案**（有就是有，没有就是没有）
- 典型：
  - "React useEffect 的依赖数组怎么写"
  - "Redis ZADD 的 NX/XX 参数"
  - "git rebase --onto 语法"
  - "为什么 `useState` 的 setter 是异步的"

**处理**：
- Lead Agent 自查（不开 Multi-Agent，见 SKILL.md 2.3 Scaling Rules "简单事实"）
- 直接访问官方 docs（按 `_source_heuristics.md` P1 层级识别）
- 不加载任何行业 YAML

### 命题调研特征（加载 YAML）

- 关键词：**"调研 / 分析 / 对比 / 选型 / 格局 / 趋势 / 评估 / 现状 / 差距"**
- 目标是**有判断的结论**（需要交叉验证 + 反面证据）
- 典型：
  - "AI 编码工具市场格局"
  - "A 股食品饮料 Q3 业绩分化原因"
  - "向量数据库选型"
  - "Rust 异步生态现状"

**处理**：进入闸门 2。

### 模糊边界

| 命题 | 判定 | 理由 |
|------|------|------|
| "Claude API 的 prompt caching 怎么用" | 具体查询 | 有官方 docs 唯一正确答案 |
| "Claude API 和 Gemini API 哪个适合 RAG" | 命题调研 | 需要对比+判断 |
| "gitleaks 怎么配" | 具体查询 | docs 直答 |
| "秘密扫描工具选型" | 命题调研 | 需要对比 |

**不确定时**：按"命题调研"处理（加载 YAML 不会错，跳过反而可能漏重要源）。

---

## 闸门 2：关键词匹配行业标签

### 金融类（加载 finance.yaml）

**触发关键词**（任一匹配即触发）：

| 子域 | 关键词 |
|------|--------|
| A 股 | A 股 / 上交所 / 深交所 / 北交所 / 科创板 / 创业板 / 巨潮 / 证监会 |
| 美股 | 美股 / NYSE / NASDAQ / SEC / 10-K / 10-Q / 财报 / EDGAR |
| 港股 | 港股 / 港交所 / HKEX / 披露易 / HKMA / 金管局 / 南下资金 / CCASS |
| 加密 | 加密 / Crypto / DeFi / 链上 / 代币 / 比特币 / 以太坊 / Web3 |
| 债券/宏观 | 债券 / 国债 / 利率 / 汇率 / 央行 / GDP / CPI / PPI / PMI / 宏观 / 货币政策 |
| 通用 | 股票 / 财报 / 估值 / K线 / 上市公司 / 监管 / 基金 / 私募 / 量化 |

### 学术类（加载 academic.yaml）

**触发关键词**：论文 / 研究 / 综述 / 学术 / 预印本 / 文献 / 引用 / arXiv / PubMed / 期刊 / 会议论文

### 技术/AI/新兴产业（加载 _source_heuristics.md）

**触发特征**（默认 fallback）：
- 命题涉及具体产品/框架/公司名（Next.js / Rust / Claude / Cursor / K8s ...）
- 命题涉及技术概念（AI Agent / RAG / 向量数据库 / 云原生 / 微服务 ...）
- 命题涉及新兴产业（Vision Pro / Web3 游戏 / 自动驾驶 ...）

**处理**：加载 `_source_heuristics.md`，**不加载行业 YAML**。

### 多标签叠加

命题可能触发多个标签，按优先级处理：
- "AI + 金融" 命题（如 "AI 量化基金现状"）：同时加载 finance.yaml + _source_heuristics.md
- "Crypto + 监管" 命题（如 "加密监管对交易所影响"）：加载 finance.yaml（含 crypto 子块 + 监管源）
- **blacklist.yaml 永远加载**

---

## 闸门 3：blacklist.yaml 全域加载

**无条件加载**，优先级高于任何白名单。

sub-agent 派发时必须在 prompt 明确：
- `hard` severity 条目：硬过滤，不得引用
- `soft` severity 条目：可作情绪/舆情参考，不得作为权威数据源
- `patterns`：按模式自行识别并标注

---

## 搜索预算分配

**有白名单加载时（finance/academic）**：

| 比例 | 来源 | 说明 |
|-----|------|------|
| **70%** | 白名单冷门权威 | 这些是 LLM top-of-mind 里没有的，重点倾斜才能用到 |
| **20%** | 开放搜索 | 补充 YAML 未覆盖的维度（如最新事件、新崛起的源） |
| **10%** | 启发式识别 | 按 `_source_heuristics.md` 发现新一手源（回写 YAML 候选） |

**纯启发式时（互联网/AI）**：

| 比例 | 来源 |
|-----|------|
| **60%** | 按 heuristics 推导的 P1 一手源（产品官网/GitHub releases/RFC）|
| **30%** | P2 原厂博客 + 评测榜单 + 顶会 |
| **10%** | P3 审核社区（HN / Reddit 严格版 / InfoQ） |

**超支约束**：所有 sub-agent 沿用 SKILL.md 2.3 Scaling Rules 的工具调用上限。

---

## 加载产物注入到 sub-agent prompt

Lead Agent 派发 sub-agent 时，在 prompt 中按以下顺序注入：

```markdown
## 你的任务
<子问题描述>

## 信源矩阵（必读）

### 黑名单（hard 必避，soft 降级）
<blacklist.yaml 的 sources hard/soft 列表精简版>

### 黑名单模式（按特征识别）
<blacklist.yaml 的 patterns 精简版>

### 白名单冷门权威（若加载）
<finance.yaml 或 academic.yaml 的 sources 精简版，仅 name/domain/tier/notes>

### 一手源识别启发式（若加载）
<_source_heuristics.md 的核心规则 + 本命题所属子域的推导示例>

## 回传 JSON 字段要求
除 SKILL.md 2.4 标准字段外，追加：
- whitelist_hits: 白名单源命中数量（若加载）
- heuristic_hits: 按 P1/P2/P3 分类的命中源数
- blacklist_avoided: 识别并避开的黑名单域列表
```

---

## 路由决策日志

为了调试和质量自检，每次调研在 `/tmp/research-topology-<ts>.json` 中新增 `routing` 字段：

```json
{
  "routing": {
    "gate1_result": "命题调研",
    "gate2_tags": ["finance.a-shares", "finance.crypto"],
    "yaml_loaded": ["finance.yaml", "blacklist.yaml"],
    "heuristics_loaded": false,
    "budget_allocation": { "whitelist": 0.7, "open_search": 0.2, "heuristic": 0.1 }
  }
}
```

报告的"调查拓扑"段可选择性展示路由决策，帮助用户评估 YAML 效果。

---

## 降级与兜底

1. **YAML 不存在或解析失败**：回退到 `_source_heuristics.md`，在报告 surprises 中标注
2. **白名单源全部不可达**（反爬/停服）：扩展到开放搜索，在 gaps 记录
3. **命题无法分类**：默认走 `_source_heuristics.md`，不强行匹配 finance/academic
