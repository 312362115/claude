# 画图 Skill 示例重构计划

## 关联
- 方案：docs/specs/2026-03-26-diagram-skill-design.md

## 背景

原始示例文件散落在 `diagram-examples/` 目录，与 skill 结构脱离。需要：
1. 将示例源文件迁移到 `skills/diagram/templates/` 作为正式模板
2. 更新 spec 文件的模板引用路径
3. 补充缺失的 ECharts spec 文件

## 子任务

- [x] 1. D2 模板迁移（5 个新增，2 个已有）
  - 做什么：将 `diagram-examples/d2/` 中的 state、er、network、decision-tree、dataflow 迁移到 `templates/d2/`
  - 涉及：`skills/diagram/templates/d2/`（新增 5 个文件）
  - 验收：7 个 D2 模板齐全

- [x] 2. Mermaid 模板迁移（9 个）
  - 做什么：将 `diagram-examples/mermaid/` 全部迁移到 `templates/mermaid/`
  - 涉及：`skills/diagram/templates/mermaid/`（新增 9 个文件）
  - 验收：9 个 Mermaid 模板齐全

- [x] 3. HTML 模板迁移（11 个）
  - 做什么：将 `diagram-examples/custom/` 和 `diagram-examples/html/` 迁移到 `templates/html/`
  - 涉及：`skills/diagram/templates/html/`（新增 11 个文件）
  - 验收：11 个 HTML 模板齐全

- [x] 4. ECharts 模板迁移（6 个）
  - 做什么：将 `diagram-examples/echarts/` 迁移到 `templates/echarts/`
  - 涉及：`skills/diagram/templates/echarts/`（新增 6 个文件）
  - 验收：6 个 ECharts 模板齐全

- [x] 5. Spec 文件旧路径修正（5 个）
  - 做什么：swot、fishbone、orgchart、venn、journey 的 `diagram-examples/` 引用改为 `templates/`
  - 涉及：`skills/diagram/references/diagrams/` 下 5 个文件
  - 验收：无 `diagram-examples/` 引用残留

- [x] 6. Spec 文件新增模板引用（13 个）
  - 做什么：给 state、er、network、decision-tree、dataflow、class、c4、mindmap、gantt、timeline、swimlane、sequence、architecture 添加/修正模板引用
  - 涉及：`skills/diagram/references/diagrams/` 下 13 个文件
  - 验收：每个 spec 都有 `## 模板` 章节指向正确的模板路径

- [x] 7. 新建 ECharts spec 文件（7 个）
  - 做什么：创建 bar-chart、line-chart、pie-chart、radar-chart、heatmap、sankey、scatter 的 spec
  - 涉及：`skills/diagram/references/diagrams/`（新增 7 个文件）
  - 验收：SKILL.md 引用的 26 个 spec 全部存在

- [ ] 8. 补充 scatter 散点图模板
  - 做什么：创建散点图 ECharts 示例模板
  - 涉及：`skills/diagram/templates/echarts/scatter.html`（新建）
  - 验收：scatter spec 有可用模板

- [ ] 9. 清理 diagram-examples 旧目录
  - 做什么：确认所有内容已迁移后，删除 `diagram-examples/` 目录
  - 涉及：`~/.claude/diagram-examples/`（删除）
  - 验收：旧目录不存在，所有引用指向 `templates/`
