# Claude Code Skills

[![GitHub Stars](https://img.shields.io/github/stars/312362115/claude?style=social)](https://github.com/312362115/claude/stargazers)&nbsp;&nbsp;
[![GitHub Forks](https://img.shields.io/github/forks/312362115/claude?style=social)](https://github.com/312362115/claude/network/members)&nbsp;&nbsp;
[![GitHub Issues](https://img.shields.io/github/issues/312362115/claude)](https://github.com/312362115/claude/issues)&nbsp;&nbsp;
[![License](https://img.shields.io/github/license/312362115/claude)](https://github.com/312362115/claude/blob/main/LICENSE)

> **做好比做完重要** — 以字节范（ByteStyle）核心价值观驱动的 AI 辅助开发体系

一套围绕 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 构建的专业开发工作流，包含 **20 个自研技能**，覆盖从需求管理到上线发版的完整开发生命周期。让 Claude 从代码助手进化为全流程开发伙伴。

---

## 核心亮点

- **需求驱动的工作流** — 以需求状态流转（open → in-progress → done）为核心，需求关闭时自动触发复盘和经验沉淀，形成闭环
- **流程与能力分离** — 5 个流程 skill 负责调度"做什么"，15 个能力 skill 负责"怎么做"，可独立使用也可组合
- **29 种专业图表** — 流程图、ER 图、架构图、雷达图、桑基图、热力图等，统一设计规范
- **深度调研引擎** — 假设驱动、多跳搜索、交叉验证，输出专业研究报告（MD / HTML）
- **AI 安全审查** — 注入防护、认证授权、敏感数据、配置安全、业务安全 5 个维度
- **通用写作能力** — 技术文档 / 产品文档 / 项目汇报（精排 HTML），7 个文档模板
- **知识库引擎** — 参考 Karpathy LLM Wiki，Ingest 摄入 + Query 查询 + Lint 健检 + Index 索引
- **经验闭环** — 复盘沉淀到 `docs/decisions/`，下次新任务自动检索历史经验，避免重复踩坑

---

## 快速开始

### 安装

打开 Claude Code，直接告诉它：

```
帮我把 https://github.com/312362115/claude 仓库里的 skills/ 目录
安装到我的 ~/.claude/skills/ 下
```

所有依赖已内联打包，无需额外安装。

### 使用

斜杠命令或自然语言触发：

```
/task-start          # 启动新任务
/diagram             # 生成专业图表
/deep-research       # 深度调研报告
```

```
"帮我画一个系统架构图"        → 自动触发 diagram
"调研一下 React vs Vue"      → 自动触发 deep-research
"帮我写个技术方案"            → 自动触发 writing
"这块代码帮我梳理一下"        → 自动触发 code-walkthrough
"安全审计一下"                → 自动触发 security-audit
"这个需求做完了"              → 自动触发 task-manager（复盘 + 沉淀）
```

---

## 工作流

以需求状态变更为核心驱动整个开发流程：

```
open ──→ in-progress ──→ done
 │           │              │
 │           │              └─ 触发：复盘 + 经验沉淀 + 文档更新
 │           └─ task-start 启动时标记
 └──→ dropped
```

```
task-manager    决定做哪个需求
      ↓
task-start      对焦需求 → 调度调研/选型/原型/写方案
      ↓
task-execute    编码 → 可调用 code-walkthrough / dependency-map / refactoring
      ↓
task-finish     每次提交前 CR 自检
      ↓
task-manager    需求标 done → 复盘 → docs/decisions/ → 经验闭环
      ↓
release         发版（CalVer + changelog + GitHub Releases）
```

---

## 20 个 Skill 一览

### 流程 Skill（5 个）

| Skill | 定位 |
|-------|------|
| **task-manager** | 需求全生命周期管理（收集 / 排序 / 清理 / 关闭 + 复盘） |
| **task-start** | 任务启动调度（对焦 + 调度调研/选型/写方案） |
| **task-execute** | 跨会话大型任务持续执行 |
| **task-finish** | 提交前 CR 自检（快速 / 深度） |
| **refactoring** | 大规模重构（影响分析 → 安全网 → 分步重构 → 回归） |

### 能力 Skill（15 个）

| 领域 | Skill | 定位 |
|------|-------|------|
| **安全质量** | security-audit | AI 安全审查（5 个维度） |
| | perf-profiling | 前后端性能分析 |
| **写作表达** | writing | 通用写作（技术文档 / 产品文档 / 汇报 HTML） |
| | deep-research | 深度调研 + 专业报告 |
| | tech-evaluation | 技术选型决策 |
| | diagram | 29 种专业图表 |
| **代码理解** | code-walkthrough | 代码导读，建立心智模型 |
| | dependency-map | 依赖分析，影响面评估 |
| **开发辅助** | release | 发版自动化（CalVer） |
| | rapid-prototype | 5 分钟可交互 HTML demo |
| | preview-md | Markdown 浏览器预览 |
| **日常效率** | log-analysis | 日志分析（异常 → 时间线 → 根因） |
| | env-troubleshoot | 环境排障（Node / Python / Docker） |
| | docs-management | 知识库引擎（参考 Karpathy LLM Wiki） |
| | learning-companion | 学习助手（按已有水平定制教学） |

> 详细文档见 [skills/README.md](skills/README.md) | 精排 HTML 全景报告见 [docs/reports/](docs/reports/)

---

## 图表能力

覆盖 **29 种图表**，统一设计规范，三种输出格式：

| 格式 | 支持图表 | 适用场景 |
|------|---------|---------|
| **Mermaid DSL** | 20+ 种（流程图、时序图、ER 图、甘特图...） | 日常文档，可版本控制 |
| **PNG** | 全部 29 种 | PPT、邮件附件 |
| **HTML** | 全部 29 种 | 交互式展示 |

```
> 画一个用户注册的流程图
> 帮我生成一个技术选型的雷达图
> 画个数据库 ER 图
```

---

## 调研报告

对任意命题进行系统性调研，支持 **Markdown**（日常）和 **HTML**（正式交付）两种输出：

- 假设驱动研究 + 多跳网络搜索
- 数据来源三级分类（一手 / 二手 / 三手）
- 反面证据强制搜索 + 结论置信度分级
- 自动生成配套图表嵌入报告

```
> 调研一下目前主流的前端状态管理方案
> 做个 Supabase vs Firebase 的对比分析
```

---

## 项目结构

```
~/.claude/
├── CLAUDE.md                # 全局开发规范（字节范 ByteStyle）
├── skills/                  # 20 个自研技能
│   ├── task-manager/        #   需求管理（含复盘）
│   ├── task-start/          #   任务启动调度
│   ├── task-execute/        #   持续执行
│   ├── task-finish/         #   提交前自检
│   ├── refactoring/         #   重构流程
│   ├── security-audit/      #   安全审查
│   ├── writing/             #   通用写作（含 7 个模板 + HTML 汇报模板）
│   ├── deep-research/       #   深度调研
│   ├── tech-evaluation/     #   技术选型
│   ├── diagram/             #   图表生成（29 种）
│   ├── code-walkthrough/    #   代码导读
│   ├── dependency-map/      #   依赖分析
│   ├── perf-profiling/      #   性能分析
│   ├── release/             #   发版自动化
│   ├── rapid-prototype/     #   快速原型
│   ├── preview-md/          #   MD 预览
│   ├── log-analysis/        #   日志分析
│   ├── env-troubleshoot/    #   环境排障
│   ├── docs-management/     #   知识库引擎
│   ├── learning-companion/  #   学习助手
│   └── shared/              #   共享样式
├── docs/                    # 项目文档
│   ├── backlog/             #   需求池
│   ├── specs/               #   方案设计
│   ├── plans/               #   开发计划
│   ├── decisions/           #   复盘记录（经验真相源）
│   ├── audits/              #   安全审计报告
│   ├── reports/             #   汇报
│   ├── tests/               #   测试用例
│   └── guides/              #   开发指南
└── extensions/              # VS Code 扩展
    └── preview-md-launcher/ #   MD 浏览器预览插件
```

---

## 依赖

- **[ELKjs](https://github.com/kieler/elkjs)** — 图布局引擎，已内联打包
- **[Playwright MCP](https://github.com/microsoft/playwright-mcp)** — HTML → PNG 截图

---

## Star History

<p align="center">
  <img src="https://api.star-history.com/svg?repos=312362115/claude&type=Date" alt="Star History Chart" width="600">
</p>

---

## 许可证

[MIT](LICENSE)
