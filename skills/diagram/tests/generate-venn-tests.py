"""生成 venn L1-L4 测试 HTML 文件"""
import re
import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / 'docs' / 'assets' / 'diagram' / 'tests' / 'html'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 读取模板
with open('../templates/html/venn.html', 'r') as f:
    template = f.read()

# 提取引擎部分（数据结束标记之后到 </script>）
engine_match = re.search(r'(// ===== 数据结束 =====\n.*)</script>', template, re.DOTALL)
engine = engine_match.group(1)

# 提取 HTML 头部（从开始到 <script> 标签后）
head_match = re.search(r'(.*<script>\n)', template, re.DOTALL)
html_head = head_match.group(1)

# L1: 2 circles, 2 items each
L1 = '''// ===== 数据 =====
var circles = [
  { label: '设计', items: ['Figma', 'Sketch'], color: 0 },
  { label: '开发', items: ['React', 'TypeScript'], color: 1 }
];
var intersection = ['Design System'];
'''

# L2: current default data (3 circles)
L2 = '''// ===== 数据 =====
var circles = [
  { label: '前端', items: ['React', 'Vue', 'CSS'], color: 0 },
  { label: '后端', items: ['Node.js', 'Go', 'SQL'], color: 1 },
  { label: '运维', items: ['Docker', 'K8s', 'CI/CD'], color: 2 }
];
var intersection = ['全栈工程师'];
'''

# L3: 3 circles, 5 items each
L3 = '''// ===== 数据 =====
var circles = [
  { label: '产品', items: ['需求分析', '用户研究', '原型设计', '数据分析', 'A/B 测试'], color: 0 },
  { label: '设计', items: ['视觉设计', '交互设计', '动效设计', '设计系统', '品牌规范'], color: 3 },
  { label: '研发', items: ['前端开发', '后端开发', '性能优化', '代码审查', '自动化测试'], color: 2 }
];
var intersection = ['用户体验', '敏捷协作'];
'''

# L4: 4 circles (venn template supports n circles via angle calculation)
L4 = '''// ===== 数据 =====
var circles = [
  { label: '商业', items: ['商业模式', '收入增长', '市场定位', '竞争策略', '融资规划'], color: 0 },
  { label: '产品', items: ['用户需求', '功能规划', '产品路线图', '数据驱动', '体验优化'], color: 1 },
  { label: '技术', items: ['架构设计', '技术选型', '性能调优', '安全防护', '运维保障'], color: 4 },
  { label: '运营', items: ['用户增长', '内容运营', '活动策划', '社群管理', '品牌传播'], color: 3 }
];
var intersection = ['创业核心能力'];
'''

test_data = {
    'L1': L1,
    'L2': L2,
    'L3': L3,
    'L4': L4
}

for level, data in test_data.items():
    content = html_head + data + engine + '</script>\n</body>\n</html>\n'
    filename = f'venn-{level}.html'
    with open(str(OUTPUT_DIR / filename), 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
