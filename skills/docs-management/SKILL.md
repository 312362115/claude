---
name: docs-management
version: 1.0.0
last_updated: 2026-04-08
repository: https://github.com/312362115/claude
description: >
  项目知识库引擎：持续维护 docs/ 目录作为活的知识库。
  灵感来源：Karpathy LLM Wiki — LLM 不只是写文档，而是持续维护知识库。
  四个核心操作：Ingest（摄入新信息）、Query（检索知识）、Lint（健康检查）、Index（索引维护）。
  触发词：文档检查、清理文档、文档索引、docs 整理、知识库、文档过期了吗。
  触发场景：task-manager 标 done 时自动触发 Ingest、定期 Lint 健检、用户查询项目历史。
  即使用户没有说"文档管理"，只要涉及 docs/ 目录的整理/检查/更新，都应触发此技能。
---

# 项目知识库引擎（Docs Management）

> "维护知识库最累的不是阅读和思考，是记账——交叉引用、一致性维护。这正是 LLM 擅长的。"
> — Karpathy, LLM Wiki

---

## 三层架构

```
Raw Sources（原始素材）  →  代码、git log、会议记录、外部文档
Wiki（知识库）           →  docs/ 目录下所有结构化文档
Schema（规则）           →  CLAUDE.md 中的文档规范
```

---

## 四个核心操作

### 操作 1：Ingest（摄入）

> 新信息进来时，不只是新建文件，而是找到已有文档合并更新。

**触发时机**：
- task-manager 标 done 时（复盘完成后自动触发）
- 新的设计决策产生时
- 外部信息需要整合到项目文档时

**执行流程**：

```
新信息产生
  │
  ├─ 搜索 docs/ 中是否有相关文档
  │   ├─ 有 → 更新已有文档，合并新信息
  │   └─ 无 → 创建新文档
  │
  ├─ 更新 docs/ 内相关交叉引用
  │
  └─ 更新 INDEX（如有）
```

**示例**：
- task-finish 产出复盘 → 写入 `docs/decisions/`，同时检查对应的 spec 是否需要标注"方案已执行，实际偏差见 decisions/xxx"
- 发现新的最佳实践 → 更新 `docs/guides/` 相关指南

### 操作 2：Query（查询）

> docs/ 是项目的可查询知识库，不是文件堆。

**触发时机**：
- 用户问"这个模块之前怎么设计的？"
- 用户问"上次类似问题怎么解的？"
- task-start 对焦阶段检索历史经验

**执行流程**：

```
查询请求
  │
  ├─ 在 docs/ 中搜索相关文档
  │   ├─ specs/ — 设计方案
  │   ├─ decisions/ — 踩坑记录和经验
  │   ├─ plans/ — 历史开发计划
  │   ├─ tests/ — 测试用例
  │   └─ guides/ — 开发指南
  │
  ├─ 综合相关文档给出回答
  │
  └─ 如果回答有价值且不在现有文档中 → Ingest 回 wiki
```

### 操作 3：Lint（健康检查）

> 定期体检，防止文档腐烂。

**触发时机**：
- 用户主动要求检查
- 大批量代码改动后
- 定期维护

**检查清单**：

| # | 检查项 | 怎么查 | 问题示例 |
|---|--------|--------|---------|
| 1 | **引用有效性** | 文档中引用的文件路径是否存在 | spec 引用了已删除的文件 |
| 2 | **进度一致性** | plan 的 checklist 和实际代码是否一致 | plan 说"待做"但代码已完成 |
| 3 | **INDEX 同步** | INDEX.md 和实际文件是否对得上 | INDEX 有但文件已删 |
| 4 | **跨文档一致** | plan 引用的 spec 是否存在 | plan 指向不存在的 spec |
| 5 | **状态同步** | backlog 状态和实际进度是否匹配 | backlog open 但 plan 已全部完成 |
| 6 | **孤立文档** | 有没有不被任何 INDEX 或文档引用的文件 | 遗忘的旧 spec |
| 7 | **过期内容** | 文档描述的代码结构是否还存在 | spec 说"改 src/old.ts"但该文件已重命名 |
| 8 | **记忆巡检** | memory 中的条目是否仍然有效 | feedback 引用的模块已删除、project 信息已过期 |

**输出格式**：

```markdown
## Docs 健康检查报告 — YYYY-MM-DD

### 概况
- 扫描目录：docs/
- 文档总数：X 个
- 发现问题：X 个

### 问题清单

| # | 级别 | 文件 | 问题 | 建议 |
|---|------|------|------|------|
| 1 | 高 | plans/xxx.md | 引用的 spec 不存在 | 更新引用或补建 spec |
| 2 | 中 | specs/xxx.md | 引用的文件路径 src/old.ts 已不存在 | 更新路径 |
| 3 | 低 | backlog/xxx.md | 状态 open 但关联 plan 已全部完成 | 更新为 done |
```

### 操作 4：Index（索引维护）

> 索引是知识库的入口，必须和实际内容同步。

**维护对象**：
- `docs/backlog/INDEX.md` — 需求索引（已有，由 task-manager 维护）
- `docs/decisions/INDEX.md` — 经验索引（待建，按时间倒序）

**INDEX 更新时机**：
- 新建文档后
- 文档状态变更后
- Lint 发现不一致后

---

## 与其他 skill 的关系

```
task-finish（复盘产出）→ docs-management.Ingest（整合到知识库）
task-start（对焦阶段）→ docs-management.Query（检索历史经验）
task-manager（需求管理）→ docs-management.Index（维护 backlog INDEX）

定期 / 用户主动 → docs-management.Lint（健康检查）
```

**docs-management vs writing**：
- writing：**生产**文档（从无到有写出来）
- docs-management：**维护**文档（确保已有文档保持健康和可用）

**docs-management vs task-manager**：
- task-manager：专门管 backlog（需求的收集/排序/清理）
- docs-management：管整个 docs/ 目录（包括 backlog 之外的 specs/plans/decisions/等）
