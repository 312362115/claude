"""生成 radar L1-L4 测试 HTML 文件"""

# 读取模板
with open('../templates/html/radar.html', 'r') as f:
    template = f.read()

# radar 模板的 legend 随数据变化，所以每个级别构建完整 HTML

# 提取 CSS 样式部分（从开头到 </style> 后）
import re
style_match = re.search(r'(.*</style>\n)', template, re.DOTALL)
html_style = style_match.group(1)

# 提取引擎部分：从 function pt(...) 到 </script>
engine_match = re.search(r'(function pt\(.*)</script>', template, re.DOTALL)
engine = engine_match.group(1)

tail = '</script>\n</body>\n</html>\n'

def make_legend_html(series_list):
    """生成 legend div HTML"""
    items = []
    for s in series_list:
        items.append(f'    <div class="legend-item">\n'
                     f'      <div class="legend-rect" style="background: {s["color"]}"></div>{s["legend"]}\n'
                     f'    </div>')
    return '  <div class="legend">\n' + '\n'.join(items) + '\n  </div>'

def make_html(legend_html, data_js):
    body = (f'</head>\n'
            f'<body class="fixed-1200">\n'
            f'  <div class="title">技术方案评估对比</div>\n'
            f'  <div class="subtitle">多维度综合评分（满分 100）</div>\n'
            f'{legend_html}\n'
            f'\n'
            f'  <div class="chart-wrap">\n'
            f'    <svg id="radar" width="1100" height="640" viewBox="0 0 1100 640"></svg>\n'
            f'  </div>\n'
            f'\n'
            f'<script src="lib/utils.js"></script>\n'
            f'<script>\n'
            f'{data_js}\n'
            f'{engine}'
            f'{tail}')
    return html_style + body

# L1: 4 axes, 1 series（最简）
L1_series = [
    {'color': 'rgba(102,126,234,0.7)', 'legend': '方案 A — 微服务'}
]
L1_data = '''const svg = document.getElementById('radar');

const cx = 500, cy = 310, R = 220;
const axes = 4;
const levels = 5;
const labels = ['性能', '可维护性', '扩展性', '安全性'];

const series = [
  { name: 'A', values: [90, 70, 95, 85], color: 'rgba(102,126,234,0.8)', fill: 'rgba(102,126,234,0.12)' }
];
'''

# L2: 6 axes, 3 series（默认模板数据）
L2_series = [
    {'color': 'rgba(102,126,234,0.7)', 'legend': '方案 A — 微服务'},
    {'color': 'rgba(245,87,108,0.7)', 'legend': '方案 B — Serverless'},
    {'color': 'rgba(67,233,123,0.7)', 'legend': '方案 C — 单体优化'}
]
L2_data = '''const svg = document.getElementById('radar');

const cx = 500, cy = 310, R = 220;
const axes = 6;
const levels = 5;
const labels = ['性能', '可维护性', '扩展性', '安全性', '成本', '学习曲线'];

const series = [
  { name: 'A', values: [90, 70, 95, 85, 50, 45], color: 'rgba(102,126,234,0.8)', fill: 'rgba(102,126,234,0.12)' },
  { name: 'B', values: [75, 85, 80, 70, 90, 60], color: 'rgba(245,87,108,0.8)', fill: 'rgba(245,87,108,0.12)' },
  { name: 'C', values: [65, 90, 55, 80, 85, 90], color: 'rgba(67,233,123,0.8)', fill: 'rgba(67,233,123,0.12)' }
];
'''

# L3: 8 axes, 3 series
L3_series = [
    {'color': 'rgba(102,126,234,0.7)', 'legend': 'React'},
    {'color': 'rgba(245,87,108,0.7)', 'legend': 'Vue'},
    {'color': 'rgba(67,233,123,0.7)', 'legend': 'Angular'}
]
L3_data = '''const svg = document.getElementById('radar');

const cx = 500, cy = 310, R = 220;
const axes = 8;
const levels = 5;
const labels = ['性能', '生态系统', '学习曲线', '社区活跃度', '企业采用', '文档质量', 'TypeScript 支持', '移动端'];

const series = [
  { name: 'React', values: [88, 95, 65, 98, 92, 80, 90, 75], color: 'rgba(102,126,234,0.8)', fill: 'rgba(102,126,234,0.12)' },
  { name: 'Vue', values: [85, 82, 90, 88, 78, 92, 85, 70], color: 'rgba(245,87,108,0.8)', fill: 'rgba(245,87,108,0.12)' },
  { name: 'Angular', values: [80, 78, 45, 75, 88, 85, 98, 82], color: 'rgba(67,233,123,0.8)', fill: 'rgba(67,233,123,0.12)' }
];
'''

# L4: 10 axes, 4 series
L4_series = [
    {'color': 'rgba(102,126,234,0.7)', 'legend': 'PostgreSQL'},
    {'color': 'rgba(245,87,108,0.7)', 'legend': 'MySQL'},
    {'color': 'rgba(67,233,123,0.7)', 'legend': 'MongoDB'},
    {'color': 'rgba(250,130,49,0.7)', 'legend': 'Redis'}
]
L4_data = '''const svg = document.getElementById('radar');

const cx = 500, cy = 310, R = 220;
const axes = 10;
const levels = 5;
const labels = ['读性能', '写性能', '事务支持', '水平扩展', '运维成本', '数据一致性', '查询灵活性', '生态工具', '学习成本', '社区支持'];

const series = [
  { name: 'PostgreSQL', values: [85, 80, 98, 60, 70, 98, 95, 88, 55, 90], color: 'rgba(102,126,234,0.8)', fill: 'rgba(102,126,234,0.12)' },
  { name: 'MySQL', values: [88, 82, 90, 55, 80, 90, 80, 92, 75, 95], color: 'rgba(245,87,108,0.8)', fill: 'rgba(245,87,108,0.12)' },
  { name: 'MongoDB', values: [90, 92, 45, 95, 65, 50, 70, 78, 80, 85], color: 'rgba(67,233,123,0.8)', fill: 'rgba(67,233,123,0.12)' },
  { name: 'Redis', values: [99, 98, 30, 80, 60, 40, 35, 72, 85, 88], color: 'rgba(250,130,49,0.8)', fill: 'rgba(250,130,49,0.12)' }
];
'''

test_data = {
    'L1': (L1_series, L1_data),
    'L2': (L2_series, L2_data),
    'L3': (L3_series, L3_data),
    'L4': (L4_series, L4_data)
}

for level, (series_list, data_js) in test_data.items():
    legend_html = make_legend_html(series_list)
    content = make_html(legend_html, data_js)
    filename = f'radar-{level}.html'
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
