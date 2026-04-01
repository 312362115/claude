"""生成 treemap L1-L4 测试 HTML 文件"""
import re
import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / 'docs' / 'assets' / 'diagram' / 'tests' / 'html'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not os.path.exists('lib'):
    os.symlink('../templates/html/lib', 'lib')

with open('../templates/html/treemap.html', 'r') as f:
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
  body { font-family: -apple-system, system-ui, 'PingFang SC', sans-serif; background: #fff; padding: 24px; display: inline-block; }
  .title { font-size: 22px; font-weight: 700; color: #1a1a2e; margin-bottom: 6px; }
  .subtitle { font-size: 14px; color: #888; margin-bottom: 16px; }
</style>
<script src="lib/utils.js"></script>
</head>
<body>
<div class="title" id="title"></div>
<div class="subtitle" id="subtitle"></div>
<svg id="canvas"></svg>
<script>
(function() {
  var svg = document.getElementById('canvas');
  var SANS = "-apple-system, system-ui, 'PingFang SC', sans-serif";

'''

tail = '</script>\n</body>\n</html>\n'

L1 = '''
  document.getElementById('title').textContent = '磁盘使用';
  document.getElementById('subtitle').textContent = 'L1 简单 · 4 叶节点';
  var data = { name: 'Root', children: [
    { name: 'Documents', value: 120 },
    { name: 'Photos', value: 80 },
    { name: 'Music', value: 50 },
    { name: 'Videos', value: 30 }
  ]};
'''

L2 = '''
  document.getElementById('title').textContent = '市场份额分布';
  document.getElementById('subtitle').textContent = 'L2 中等 · 2 层 · 10 叶节点';
  var data = { name: 'Root', children: [
    { name: '搜索引擎', children: [
      { name: 'Google', value: 250 },
      { name: 'Bing', value: 60 },
      { name: '百度', value: 40 }
    ]},
    { name: '社交媒体', children: [
      { name: '微信', value: 120 },
      { name: '抖音', value: 100 },
      { name: '微博', value: 60 }
    ]},
    { name: '电商平台', children: [
      { name: '淘宝', value: 90 },
      { name: '京东', value: 70 },
      { name: '拼多多', value: 40 }
    ]},
    { name: '视频流媒体', value: 150 }
  ]};
'''

L3 = '''
  document.getElementById('title').textContent = '技术栈占比';
  document.getElementById('subtitle').textContent = 'L3 复杂 · 3 层 · 15 叶节点';
  var data = { name: 'Root', children: [
    { name: 'Frontend', children: [
      { name: 'React', value: 300 },
      { name: 'Vue', value: 200 },
      { name: 'Angular', value: 100 },
      { name: 'Svelte', value: 50 }
    ]},
    { name: 'Backend', children: [
      { name: 'Node.js', value: 250 },
      { name: 'Python', children: [
        { name: 'Django', value: 80 },
        { name: 'Flask', value: 60 },
        { name: 'FastAPI', value: 40 }
      ]},
      { name: 'Go', value: 120 },
      { name: 'Java', value: 180 }
    ]},
    { name: 'DevOps', children: [
      { name: 'Docker', value: 100 },
      { name: 'K8s', value: 80 }
    ]}
  ]};
'''

L4 = '''
  document.getElementById('title').textContent = '全球 IT 支出';
  document.getElementById('subtitle').textContent = 'L4 超级复杂 · 3 层 · 20+ 叶节点';
  var data = { name: 'Root', children: [
    { name: '北美', children: [
      { name: 'Cloud', value: 400 },
      { name: 'Security', value: 200 },
      { name: 'AI/ML', value: 300 },
      { name: 'Infra', value: 150 }
    ]},
    { name: '欧洲', children: [
      { name: 'Cloud', value: 250 },
      { name: 'Security', value: 180 },
      { name: 'IoT', value: 100 },
      { name: 'Data', children: [
        { name: 'Analytics', value: 80 },
        { name: 'Storage', value: 60 },
        { name: 'ETL', value: 40 }
      ]}
    ]},
    { name: '亚太', children: [
      { name: 'Mobile', value: 350 },
      { name: 'E-commerce', value: 280 },
      { name: 'FinTech', children: [
        { name: 'Payment', value: 120 },
        { name: 'Lending', value: 80 },
        { name: 'InsurTech', value: 50 }
      ]}
    ]},
    { name: '其他', children: [
      { name: 'LATAM', value: 80 },
      { name: 'MEA', value: 60 },
      { name: 'Africa', value: 30 }
    ]}
  ]};
'''

test_data = {'L1': L1, 'L2': L2, 'L3': L3, 'L4': L4}

for level, data in test_data.items():
    content = header + data + '\n' + engine + tail
    filename = f'treemap-{level}.html'
    with open(str(OUTPUT_DIR / filename), 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
