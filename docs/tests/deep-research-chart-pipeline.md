# Deep-Research 图表生成链路验证

> 最近执行：2026-04-02 10:18

## 结果：42/42 passed

### 统计图 HTML（bridge.py → HTML）（10/10）

| 图表类型 | 状态 | 详情 |
|---------|------|------|
| bar | ✅ | html 5KB |
| line | ✅ | html 5KB |
| pie | ✅ | html 8KB |
| radar | ✅ | html 5KB |
| heatmap | ✅ | html 6KB |
| scatter | ✅ | html 6KB |
| funnel | ✅ | html 5KB |
| waterfall | ✅ | html 6KB |
| treemap | ✅ | html 10KB |
| combo | ✅ | html 9KB |

### 统计图 PNG（bridge.py → PNG）（3/3）

| 图表类型 | 状态 | 详情 |
|---------|------|------|
| bar | ✅ | png 51KB |
| pie | ✅ | png 53KB |
| radar | ✅ | png 95KB |

### 结构图 PNG（capture.py → PNG）（29/29）

| 图表类型 | 状态 | 详情 |
|---------|------|------|
| architecture-L1 | ✅ | png 32KB |
| c4-L1 | ✅ | png 96KB |
| class-L1 | ✅ | png 74KB |
| combo-L1 | ✅ | png 48KB |
| dataflow-L1 | ✅ | png 19KB |
| decision-tree-L1 | ✅ | png 29KB |
| er-L1 | ✅ | png 73KB |
| fishbone-L1 | ✅ | png 57KB |
| flowchart-L1 | ✅ | png 35KB |
| funnel-L1 | ✅ | png 77KB |
| gantt-L1 | ✅ | png 71KB |
| git-graph-L1 | ✅ | png 27KB |
| heatmap-L1 | ✅ | png 65KB |
| journey-L1 | ✅ | png 44KB |
| kanban-L1 | ✅ | png 52KB |
| mindmap-L1 | ✅ | png 75KB |
| network-L1 | ✅ | png 38KB |
| orgchart-L1 | ✅ | png 45KB |
| pie-L1 | ✅ | png 73KB |
| radar-L1 | ✅ | png 98KB |
| sankey-L1 | ✅ | png 741KB |
| sequence-L1 | ✅ | png 65KB |
| state-L1 | ✅ | png 27KB |
| swimlane-L1 | ✅ | png 36KB |
| swot-L1 | ✅ | png 62KB |
| timeline-L1 | ✅ | png 60KB |
| treemap-L1 | ✅ | png 39KB |
| venn-L1 | ✅ | png 74KB |
| waterfall-L1 | ✅ | png 58KB |

## 执行命令

```bash
python skills/deep-research/tests/verify-chart-pipeline.py        # 全量
python skills/deep-research/tests/verify-chart-pipeline.py --quick # 仅 HTML
```
