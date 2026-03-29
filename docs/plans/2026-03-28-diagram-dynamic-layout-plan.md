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
  - 做什么：手动布局（主路径向下+否分支右侧）+ 分组背景overlay
  - 涉及：`skills/diagram/templates/html/flowchart.html`
  - 验收：✅ L2 通过

- [x] 4. P0 — sequence 动态布局
  - 做什么：改造为 JS 动态布局，支持任意数量参与者和消息，含 fragment（loop/alt/opt/par/break）
  - 涉及：`skills/diagram/templates/html/sequence.html`（重写）
  - 验收：✅ 6 参与者 12 消息 + alt fragment + 自调用 + database 圆柱体，均正常

- [x] 5. P0 — er 动态布局
  - 做什么：ELKjs layered 布局，支持任意数量表和关系
  - 涉及：`skills/diagram/templates/html/er.html`（重写）
  - 验收：✅ L2 通过（6 表 5 关系），L1/L3/L4 待验证

- [x] 6. P1 — class 动态布局
  - 做什么：ELKjs layered 布局，支持类/枚举/接口和多种关系类型
  - 涉及：`skills/diagram/templates/html/class.html`（重写）
  - 验收：✅ L2 通过（6 类 3 枚举 8 关系）

- [x] 7. P1 — architecture 动态布局
  - 做什么：手动层堆叠（预定义层序），无箭头，间距紧凑
  - 涉及：`skills/diagram/templates/html/architecture.html`
  - 验收：✅ L2 通过

- [x] 8. P1 — swimlane 动态布局
  - 做什么：手动网格布局（列×行），泳道高度独立，箭头缩小
  - 涉及：`skills/diagram/templates/html/swimlane.html`
  - 验收：✅ L2 通过

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
