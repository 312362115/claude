## 技术方案：Diagram Bridge — JSON → PNG/HTML 桥接脚本

### 1. 背景与目标

Deep-Research 当前用 matplotlib/graphviz（115MB venv）生成图表，与 Diagram skill 的 HTML+SVG 体系并行，存在两套设计系统。

- **目标**：用一个桥接脚本 `bridge.py`，让 Deep-Research 通过 JSON 配置直接调用 Diagram 模板生成图表
- **验收标准**：`python bridge.py --type pie --config data.json --output chart.png` 一行命令出图
- **不做**：修改 Diagram 模板本身、不改变 Diagram skill 的直接使用方式

### 2. 现状分析

Deep-Research 图表生成：
- `generate_chart.py`（463 行）— matplotlib 统计图
- `generate_diagram.py`（301 行）— graphviz 结构图
- `setup_deps.py`（94 行）— venv 安装脚本
- `.venv/`（115MB）— Python 依赖

Diagram skill 已覆盖的图表类型：25 种，全部用 HTML+SVG+Playwright。

### 3. 方案设计

**核心思路**：bridge.py 读取 JSON 配置 → 生成数据注入的 HTML → Playwright 截图为 PNG。

**JSON 配置格式**（每种图表类型一个 schema）：

```json
{
  "type": "bar",
  "title": "Redis vs Memcached 性能对比",
  "subtitle": "ops/sec",
  "data": {
    "categories": ["读取", "写入", "混合"],
    "series": [
      {"name": "Redis", "values": [100000, 80000, 85000]},
      {"name": "Memcached", "values": [95000, 85000, 82000]}
    ]
  }
}
```

**支持的图表类型**（Deep-Research 常用）：

| 类型 | JSON data 结构 |
|------|--------------|
| bar | categories + series[{name, values}] |
| line | categories + series[{name, values}] |
| pie | items[{name, value}] |
| radar | labels + series[{name, values}] |
| heatmap | xLabels + yLabels + data[[x,y,v]...] |
| scatter | series[{name, data[[x,y]...]}] |
| funnel | stages[{name, value}] |
| waterfall | items[{name, value, type}] |

**调用方式**：

```bash
# JSON 文件输入
python bridge.py --type bar --config data.json --output chart.png

# 也支持 HTML 输出
python bridge.py --type bar --config data.json --output chart.html --format html

# 管道输入（Claude 直接传 JSON）
echo '{"type":"pie","title":"市场份额",...}' | python bridge.py --output chart.png
```

### 4. 实施计划

- [x] 1. 创建 `skills/diagram/scripts/bridge.py`（JSON → HTML → PNG）
- [ ] 2. 重写 `deep-research/SKILL.md` 第四步
- [ ] 3. 验证：用 bridge.py 生成 8 种典型图表（已完成）
- [ ] 4. 实战验证：在真实 deep-research 调研中跑通 bridge 图表生成
- [ ] 5. 旧脚本清理（待实战验证通过后再决定）

### 5. 风险与边界

- 风险：模板数据格式变化时 bridge 需要同步更新 → 用回归测试覆盖
- 不做：所有 25 种图表类型都支持 bridge（先做 8 种统计图，结构图仍由 Claude 直接写 HTML）
