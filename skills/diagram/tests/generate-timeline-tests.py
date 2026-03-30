"""生成 timeline L1-L4 测试 HTML 文件"""

# 读取模板
with open('../templates/html/timeline.html', 'r') as f:
    template = f.read()

# head = 从开头到 <script src="lib/utils.js"></script>\n<script> (含)
marker = '<script src="lib/utils.js"></script>\n<script>'
head = template[:template.index(marker) + len(marker)]

tail = '</script>\n</body>\n</html>\n'

# 提取渲染引擎：从 "// 布局：纵向中轴线" 开始到 script 结尾之前
engine_start = '// 布局：纵向中轴线'
engine_end = '</script>'
engine_idx = template.index(engine_start)
engine_end_idx = template.index(engine_end, engine_idx)
engine = template[engine_idx:engine_end_idx]

# L1: 2 sections, 2-3 events each
L1_data = '''
const svg = document.getElementById('tl');

const colors = ['#667eea', '#f5576c'];

const sections = [
  { name: '创业初期', years: '2020–2021',
    events: ['公司注册', '产品原型', '种子轮融资'] },
  { name: '快速增长', years: '2022–2023',
    events: ['用户破万', 'A 轮融资'] }
];

'''

# L2: 默认模板数据 (5 sections)
L2_data = '''
const svg = document.getElementById('tl');

const colors = ['#667eea', '#f5576c', '#43e97b', '#4facfe', '#fa8231'];

const sections = [
  { name: '静态页面时代', years: '1995–1999',
    events: ['JavaScript 诞生', 'HTML 2.0', 'CSS 1.0', '浏览器大战', 'XMLHttpRequest'] },
  { name: 'Web 2.0 时代', years: '2004–2009',
    events: ['Gmail · AJAX 流行', 'jQuery 革命', 'Chrome · V8 引擎', 'Node.js 诞生'] },
  { name: '前端工程化时代', years: '2010–2014',
    events: ['AngularJS · npm', 'TypeScript · Webpack', 'React 开源', 'Vue.js · HTML5'] },
  { name: '现代前端时代', years: '2015–2019',
    events: ['ES6 标准发布', 'React Native · GraphQL', 'Vue 2 · Angular 2', 'React Hooks · Svelte'] },
  { name: '新一代工具链', years: '2020–2024',
    events: ['Vue 3 · Vite', 'Next.js · RSC', 'Bun · Turbopack', 'AI 辅助编程 · React 19'] }
];

'''

# L3: 6 sections, 6 events each
L3_data = '''
const svg = document.getElementById('tl');

const colors = ['#667eea', '#f5576c', '#43e97b', '#4facfe', '#fa8231', '#a55eea'];

const sections = [
  { name: '萌芽期', years: '1990–1995',
    events: ['HTML 1.0 草案', 'Mosaic 浏览器', 'HTTP 1.0', 'CGI 网关', 'Perl 动态页面', 'Apache 服务器'] },
  { name: '门户时代', years: '1996–2000',
    events: ['JavaScript 1.0', 'CSS 1.0 规范', 'Flash 插件', 'IE 4 发布', 'Yahoo 上市', 'dotcom 泡沫'] },
  { name: 'Web 2.0', years: '2001–2006',
    events: ['AJAX 出现', 'RSS 订阅', 'Wikipedia 上线', 'Ruby on Rails', 'jQuery 发布', 'Google Maps'] },
  { name: '移动互联网', years: '2007–2012',
    events: ['iPhone 发布', 'Android 问世', 'App Store 上线', 'HTML5 草案', 'Node.js 诞生', '响应式设计'] },
  { name: '云原生时代', years: '2013–2018',
    events: ['Docker 容器', 'Kubernetes 开源', 'React/Vue 崛起', 'Serverless', 'GraphQL', 'PWA 标准'] },
  { name: 'AI 时代', years: '2019–2024',
    events: ['GPT-2 发布', 'GitHub Copilot', 'ChatGPT 爆发', 'AI Agent', 'Rust 生态', 'WebAssembly'] }
];

'''

# L4: 8 sections, 7+ events each
L4_data = '''
const svg = document.getElementById('tl');

const colors = ['#667eea', '#f5576c', '#43e97b', '#4facfe', '#fa8231', '#a55eea', '#00b894', '#e17055'];

const sections = [
  { name: '古典计算', years: '1940–1959',
    events: ['ENIAC 诞生', '冯诺依曼架构', '晶体管发明', 'FORTRAN 语言', 'LISP 语言', '集成电路', 'COBOL 发布'] },
  { name: '大型机时代', years: '1960–1969',
    events: ['IBM System/360', 'ARPANET 诞生', 'UNIX 系统', '鼠标发明', '结构化编程', 'ASCII 标准', '阿波罗导航计算机'] },
  { name: '微机革命', years: '1970–1979',
    events: ['Intel 4004', 'C 语言', 'Ethernet 发明', 'Apple II', 'TCP/IP 协议', 'SQL 标准', 'VisiCalc 电子表格'] },
  { name: 'PC 普及', years: '1980–1989',
    events: ['IBM PC', 'Macintosh', 'Windows 1.0', 'C++ 语言', 'GNU 项目', 'Perl 语言', 'World Wide Web'] },
  { name: '互联网兴起', years: '1990–1995',
    events: ['Linux 诞生', 'Python 发布', 'Mosaic 浏览器', 'Java 语言', 'JavaScript 诞生', 'Amazon 上线', 'PHP 发布'] },
  { name: 'Web 时代', years: '1996–2005',
    events: ['CSS 标准', 'Google 创立', '.NET 框架', 'AJAX 革命', 'Ruby on Rails', 'Firefox 浏览器', 'Git 诞生'] },
  { name: '移动时代', years: '2006–2015',
    events: ['iPhone 发布', 'Android 系统', 'Node.js 诞生', 'Docker 容器', 'React 开源', 'Swift 语言', 'Kubernetes'] },
  { name: 'AI 与云', years: '2016–2024',
    events: ['AlphaGo', 'TensorFlow 2', 'GPT-3 发布', 'GitHub Copilot', 'ChatGPT 爆发', 'Rust 崛起', 'AI Agent 时代'] }
];

'''

# 渲染引擎模板（参数化 sectionH / eventGap）
def make_engine(sectionH=140, eventGap=28):
    return f'''// 布局：纵向中轴线
const CX = 600;          // 中轴 x
const startY = 30;       // 起始 y
const sectionH = {sectionH};    // 每个时代段高度
const eventGap = {eventGap};     // 事件行间距
const eventOffsetX = 200; // 事件卡片到中轴的水平距离
const dotR = 5;

// 中轴线
svg.appendChild(el('line', {{
  x1: CX, y1: startY, x2: CX, y2: startY + sections.length * sectionH,
  stroke: '#e2e8f0', 'stroke-width': 2
}}));

sections.forEach((sec, si) => {{
  const color = colors[si];
  const baseY = startY + si * sectionH;

  // 第一个事件的 y 基准
  const firstEventY = baseY + 6;

  // 时代节点圆点（大）— 与第一个事件卡片中心对齐
  svg.appendChild(el('circle', {{
    cx: CX, cy: firstEventY + 11, r: 10,
    fill: color
  }}));

  // 时代名称（左侧）— 顶部与第一个事件卡片顶部对齐
  const nameEl = el('text', {{
    x: CX - 24, y: firstEventY + 2,
    'text-anchor': 'end', 'dominant-baseline': 'hanging',
    'font-size': 16, 'font-weight': 700, fill: color
  }});
  nameEl.textContent = sec.name;
  svg.appendChild(nameEl);

  // 年份（左侧，名称下方）
  const yearEl = el('text', {{
    x: CX - 24, y: firstEventY + 20,
    'text-anchor': 'end', 'dominant-baseline': 'hanging',
    'font-size': 12, fill: '#94a3b8'
  }});
  yearEl.textContent = sec.years;
  svg.appendChild(yearEl);

  // 事件卡片（右侧，竖向排列）
  sec.events.forEach((evt, ei) => {{
    const ey = firstEventY + ei * eventGap;
    const ex = CX + 24;

    // 横线连接到中轴
    svg.appendChild(el('line', {{
      x1: CX + 10, y1: ey + 10, x2: ex - 2, y2: ey + 10,
      stroke: color, 'stroke-width': 1, opacity: 0.3
    }}));

    // 小圆点
    svg.appendChild(el('circle', {{
      cx: CX, cy: ey + 10, r: 3.5,
      fill: '#fff', stroke: color, 'stroke-width': 1.5
    }}));

    // 事件卡片背景
    const tw = evt.length * 12 + 20;
    svg.appendChild(el('rect', {{
      x: ex, y: ey, width: tw, height: 22,
      rx: 4, fill: color, opacity: 0.08
    }}));

    // 左边色条
    svg.appendChild(el('rect', {{
      x: ex, y: ey, width: 3, height: 22,
      rx: 1.5, fill: color, opacity: 0.6
    }}));

    // 事件文字
    const textEl = el('text', {{
      x: ex + 10, y: ey + 15,
      'font-size': 12, fill: '#334155'
    }});
    textEl.textContent = evt;
    svg.appendChild(textEl);
  }});
}});
'''

# 各级别使用不同的 SVG 高度和引擎参数
level_config = {
    'L1': {'svgH': 740, 'sectionH': 140, 'eventGap': 28},
    'L2': {'svgH': 740, 'sectionH': 140, 'eventGap': 28},
    'L3': {'svgH': 780, 'sectionH': 120, 'eventGap': 22},
    'L4': {'svgH': 780, 'sectionH': 90,  'eventGap': 16},
}

level_data = {
    'L1': L1_data,
    'L2': L2_data,
    'L3': L3_data,
    'L4': L4_data,
}

for level, cfg in level_config.items():
    svgH = cfg['svgH']
    # 替换 head 中的 SVG 高度（height 属性和 viewBox）以及 viewport meta
    level_head = head.replace(
        'height="740" viewBox="0 0 1200 740"',
        f'height="{svgH}" viewBox="0 0 1200 {svgH}"'
    ).replace(
        'height=800',
        f'height={svgH + 60}'
    )
    engine = make_engine(cfg['sectionH'], cfg['eventGap'])
    script = level_data[level] + engine
    content = level_head + '\n' + script + '\n' + tail
    filename = f'timeline-{level}.html'
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Generated {filename} (svgH={svgH}, sectionH={cfg["sectionH"]}, eventGap={cfg["eventGap"]})')
