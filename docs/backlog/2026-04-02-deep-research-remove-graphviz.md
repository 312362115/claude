---
priority: P2
status: open
spec:
plan:
---

# Deep-Research 清理 Graphviz 依赖 — 图表统一对齐 Diagram Skill

## 背景

Deep-Research skill 的图表生成目前有两套路径：
1. **统计图**：bridge.py（已对齐 Diagram skill）
2. **结构图**：generate_diagram.py（依赖 graphviz Python 包 + dot 命令）

Graphviz 是多余依赖，所有结构图已有 Diagram skill 的 HTML/SVG 模板 + capture.py 截图方案，应统一。

## 要做的事

### 1. SKILL.md 更新
- 第四步图表类型列表补齐新增类型（treemap/combo/kanban/git-graph）
- 结构图表列表补齐（state/ER/class/mindmap/gantt 等全部 29 种）
- 去掉任何 graphviz 相关描述

### 2. 删除 generate_diagram.py
- 结构图改用 capture.py + Diagram skill 模板
- 确认无其他文件引用 generate_diagram.py

### 3. setup_deps.py 清理
- 去掉 graphviz Python 包安装
- 去掉 graphviz 系统二进制（dot）安装

### 4. chart-styles.md 清理
- 去掉 5 处 `### graphviz 配置` 段落
- 统一引用 Diagram skill 的 design-system.md

## 影响范围

| 文件 | 改动 |
|------|------|
| `SKILL.md` | 更新图表类型列表 |
| `scripts/generate_diagram.py` | 删除 |
| `scripts/setup_deps.py` | 去 graphviz |
| `references/chart-styles.md` | 去 graphviz 配置段 |
