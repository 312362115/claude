# 画图 Skill 动态布局引擎开发计划

## 关联
- 方案：docs/specs/2026-03-28-diagram-dynamic-layout-design.md

## 子任务

- [x] 1. 公共工具库设计与实现
  - 做什么：实现 diagram-utils 标准函数集（measureText、calcNodeSize、isOverlap、findOverlaps、connectNodes、calcCanvasSize、validateDiagram）
  - 涉及：`skills/diagram/references/diagram-utils.md`（规范文档），可在任意模板中验证
  - 验收：用 flowchart 模板验证工具函数可用，碰撞检测和画布自适应工作正常

- [ ] 2. 配色方案系统
  - 做什么：定义 theme 对象结构，将 default 配色从 design-system.md 提取为标准 theme 对象，文档化 theme 接口
  - 涉及：`skills/diagram/references/design-system.md`（更新配色章节），`skills/diagram/references/themes.md`（新建）
  - 验收：theme 对象结构定义完成，default 主题覆盖所有组件颜色

- [x] 3. P0 — flowchart 动态布局
  - 做什么：改造为 JS 动态布局，支持任意数量的步骤/判断/分支，使用公共工具库 + 线性布局算法
  - 涉及：`skills/diagram/templates/html/flowchart.html`（重写），`skills/diagram/references/diagrams/flowchart.md`（更新）
  - 验收：✅ 4 种场景验证通过（简单 4 步 / 中等 8 步 2 判断 / 复杂 12 步 3 判断 / 超级复杂 15 步 4 判断），均无重叠无截断，画布自适应

- [x] 4. P0 — sequence 动态布局
  - 做什么：改造为 JS 动态布局，支持任意数量参与者和消息，含 fragment（loop/alt/opt/par/break）
  - 涉及：`skills/diagram/templates/html/sequence.html`（重写）
  - 验收：✅ 6 参与者 12 消息 + alt fragment + 自调用 + database 圆柱体，均正常

- [ ] 5. P0 — er 动态布局
  - 做什么：改造为 JS 动态布局，支持任意数量表和关系，使用公共工具库 + 网格布局算法
  - 涉及：`skills/diagram/templates/html/er.html`（重写）
  - 验收：传入 3 表 / 6 表 / 10 表含多对多关系，均无重叠，连线不穿越表

- [ ] 6. P1 — class 动态布局
  - 做什么：改造为 JS 动态布局，支持任意数量类/枚举/接口和关系
  - 涉及：`skills/diagram/templates/html/class.html`（重写）
  - 验收：传入 4 类 / 9 类含枚举 / 15 类复杂继承关系，均正常

- [ ] 7. P1 — architecture 动态布局
  - 做什么：改造为 JS 动态布局，支持任意层数和每层任意节点数，自动换行
  - 涉及：`skills/diagram/templates/html/architecture.html`（重写）
  - 验收：传入 4 层每层 3 节点 / 7 层含多行 / 层名和节点名长短不一，均正常

- [ ] 8. P1 — swimlane 动态布局
  - 做什么：改造为 JS 动态布局，支持任意泳道数量和流程步骤
  - 涉及：`skills/diagram/templates/html/swimlane.html`（重写）
  - 验收：传入 3 泳道 / 5 泳道含跨泳道判断 / 复杂审批流程，均正常

- [ ] 9. P2 — state 动态布局
  - 做什么：改造为 JS 动态布局，支持任意状态数和转换关系
  - 涉及：`skills/diagram/templates/html/state.html`（重写）
  - 验收：传入 4 状态 / 8 状态含自循环 / 并行状态，均正常

- [ ] 10. P2 — fishbone / swot / venn / journey 动态布局
  - 做什么：4 个卡片类模板改为内容动态填充（骨架固定，文字/条目数量自适应）
  - 涉及：4 个 HTML 模板（重写）
  - 验收：传入不同数量的条目（少量 3 条 / 中量 6 条 / 多量 10 条），布局自适应无溢出

- [ ] 11. 通用兜底布局引擎
  - 做什么：实现通用布局算法，自动识别数据结构（树形/分层/网格/自由），选择最合适的布局
  - 涉及：`skills/diagram/references/generic-layout.md`（新建）
  - 验收：传入一个未知类型的图结构数据，能生成可用的图表

- [ ] 12. 验证检查系统
  - 做什么：实现 validateDiagram() 和自动修正逻辑，集成到生成流程
  - 涉及：公共工具库（补充验证函数），`skills/diagram/references/diagram-utils.md`（更新）
  - 验收：故意传入会导致重叠的数据，验证系统能检测到并自动修正

- [ ] 13. SKILL.md 更新
  - 做什么：更新生成流程说明，明确"数据→布局→验证→截图"的工作方式，补充配色方案切换指导
  - 涉及：`skills/diagram/SKILL.md`（更新）
  - 验收：新的 SKILL.md 能指导 Claude 正确使用动态布局生成图表

- [ ] 14. 回归测试
  - 做什么：用 26 种图表各跑一次真实数据生成，截图对比确认质量不低于第一阶段
  - 涉及：`docs/tests/diagram-regression.md`（新建），`docs/assets/`（更新截图）
  - 验收：26 张截图全部通过人工 review，gallery 文档更新
