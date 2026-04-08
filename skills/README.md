# Skills 技能体系

20 个 skill 覆盖从需求到上线的完整开发流程。采用**流程与能力分离**架构——流程 skill 负责调度"做什么"，能力 skill 负责"怎么做"。

> 精排 HTML 全景报告：`docs/reports/2026-04-08-skill-system-overview.html`

---

## 架构：流程 vs 能力分离

```
流程 skill（调度"做什么"）          能力 skill（负责"怎么做"）
─────────────────────────          ──────────────────────────
task-manager    需求管理             writing         通用写作
task-start      启动调度             deep-research   深度调研
task-execute    执行管理             tech-evaluation 技术选型
task-finish     提交自检             diagram         专业图表
refactoring     重构流程             code-walkthrough 代码导读
                                    dependency-map   依赖分析
                                    security-audit   安全审计
                                    perf-profiling   性能分析
                                    release          发版
                                    rapid-prototype  快速原型
                                    log-analysis     日志分析
                                    env-troubleshoot 环境排障
                                    docs-management  知识库引擎
                                    learning-companion 学习助手
                                    preview-md       MD 预览
```

---

## 需求状态驱动的工作流

以需求状态变更为核心驱动整个工作流：

```
task-manager: open → 收集需求、排优先级
                ↓ 决定做
task-manager: in-progress → task-start 启动
                ↓
            task-start → 对焦 + 方案调度
                ├─→ deep-research（调研）
                ├─→ tech-evaluation（选型）
                ├─→ rapid-prototype（原型验证）
                └─→ writing（写 spec / plan）
                ↓
            task-execute → 编码 + 进度管理
                ├─→ code-walkthrough（理解代码）
                ├─→ dependency-map（影响分析）
                └─→ refactoring（大规模重构）
                ↓
            task-finish → 每次提交前 CR 自检
                ├─→ security-audit（上线前安全审查）
                └─→ release（发版）
                ↓
            （手动测试、bug 修复、调整...可能多轮）
                ↓
task-manager: done → 需求彻底完成
                ├─ 复盘 → docs/decisions/
                ├─ Ingest → docs-management 更新文档
                └─ memory → 跨会话索引
```

### 需求状态

| 状态 | 含义 | INDEX 标记 | 触发行为 |
|------|------|-----------|---------|
| `open` | 待排期 | `[ ]` | 无 |
| `in-progress` | 开发中 | `[~]` | 方便跨会话跟踪 |
| `done` | 完成 | `[x]` | 触发复盘 + 经验沉淀 + Ingest |
| `dropped` | 放弃 | `~~删除线~~` | 记录原因 |

### 经验闭环

```
task-start（检索 decisions/ 历史经验）→ 执行 → task-manager 标 done（产出新经验）
      ↑                                                    │
      └──────────────── docs/decisions/ ←──────────────────┘
```

---

## Skill 完整清单

### 流程 Skill（5 个）

| Skill | 定位 | 触发词 |
|-------|------|--------|
| **task-manager** | 需求全生命周期管理（收集/排序/清理/关闭+复盘） | 梳理需求、排优先级、做完了 |
| **task-start** | 任务启动调度（对焦+调度写方案/选型/调研） | 新功能、实现xxx |
| **task-execute** | 跨会话大型任务进度管理 | 长期任务、继续 |
| **task-finish** | 提交前 CR 自检（快速/深度） | 提交代码、自检 |
| **refactoring** | 大规模重构流程（影响分析→安全网→分步→回归） | 重构、解耦、架构调整 |

### 能力 Skill — 安全与质量（2 个）

| Skill | 定位 | 触发词 |
|-------|------|--------|
| **security-audit** | AI 安全审查（注入/认证/敏感数据/配置/业务 5 维度） | 安全审计、上线前检查 |
| **perf-profiling** | 前后端性能分析（Core Web Vitals + API profiling） | 太慢了、性能优化 |

### 能力 Skill — 写作与表达（4 个）

| Skill | 定位 | 触发词 |
|-------|------|--------|
| **writing** | 通用写作（技术文档/产品文档/汇报精排HTML） | 写文档、写方案、写汇报 |
| **deep-research** | 深度调研 + 专业报告 | 调研、分析报告 |
| **tech-evaluation** | 技术选型决策（权重矩阵 + PoC） | 选哪个、A 还是 B |
| **diagram** | 专业图表（29 种，HTML/SVG/PNG） | 画图、图表 |

### 能力 Skill — 代码理解（2 个）

| Skill | 定位 | 触发词 |
|-------|------|--------|
| **code-walkthrough** | 代码导读（架构→流程→设计决策） | 帮我梳理、这块代码怎么运作 |
| **dependency-map** | 依赖分析（调用链+数据流+影响面） | 改这个会影响哪里 |

### 能力 Skill — 开发辅助（3 个）

| Skill | 定位 | 触发词 |
|-------|------|--------|
| **release** | 发版自动化（CalVer + changelog + GitHub Releases） | 发版、发布 |
| **rapid-prototype** | 快速原型（5 分钟可交互 HTML demo） | 快速出个 demo、验证一下 |
| **preview-md** | Markdown 浏览器预览（GitHub 风格 + 目录） | 预览文档 |

### 能力 Skill — 日常效率（4 个）

| Skill | 定位 | 触发词 |
|-------|------|--------|
| **log-analysis** | 日志分析（异常定位→时间线→根因） | 帮我看看日志 |
| **env-troubleshoot** | 环境排障（Node/Python/Docker） | 跑不起来、装不上 |
| **docs-management** | 知识库引擎（Ingest/Query/Lint/Index） | 文档检查、docs 整理 |
| **learning-companion** | 学习助手（按已有水平用类比教新技术） | 帮我学一下 |

---

## 版本管理

每个 skill 的 SKILL.md frontmatter 包含 `version` 和 `last_updated`。
变更记录在各自目录的 `CHANGELOG.md` 中。

**版本号规则（semver）**：
- **major**：破坏性变更
- **minor**：新功能
- **patch**：修复、改进
