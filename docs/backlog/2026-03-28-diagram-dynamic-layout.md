---
priority: P1
status: open
spec:
plan:
---

# 画图 Skill 第二阶段：全模板动态布局引擎

## 背景

第一阶段完成了 26 个图表类型的 HTML/SVG 模板和统一设计规范。但当前有 11 个模板（class、orgchart、flowchart、er、sequence、state、swimlane、fishbone、architecture、swot、venn）使用硬编码坐标，无法适应不同数据量的真实场景。

## 目标

所有模板改为 JS 动态布局，传入数据即可自动生成美观、不重叠的图表。

## 关键任务

1. **静态模板 → 动态布局**：11 个硬编码模板全部改为 JS 计算坐标
   - 节点宽度根据文字内容动态计算
   - 节点位置由布局算法自动分配
   - 画布尺寸由内容撑开

2. **布局约束系统**：写入设计规范
   - 最小间距约束（节点间 ≥ 40px，层间 ≥ 60px）
   - 防碰撞检测：渲染后检测重叠，自动调整
   - 连线路由：避开节点，不穿越

3. **SKILL.md 生成指导**：明确"参考模板风格 + JS 动态生成"的工作方式
   - 不是"填模板"，而是"按规范写布局代码"
   - 提供各图表类型的布局算法参考（树形、网格、径向等）

4. **验证机制**：生成后自动截图 + 检查尺寸/内容是否正常

## 已有的动态模板（可参考）

mindmap、pie、radar、bar、line、scatter、heatmap、sankey、timeline、gantt、c4、decision-tree、dataflow、network、orgchart（15 个已经是动态的）
