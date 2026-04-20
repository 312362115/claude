# 一手源识别启发式

> 对于没有白名单的领域（互联网技术 / AI / 新兴产业 / 各种快速变化的赛道），本文档指导 sub-agent 如何**动态识别一手权威源**，不依赖穷举列表。

**加载时机**：router 判定命题属于"无白名单领域"时，sub-agent prompt 中注入本文件内容。

---

## 核心原则

**官方 > 原厂 > 审核社区 > 聚合媒体 > 转引站**

识别时问自己：
1. 这个内容是"**谁的第一手表述**"？
2. 如果出错，"**谁负责**"？（有维护者/法人责任的优于匿名）
3. 内容是"**原创产出**"还是"**转引整合**"？

---

## 一手源优先级排序（高到低）

| 优先级 | 类型 | 示例 |
|--------|------|------|
| **P1** | 产品/项目官网 docs | `<product>.org/docs`, `<product>.io/docs`, `docs.<product>.com` |
| **P1** | 产品/项目官方博客 | `blog.<company>.com`, `<product>.org/blog`, `<company>.com/engineering` |
| **P1** | 官方 GitHub releases | `github.com/<org>/<repo>/releases`, `github.com/<org>/<repo>/discussions` |
| **P1** | 官方规范/RFC/EIP/BIP | `w3.org/TR/...`, `tc39.es/proposal-...`, `eips.ethereum.org/...` |
| **P2** | 原厂技术博客（大厂） | Google/Meta/Anthropic/OpenAI/Mozilla/Cloudflare 的 engineering blog |
| **P2** | 顶会论文官网（非聚合） | NeurIPS/ICLR/SIGCOMM 各自官网；不是 Google Scholar |
| **P2** | 官方 Twitter/X 账号（认证蓝标） | 项目维护者 + 公司官方账号 |
| **P3** | 有严格审核的社区 | Hacker News, r/<严格版> (r/rust/r/LocalLLaMA), InfoQ, LWN |
| **P3** | OSS 维护者的个人博客 | Dan Abramov, Simon Willison, Gergely Orosz 等核心社区人 |
| **P4** | 聚合媒体（原创为主） | TheVerge, ArsTechnica, TechCrunch 深度报道 |
| **❌** | blacklist.yaml 列入的域 | 强制避开 |

---

## 必避规则

1. **任何 blacklist.yaml 列入的域名**（硬过滤）
2. `*.csdn.net` / 掘金搬运类 / 百家号纯转载
3. 标题含"震撼 / 揭秘 / 必涨 / 一定要看 / 神预言"的 SEO 站
4. 生成式 AI 洗稿站（无实名作者 + 无引用溯源 + 段落跳跃）
5. 同一事件在短命域名（`*-news.com`/`*-daily.com`）集中出现

---

## 领域推导示例

### AI/LLM 赛道

**命题：Claude 3.7 Sonnet 编码能力对比**
```
P1 一手：
- anthropic.com/news
- anthropic.com/engineering
- anthropic.com/claude/sonnet（产品页）

P2 评测：
- lmarena.ai（Chatbot Arena 盲测排行）
- artificialanalysis.ai（延迟/价格/质量综合）
- livebench.ai（抗污染动态测试）
- swebench.com（软件工程任务）
- aider.chat/docs/leaderboards（编程场景）

P3 社区：
- huggingface.co/papers（论文日更）
- news.ycombinator.com（讨论深度高）
```

**命题：开源 Agent 框架选型**
```
P1 一手：
- langchain-ai.github.io（LangChain 官方）
- github.com/langchain-ai/langgraph/releases
- microsoft.github.io/autogen
- docs.crewai.com
- github.com/openai/swarm（已迁移至 Agents SDK）
- github.com/huggingface/smolagents

P2 大厂观点：
- Anthropic engineering（"Building Effective Agents" 系列）
- OpenAI Cookbook

P3 社区：
- HN + r/LocalLLaMA
```

**命题：AI 编码工具市场格局**
```
P1 产品方：
- cursor.com/blog
- codeium.com/blog（Windsurf）
- docs.claude.com/en/docs/claude-code
- github.blog/tag/copilot
- v0.dev, bolt.new, replit.com/agent

P2 行业报告：
- a16z.com/100-gen-ai-apps（a16z 百强榜）
- sequoiacap.com/article（Sequoia AI 系列）
- Stack Overflow Developer Survey（AI 使用章节）
- JetBrains Developer Ecosystem Report

P3 社区：
- HN + r/ChatGPTCoding + InfoQ
```

### 互联网技术

**命题：Next.js 15 新特性**
```
P1 一手：
- nextjs.org/blog
- nextjs.org/docs
- github.com/vercel/next.js/releases

P2 原厂：
- vercel.com/blog
- @nextjs 官方 X

P3 社区：
- dev.to/t/nextjs（部分原创）
- HN
```

**命题：Rust 异步生态现状**
```
P1 一手：
- rust-lang.org/blog
- blog.rust-lang.org/inside-rust
- github.com/rust-lang/rust/releases
- foundation.rust-lang.org

P1 核心项目官方：
- tokio.rs/blog
- async.rs（async-std，注意：已进入维护模式）
- docs.rs/<crate>

P3 社区：
- this-week-in-rust.org
- users.rust-lang.org
- r/rust
```

**命题：K8s vs Nomad 2026 现状**
```
P1 一手：
- kubernetes.io/blog
- hashicorp.com/blog（Nomad）
- github.com/kubernetes/kubernetes/releases
- github.com/hashicorp/nomad/releases

P2 生态：
- cncf.io/reports（CNCF 调查报告）
- kccncna.com（KubeCon 官方会议）
- landscape.cncf.io

P3 第三方观察：
- TheNewStack（云原生深度报道）
- 各大云厂商技术博客（AWS/GCP/Azure）
```

### 其他领域

**命题：Vision Pro 开发者生态**
```
P1：developer.apple.com, WWDC session 回放
P3：r/visionpro, iOS 技术博客
```

**命题：Stripe vs Adyen 支付能力对比**
```
P1：stripe.com/docs, adyen.com/developers
P2：两家 engineering blog
P3：HN 支付相关讨论
```

---

## 降级策略（找不到足够一手源时）

如果 P1/P2 源不足以回答命题，按以下顺序降级：

1. **扩展 P3 社区源**（HN / Reddit 严格版 / InfoQ）
2. **允许引用 P4 聚合媒体**（TheVerge/ArsTechnica/TechCrunch 深度报道）
3. **在 findings 中标注来源层级**（T1/T2/T3），让读者知晓
4. **在 gaps 中列出"未找到一手源"的维度**

⚠️ **永远不降级到 blacklist**。

---

## sub-agent 执行纪律

当 prompt 加载本文件时，sub-agent 必须：

1. 调用 WebSearch 前，**先根据命题关键词推导 P1 源的 URL 候选**
2. 优先访问推导出的 P1 候选，再开放搜索补充
3. 在 findings 的 `tier_suggestion` 字段明确标注 T1/T2/T3
4. 遇到黑名单域**立即放弃**，不要"顺手看看"
5. 回传 JSON 增加 `heuristic_hits` 字段，列出成功命中的 P1/P2 源数量

```json
{
  "findings": [...],
  "heuristic_hits": {
    "p1_official": 3,
    "p2_authoritative": 2,
    "p3_community": 1,
    "blacklist_avoided": ["csdn.net", "xxxnews.com"]
  }
}
```
