"""生成 pie L1-L4 测试 HTML 文件"""
import re

# 读取模板
with open('../templates/html/pie.html', 'r') as f:
    template = f.read()

# 提取 HTML 头部（从开始到 <script src="lib/utils.js"></script>\n<script>\n）
head_match = re.search(r'(.*<script src="lib/utils\.js"></script>\n<script>\n)', template, re.DOTALL)
html_head = head_match.group(1)

# 提取引擎部分（从 // 布局参数 到文件末尾）
engine_match = re.search(r'(// 布局参数\n.*)</script>\n</body>\n</html>', template, re.DOTALL)
engine = engine_match.group(1)

tail = '</script>\n</body>\n</html>\n'

# L1: 3 items（最简）
L1 = '''// 数据 & 配色
const data = [
  { value: 3200, name: 'React' },
  { value: 2800, name: 'Vue' },
  { value: 1500, name: 'Angular' }
];
const colors = [
  'rgba(102,126,234,0.75)', 'rgba(245,87,108,0.75)', 'rgba(79,172,254,0.75)'
];
const total = data.reduce((s, d) => s + d.value, 0);

'''

# L2: 默认模板 8 items
L2 = '''// 数据 & 配色
const data = [
  { value: 3200, name: 'React' },
  { value: 2800, name: 'Vue' },
  { value: 1500, name: 'Angular' },
  { value: 1200, name: 'Next.js' },
  { value: 800,  name: 'Svelte' },
  { value: 600,  name: 'Nuxt' },
  { value: 450,  name: 'Solid' },
  { value: 350,  name: 'Astro' }
];
const colors = [
  'rgba(102,126,234,0.75)', 'rgba(245,87,108,0.75)', 'rgba(79,172,254,0.75)',
  'rgba(67,233,123,0.75)',  'rgba(250,130,49,0.75)',  'rgba(165,94,234,0.75)',
  'rgba(252,92,101,0.75)',  'rgba(38,222,129,0.75)'
];
const total = data.reduce((s, d) => s + d.value, 0);

'''

# L3: 10 items，大小差异明显
L3 = '''// 数据 & 配色
const data = [
  { value: 5200, name: 'JavaScript' },
  { value: 4800, name: 'Python' },
  { value: 3600, name: 'TypeScript' },
  { value: 2400, name: 'Java' },
  { value: 1800, name: 'C#' },
  { value: 1200, name: 'Go' },
  { value: 900,  name: 'Rust' },
  { value: 600,  name: 'PHP' },
  { value: 400,  name: 'Swift' },
  { value: 250,  name: 'Kotlin' }
];
const colors = [
  'rgba(102,126,234,0.75)', 'rgba(245,87,108,0.75)', 'rgba(79,172,254,0.75)',
  'rgba(67,233,123,0.75)',  'rgba(250,130,49,0.75)',  'rgba(165,94,234,0.75)',
  'rgba(252,92,101,0.75)',  'rgba(38,222,129,0.75)',  'rgba(255,165,2,0.75)',
  'rgba(46,213,115,0.75)'
];
const total = data.reduce((s, d) => s + d.value, 0);

'''

# L4: 14 items，含长名称，测试标签防碰撞
L4 = '''// 数据 & 配色
const data = [
  { value: 8500, name: 'Visual Studio Code' },
  { value: 6200, name: 'IntelliJ IDEA' },
  { value: 4800, name: 'Sublime Text' },
  { value: 3600, name: 'Vim/Neovim' },
  { value: 2900, name: 'WebStorm' },
  { value: 2200, name: 'PyCharm Professional' },
  { value: 1800, name: 'Xcode' },
  { value: 1400, name: 'Android Studio' },
  { value: 1000, name: 'Eclipse IDE' },
  { value: 750,  name: 'Atom (已归档)' },
  { value: 500,  name: 'Emacs' },
  { value: 350,  name: 'Notepad++' },
  { value: 200,  name: 'Fleet (JetBrains)' },
  { value: 120,  name: 'Zed Editor' }
];
const colors = [
  'rgba(102,126,234,0.75)', 'rgba(245,87,108,0.75)', 'rgba(79,172,254,0.75)',
  'rgba(67,233,123,0.75)',  'rgba(250,130,49,0.75)',  'rgba(165,94,234,0.75)',
  'rgba(252,92,101,0.75)',  'rgba(38,222,129,0.75)',  'rgba(255,165,2,0.75)',
  'rgba(46,213,115,0.75)',  'rgba(116,185,255,0.75)', 'rgba(223,228,234,0.75)',
  'rgba(255,107,129,0.75)', 'rgba(55,66,250,0.75)'
];
const total = data.reduce((s, d) => s + d.value, 0);

'''

test_data = {'L1': L1, 'L2': L2, 'L3': L3, 'L4': L4}

for level, data in test_data.items():
    content = html_head + data + engine + tail
    filename = f'pie-{level}.html'
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
