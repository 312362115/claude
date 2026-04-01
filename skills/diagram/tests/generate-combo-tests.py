"""生成 combo L1-L4 测试 HTML 文件"""
import re
import os

if not os.path.exists('lib'):
    os.symlink('../templates/html/lib', 'lib')

with open('../templates/html/combo.html', 'r') as f:
    template = f.read()

# 提取引擎（从 配色 到文件末尾）
engine_match = re.search(r'(  // ========== 配色 ==========.*)</script>\n</body>\n</html>', template, re.DOTALL)
engine = engine_match.group(1)

header = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, system-ui, 'PingFang SC', sans-serif; background: #fff; display: flex; flex-direction: column; align-items: center; }
  .title { font-size: 22px; font-weight: 700; color: #1a1a2e; margin-top: 28px; }
  .subtitle { font-size: 14px; color: #888; margin-top: 6px; }
  .chart-wrap { margin-top: 20px; position: relative; }
</style>
<script src="lib/utils.js"></script>
</head>
<body>
<div class="title" id="title"></div>
<div class="subtitle" id="subtitle"></div>
<div class="chart-wrap">
  <svg id="canvas"></svg>
</div>
<script>
(function() {
  var svg = document.getElementById('canvas');
  var SANS = "-apple-system, system-ui, 'PingFang SC', sans-serif";

'''

tail = '</script>\n</body>\n</html>\n'

L1 = '''
  document.getElementById('title').textContent = '销售额对比';
  document.getElementById('subtitle').textContent = 'L1 简单 · 2 类别 · 1 柱状系列';
  var data = {
    categories: ['线上', '线下'],
    series: [
      { name: '销售额（万元）', type: 'bar', values: [85, 120] }
    ]
  };
'''

L2 = '''
  document.getElementById('title').textContent = '季度营收与利润率';
  document.getElementById('subtitle').textContent = 'L2 中等 · 4 类别 · 2 柱 + 1 折线';
  var data = {
    categories: ['Q1', 'Q2', 'Q3', 'Q4'],
    series: [
      { name: '营收（万元）', type: 'bar', values: [120, 150, 180, 200] },
      { name: '成本（万元）', type: 'bar', values: [80, 95, 110, 120] },
      { name: '利润率', type: 'line', values: [0.33, 0.37, 0.39, 0.40], yAxis: 'right', format: 'percent' }
    ]
  };
'''

L3 = '''
  document.getElementById('title').textContent = '上半年营收与增长趋势';
  document.getElementById('subtitle').textContent = 'L3 复杂 · 6 类别 · 2 柱 + 2 折线 · 双 Y 轴';
  var data = {
    categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    series: [
      { name: '产品A（万元）', type: 'bar', values: [90, 105, 130, 145, 160, 175] },
      { name: '产品B（万元）', type: 'bar', values: [60, 72, 85, 93, 110, 125] },
      { name: '同比增长', type: 'line', values: [0.12, 0.15, 0.18, 0.22, 0.25, 0.28], yAxis: 'right', format: 'percent' },
      { name: '环比增长', type: 'line', values: [0.05, 0.08, 0.11, 0.09, 0.13, 0.10], yAxis: 'right', format: 'percent' }
    ]
  };
'''

L4 = '''
  document.getElementById('title').textContent = '全年业务数据总览';
  document.getElementById('subtitle').textContent = 'L4 超级复杂 · 12 类别 · 3 柱 + 2 折线 · 大数据集';
  var data = {
    categories: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
    series: [
      { name: '华东区（万元）', type: 'bar', values: [320, 280, 350, 390, 420, 450, 480, 460, 500, 530, 560, 620] },
      { name: '华南区（万元）', type: 'bar', values: [210, 195, 240, 265, 290, 310, 330, 315, 350, 370, 390, 430] },
      { name: '华北区（万元）', type: 'bar', values: [150, 135, 170, 190, 210, 225, 245, 230, 260, 275, 295, 330] },
      { name: '整体增长率', type: 'line', values: [0.08, 0.06, 0.12, 0.15, 0.18, 0.20, 0.22, 0.19, 0.24, 0.26, 0.28, 0.32], yAxis: 'right', format: 'percent' },
      { name: '目标达成率', type: 'line', values: [0.85, 0.78, 0.92, 0.95, 0.98, 1.02, 1.05, 0.99, 1.08, 1.10, 1.12, 1.18], yAxis: 'right', format: 'percent' }
    ]
  };
'''

test_data = {'L1': L1, 'L2': L2, 'L3': L3, 'L4': L4}

for level, data in test_data.items():
    content = header + data + '\n' + engine + tail
    filename = f'combo-{level}.html'
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
