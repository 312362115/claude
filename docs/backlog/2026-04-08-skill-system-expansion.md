---
priority: P1
status: open
spec: （待创建）
plan: （待创建）
---

# Skill 体系扩建

## 背景

当前 skill 体系覆盖了任务全生命周期（task-start → execute → finish）、调研、图表、前端、TDD、CR、调试等核心开发能力。经梳理发现以下缺口：

- **安全/质量门禁**：上线前无结构化安全审计流程
- **重构/性能**：大规模重构和性能分析缺乏结构化引导
- **写作/表达**：能产出代码但缺乏文档/汇报的专业写作能力
- **日常效率**：代码导读、依赖分析、环境排障、日志分析等高频场景无 skill 覆盖
- **项目管理**：需求管理、发版流程缺乏自动化
- **架构改造**：task-start 目前混合了流程调度和方案写作职责，需要解耦

## 架构设计

### 核心原则：流程 vs 能力分离

```
流程 skill（调度"做什么"）          能力 skill（负责"怎么做"）
─────────────────────────          ──────────────────────────
task-manager    需求管理             writing         写各种文档
task-start      启动调度             deep-research   调研（已有）
task-execute    执行管理（已有）      tech-evaluation 选型
task-finish     收尾复盘（已有）      diagram         画图（已有）
refactoring     重构流程             code-walkthrough 代码导读
                                    dependency-map   依赖分析
                                    security-audit   安全审计
                                    perf-profiling   性能分析
                                    release          发版
                                    rapid-prototype  快速原型
                                    log-analysis     日志分析
                                    env-troubleshoot 环境排障
                                    learning-companion 学习助手
                                    docs-management  文档管理
```

流程 skill 调度能力 skill，自己不负责具体产出。

### task-start 改造

把方案模板/计划模板抽到 writing skill，task-start 只保留流程调度 + 对焦逻辑：

```
task-start 改造后：
  收到需求 → 决策树判断深度
    ├─ 需要对焦 → 自己做（问答式，轻量）
    ├─ 需要 UI 原型 → 调 rapid-prototype
    ├─ 需要选型 → 调 tech-evaluation
    ├─ 需要调研 → 调 deep-research
    ├─ 需要写方案 → 调 writing（技术方案模式）
    └─ 需要写计划 → 调 writing（开发计划模式）
```

### writing skill 模式设计

```
writing
  ├─ 技术文档模式 ── API 文档、开发指南、技术方案(spec)、开发计划(plan)
  │   读者：开发者 | 风格：准确完整 | 格式：Markdown
  │
  ├─ 产品文档模式 ── PRD、用户故事、运营方案、帮助文档
  │   读者：产品/运营/用户 | 风格：面向场景 | 格式：Markdown
  │
  └─ 汇报模式 ── 项目汇报、里程碑总结、OKR 复盘、方案评审
      读者：上级/跨团队 | 风格：结论先行、数据驱动 | 格式：精排 HTML（可浏览器预览）
```

汇报模式复用 diagram skill 设计体系（配色/字体/间距），自动调 diagram 生成图表嵌入。

### docs-management skill — 项目知识库引擎

> 灵感来源：[Karpathy - LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
> 核心理念：docs/ 不是静态文件堆，而是 LLM 持续维护的活知识库。
> "维护知识库最累的不是阅读和思考，是记账——交叉引用、一致性维护。这正是 LLM 擅长的。"

**三层架构**（对应 Karpathy 的 Raw Sources → Wiki → Schema）：

```
Raw Sources（原始素材）     →  代码、git log、会议记录、外部文档
Wiki（知识库）             →  docs/ 目录下所有结构化文档
Schema（规则）             →  CLAUDE.md 中的文档规范
```

**四个核心操作**：

| 操作 | 做什么 | 触发时机 |
|------|--------|---------|
| **Ingest（摄入）** | 新信息进来时，不只是新建文件，而是找到已有文档合并更新 | task-finish 后、新决策产生时、外部信息输入时 |
| **Query（查询）** | 从 docs/ 检索项目上下文，有价值的回答反写回 wiki | "这个模块之前怎么设计的？""上次类似问题怎么解的？" |
| **Lint（健康检查）** | 检查矛盾、过期、孤立页面、缺失内容、引用断链 | 定期执行，或大批量改动后 |
| **Index（索引）** | 维护全局索引 + 时间线日志 | 文档变更时自动更新 |

**Lint 具体检查项**：
- `docs/specs/` 中的文件路径引用是否还存在？
- `docs/plans/` 的 checklist 和实际代码进度是否一致？
- `docs/backlog/INDEX.md` 和实际 backlog 文件是否对得上？
- 有没有 spec 写了但没有对应 plan？plan 完成了但 backlog 没标 done？
- `docs/decisions/` 里的经验和 CLAUDE.md 的规则是否矛盾？
- 有没有孤立文档（不被任何 INDEX 或其他文档引用）？

**Index 维护**：
- `docs/INDEX.md` — 全局索引，按目录分类，每个文档一行摘要
- `docs/LOG.md` — 时间线日志，追加式记录每次文档变更（格式：`## [YYYY-MM-DD] <操作类型> <文档路径> — 一句话说明`）

**与 writing skill 的关系**：writing 生产文档，docs-management 维护文档。
**与 task-finish 的集成**：task-finish 复盘完成后，触发 Ingest 操作更新相关文档。

### 调用关系全景

```
task-manager ─── "做不做、做哪个"
       ↓ 决定做
task-start ─── "启动调度"
       ├─→ deep-research → writing（调研结论写成文档）
       ├─→ tech-evaluation → writing（选型结论写成方案）
       ├─→ rapid-prototype（验证想法）
       ├─→ writing（技术方案模式 → spec）
       └─→ writing（开发计划模式 → plan）
               ↓
task-execute ─── "执行管理"
       ├─→ code-walkthrough（理解陌生代码）
       ├─→ dependency-map（评估影响面）
       ├─→ refactoring（大规模重构子流程）
       │       ├─→ dependency-map
       │       └─→ task-execute（进度管理）
               ↓
验证阶段
       ├─→ perf-profiling（性能验证）
       ├─→ security-audit（安全审计，上线前必做）
               ↓
task-finish ─── "收尾"
       ├─→ writing（汇报模式，如需要）
               ↓
release ─── "发版"

随时可用（不依赖流程）：
  writing / log-analysis / env-troubleshoot / learning-companion / docs-management
```

## Skill 清单（15 个）

### 新建 skill（14 个）

| # | skill 名 | 类型 | 定位 | 技术栈 |
|---|---------|------|------|--------|
| 1 | security-audit | 能力 | 上线前安全审计：OWASP Top 10 + 敏感信息 + 依赖漏洞 | JS/TS, Python; npm audit, pip-audit, trivy |
| 2 | refactoring | 流程 | 大规模重构：影响分析→安全网→分步重构→回归 | 通用 |
| 3 | perf-profiling | 能力 | 前后端性能分析：定位瓶颈、benchmark、前后对比 | Lighthouse, 按项目选工具 |
| 4 | release | 能力 | 发版自动化：CalVer 版本号 + changelog + GitHub Releases | gh CLI |
| 5 | writing | 能力 | 通用写作：技术文档/产品文档/汇报（精排HTML） | Markdown + HTML |
| 6 | tech-evaluation | 能力 | 技术选型：权重矩阵 + PoC 验证 + 决策报告 | 通用 |
| 7 | code-walkthrough | 能力 | 代码导读：架构→核心流程→关键设计决策 | 通用 |
| 8 | dependency-map | 能力 | 依赖分析：调用链追踪、影响面评估 | 通用 |
| 9 | task-manager | 流程 | 需求管理：backlog 梳理、优先级排序、过期清理 | 通用 |
| 10 | rapid-prototype | 能力 | 快速原型：5 分钟出可交互 demo | HTML/JS |
| 11 | log-analysis | 能力 | 日志分析：异常定位、错误统计、时间线提取 | 通用 |
| 12 | env-troubleshoot | 能力 | 环境排障：结构化排查开发环境问题 | Node/Python/Docker |
| 13 | learning-companion | 能力 | 学习助手：按已有水平定制学习路径 | 通用 |
| 14 | docs-management | 能力 | 项目知识库引擎：Ingest 摄入 + Query 查询 + Lint 健检 + Index 索引（参考 Karpathy LLM Wiki） | 通用 |

### 改造现有 skill（2 个）

| skill | 改造内容 |
|-------|---------|
| task-start | ① 方案/计划模板抽到 writing skill，只保留流程调度 + 对焦逻辑；② 对焦阶段自动检索 `docs/decisions/` 相关经验，有则提醒"上次类似任务踩过这些坑" |
| task-finish | 复盘机制修复（当前复盘产出为零，docs/decisions/ 目录不存在） |

**task-finish 复盘改造详情**：

问题根因：
- 沉淀路径指错：全部存 memory，没有写入 `docs/decisions/`，和 CLAUDE.md "关键决策必须随 git 提交"矛盾
- 触发不够强制：大任务做完后容易跳过复盘直接 commit
- 只有重型模式：四维回顾对中等任务太重，导致干脆不做
- 没有闭环：复盘写了但下次做类似任务时没人看

改造方案：

```
自检通过后 → 强制判断复盘深度（不可跳过）
  │
  ├─ 小任务（≤2 文件，过程顺利）→ 跳过复盘
  │
  ├─ 中等任务（≤3 文件）→ 轻量复盘（3 个问题）
  │   ① 方案和实际的偏差在哪？
  │   ② 哪里返工了、为什么？
  │   ③ 下次怎么避免？
  │   → 写入 docs/decisions/YYYY-MM-DD-<主题>.md
  │
  └─ 大任务（3+ 文件 / 新模块 / 跨会话 / 过程曲折）→ 完整复盘
      四维回顾框架
      → 写入 docs/decisions/YYYY-MM-DD-<主题>.md
  
复盘写完后：
  ├─ docs/decisions/ 是真相源（随 git 提交）
  ├─ 从中提取 1-2 条关键经验存 memory（跨会话索引）
  └─ 更新 docs/decisions/INDEX.md
```

闭环机制：
```
task-start（检索 decisions/ 历史经验）→ task-execute → task-finish（产出新经验）
      ↑                                                       │
      └──────────────── docs/decisions/ ←──────────────────────┘
```

## 建议实施顺序

### 第一批（高频刚需）
1. security-audit — 上线门禁，最刚需
2. writing — 被多个 skill 依赖，基础设施
3. refactoring — 大改防翻车
4. code-walkthrough — 接手项目第一步

### 第二批（提效明显）
5. perf-profiling
6. release
7. tech-evaluation
8. dependency-map

### 第三批（日常辅助）
9. rapid-prototype
10. log-analysis
11. env-troubleshoot
12. task-manager
13. docs-management
14. learning-companion

### 收尾（改造现有 skill）
15. task-finish 改造 — 复盘机制修复，沉淀路径改为 docs/decisions/，增加轻量复盘模式
16. task-start 改造 — 方案写作委托给 writing skill + 对焦时检索 decisions/ 历史经验（依赖 writing skill 和 task-finish 改造完成后）

## 待记录

- 面试准备 skill：暂不做，后续有需要再启动
