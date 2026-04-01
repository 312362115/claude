"""生成 sankey L1-L4 测试 HTML 文件"""

from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / "docs" / "assets" / "diagram" / "tests" / "html"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 读取模板
with open('../templates/html/sankey.html', 'r') as f:
    template = f.read()

# head = 从开头到 <script src="lib/utils.js"></script>\n<script> (含)
marker = '<script src="lib/utils.js"></script>\n<script>'
head = template[:template.index(marker) + len(marker)]

tail = '</script>\n</body>\n</html>\n'

# 渲染引擎：从 "// 布局参数" 到 script 结尾之前
# 提取引擎代码（布局参数 → 画节点，不含数据定义）
engine_start = '// 布局参数'
engine_end = '</script>'
engine_idx = template.index(engine_start)
engine_end_idx = template.index(engine_end, engine_idx)
engine = template[engine_idx:engine_end_idx]

# L1: 4 节点, 3 链接, 简单线性 A→B→C→D
L1_data = '''
const svg = document.getElementById('sk');

// 节点定义：name, layer, color
const nodesDef = [
  { name: '入口',   layer: 0, color: '#667eea' },
  { name: '浏览',   layer: 1, color: '#4facfe' },
  { name: '下单',   layer: 2, color: '#43e97b' },
  { name: '完成',   layer: 3, color: '#20bf6b' }
];

const linksDef = [
  { source: '入口', target: '浏览', value: 1000 },
  { source: '浏览', target: '下单', value: 600 },
  { source: '下单', target: '完成', value: 400 }
];

'''

L1_engine = '''// 布局参数
const padL = 60, padR = 60, padT = 20, padB = 30;
const chartW = 1120 - padL - padR;
const chartH = 660 - padT - padB;
const nodeW = 22;
const nodeGap = 14;
const maxLayers = 4;
const colW = chartW / (maxLayers - 1);
'''

# L2: 默认模板数据 (10 节点, 18 链接)
L2_data = '''
const svg = document.getElementById('sk');

// 节点定义：name, layer, color
const nodesDef = [
  { name: '首页',     layer: 0, color: '#667eea' },
  { name: '搜索',     layer: 0, color: '#764ba2' },
  { name: '推荐',     layer: 0, color: '#f093fb' },
  { name: '广告',     layer: 0, color: '#f5576c' },
  { name: '商品详情',  layer: 1, color: '#4facfe' },
  { name: '加入购物车', layer: 2, color: '#43e97b' },
  { name: '收藏',     layer: 2, color: '#fa8231' },
  { name: '下单',     layer: 3, color: '#26de81' },
  { name: '流失',     layer: 3, color: '#a5b1c2' },
  { name: '支付成功',  layer: 4, color: '#20bf6b' }
];

const linksDef = [
  { source: '首页', target: '商品详情', value: 3200 },
  { source: '首页', target: '加入购物车', value: 800 },
  { source: '首页', target: '收藏', value: 500 },
  { source: '搜索', target: '商品详情', value: 2800 },
  { source: '搜索', target: '加入购物车', value: 600 },
  { source: '推荐', target: '商品详情', value: 1800 },
  { source: '推荐', target: '收藏', value: 400 },
  { source: '广告', target: '商品详情', value: 1200 },
  { source: '广告', target: '加入购物车', value: 300 },
  { source: '商品详情', target: '加入购物车', value: 3500 },
  { source: '商品详情', target: '收藏', value: 1200 },
  { source: '商品详情', target: '流失', value: 4300 },
  { source: '加入购物车', target: '下单', value: 3200 },
  { source: '加入购物车', target: '流失', value: 2000 },
  { source: '收藏', target: '下单', value: 600 },
  { source: '收藏', target: '流失', value: 1500 },
  { source: '下单', target: '支付成功', value: 2800 },
  { source: '下单', target: '流失', value: 1000 }
];

'''

# L3: 12 节点, 22 链接
L3_data = '''
const svg = document.getElementById('sk');

// 节点定义：name, layer, color
const nodesDef = [
  { name: '直接访问',   layer: 0, color: '#667eea' },
  { name: '搜索引擎',   layer: 0, color: '#764ba2' },
  { name: '社交媒体',   layer: 0, color: '#f093fb' },
  { name: '邮件营销',   layer: 0, color: '#f5576c' },
  { name: '落地页',     layer: 1, color: '#4facfe' },
  { name: '产品页',     layer: 1, color: '#00b894' },
  { name: '注册',       layer: 2, color: '#43e97b' },
  { name: '试用',       layer: 2, color: '#fa8231' },
  { name: '跳出',       layer: 2, color: '#a5b1c2' },
  { name: '付费',       layer: 3, color: '#26de81' },
  { name: '流失',       layer: 3, color: '#dfe6e9' },
  { name: '续费',       layer: 4, color: '#20bf6b' }
];

const linksDef = [
  { source: '直接访问', target: '落地页', value: 2000 },
  { source: '直接访问', target: '产品页', value: 1500 },
  { source: '搜索引擎', target: '落地页', value: 3500 },
  { source: '搜索引擎', target: '产品页', value: 2200 },
  { source: '社交媒体', target: '落地页', value: 1800 },
  { source: '社交媒体', target: '产品页', value: 800 },
  { source: '邮件营销', target: '落地页', value: 1200 },
  { source: '邮件营销', target: '产品页', value: 600 },
  { source: '落地页', target: '注册', value: 4200 },
  { source: '落地页', target: '试用', value: 2000 },
  { source: '落地页', target: '跳出', value: 2300 },
  { source: '产品页', target: '注册', value: 2800 },
  { source: '产品页', target: '试用', value: 1500 },
  { source: '产品页', target: '跳出', value: 800 },
  { source: '注册', target: '付费', value: 3800 },
  { source: '注册', target: '流失', value: 3200 },
  { source: '试用', target: '付费', value: 2200 },
  { source: '试用', target: '流失', value: 1300 },
  { source: '跳出', target: '流失', value: 3100 },
  { source: '付费', target: '续费', value: 4000 },
  { source: '付费', target: '流失', value: 2000 },
  { source: '流失', target: '续费', value: 200 }
];

'''

L3_engine = '''// 布局参数
const padL = 60, padR = 60, padT = 20, padB = 30;
const chartW = 1120 - padL - padR;
const chartH = 660 - padT - padB;
const nodeW = 22;
const nodeGap = 14;
const maxLayers = 5;
const colW = chartW / (maxLayers - 1);
'''

# L4: 16 节点 across 5 layers, 26 链接
L4_data = '''
const svg = document.getElementById('sk');

// 节点定义：name, layer, color
const nodesDef = [
  { name: '自然搜索',   layer: 0, color: '#667eea' },
  { name: '付费搜索',   layer: 0, color: '#764ba2' },
  { name: '社交广告',   layer: 0, color: '#f093fb' },
  { name: '内容营销',   layer: 0, color: '#f5576c' },
  { name: '合作推荐',   layer: 0, color: '#00cec9' },
  { name: '首页',       layer: 1, color: '#4facfe' },
  { name: '专题页',     layer: 1, color: '#00b894' },
  { name: '博客',       layer: 1, color: '#fdcb6e' },
  { name: '免费注册',   layer: 2, color: '#43e97b' },
  { name: '演示预约',   layer: 2, color: '#fa8231' },
  { name: '跳出',       layer: 2, color: '#a5b1c2' },
  { name: '试用激活',   layer: 3, color: '#26de81' },
  { name: '销售跟进',   layer: 3, color: '#0984e3' },
  { name: '流失',       layer: 3, color: '#dfe6e9' },
  { name: '成交',       layer: 4, color: '#20bf6b' },
  { name: '未转化',     layer: 4, color: '#b2bec3' }
];

const linksDef = [
  { source: '自然搜索', target: '首页', value: 3000 },
  { source: '自然搜索', target: '博客', value: 2200 },
  { source: '付费搜索', target: '专题页', value: 2800 },
  { source: '付费搜索', target: '首页', value: 1200 },
  { source: '社交广告', target: '专题页', value: 1600 },
  { source: '社交广告', target: '首页', value: 800 },
  { source: '内容营销', target: '博客', value: 2000 },
  { source: '内容营销', target: '首页', value: 500 },
  { source: '合作推荐', target: '专题页', value: 1400 },
  { source: '合作推荐', target: '首页', value: 600 },
  { source: '首页', target: '免费注册', value: 3200 },
  { source: '首页', target: '跳出', value: 2900 },
  { source: '专题页', target: '演示预约', value: 3000 },
  { source: '专题页', target: '免费注册', value: 1800 },
  { source: '专题页', target: '跳出', value: 1000 },
  { source: '博客', target: '免费注册', value: 2400 },
  { source: '博客', target: '跳出', value: 1800 },
  { source: '免费注册', target: '试用激活', value: 4800 },
  { source: '免费注册', target: '流失', value: 2600 },
  { source: '演示预约', target: '销售跟进', value: 2400 },
  { source: '演示预约', target: '流失', value: 600 },
  { source: '跳出', target: '流失', value: 5700 },
  { source: '试用激活', target: '成交', value: 3200 },
  { source: '试用激活', target: '未转化', value: 1600 },
  { source: '销售跟进', target: '成交', value: 1800 },
  { source: '销售跟进', target: '未转化', value: 600 }
];

'''

# 公共引擎部分（从 "计算节点值" 到结尾），所有级别共用
common_engine_tail = '''
// 计算节点值 = max(inflow, outflow)
const nodeMap = {};
nodesDef.forEach(n => { nodeMap[n.name] = { ...n, inVal: 0, outVal: 0 }; });
linksDef.forEach(l => {
  nodeMap[l.source].outVal += l.value;
  nodeMap[l.target].inVal += l.value;
});
Object.values(nodeMap).forEach(n => { n.val = Math.max(n.inVal, n.outVal); });

// 按层分组
const layers = Array.from({ length: maxLayers }, () => []);
Object.values(nodeMap).forEach(n => layers[n.layer].push(n));

// 每层按值降序
layers.forEach(l => l.sort((a, b) => b.val - a.val));

// 缩放因子：找最"密"的层
const totalPerLayer = layers.map(l => l.reduce((s, n) => s + n.val, 0) + (l.length - 1) * nodeGap);
const maxTotal = Math.max(...totalPerLayer.map((t, i) => {
  const l = layers[i];
  return l.reduce((s, n) => s + n.val, 0) + (l.length - 1) * nodeGap;
}));
// 用最密层的总值来算 scale
const valOnlyMax = Math.max(...layers.map(l => l.reduce((s, n) => s + n.val, 0)));
const gapTotal = Math.max(...layers.map(l => (l.length - 1) * nodeGap));
const scale = (chartH - gapTotal) / valOnlyMax;

// 计算节点 y 位置
layers.forEach((layer, li) => {
  const totalH = layer.reduce((s, n) => s + n.val * scale, 0) + (layer.length - 1) * nodeGap;
  let y = padT + (chartH - totalH) / 2;
  layer.forEach(n => {
    n.x = padL + li * colW - nodeW / 2;
    n.y = y;
    n.h = n.val * scale;
    y += n.h + nodeGap;
    // 追踪出/入端口偏移
    n.srcOffset = 0;
    n.tgtOffset = 0;
  });
});

// 先画链接（在节点下方）
const defs = document.createElementNS(svgNS, 'defs');
svg.appendChild(defs);

linksDef.forEach((l, i) => {
  const src = nodeMap[l.source];
  const tgt = nodeMap[l.target];
  const h = l.value * scale;

  const x0 = src.x + nodeW;
  const y0 = src.y + src.srcOffset;
  const x1 = tgt.x;
  const y1 = tgt.y + tgt.tgtOffset;
  const cpx = (x0 + x1) / 2;

  // 渐变
  const gradId = `sg${i}`;
  const grad = document.createElementNS(svgNS, 'linearGradient');
  grad.setAttribute('id', gradId);
  grad.setAttribute('gradientUnits', 'userSpaceOnUse');
  grad.setAttribute('x1', x0); grad.setAttribute('y1', '0');
  grad.setAttribute('x2', x1); grad.setAttribute('y2', '0');
  const s1 = document.createElementNS(svgNS, 'stop');
  s1.setAttribute('offset', '0%'); s1.setAttribute('stop-color', src.color); s1.setAttribute('stop-opacity', '0.35');
  const s2 = document.createElementNS(svgNS, 'stop');
  s2.setAttribute('offset', '100%'); s2.setAttribute('stop-color', tgt.color); s2.setAttribute('stop-opacity', '0.35');
  grad.appendChild(s1); grad.appendChild(s2);
  defs.appendChild(grad);

  // 流带路径
  const path = document.createElementNS(svgNS, 'path');
  path.setAttribute('d', [
    `M ${x0},${y0}`,
    `C ${cpx},${y0} ${cpx},${y1} ${x1},${y1}`,
    `L ${x1},${y1 + h}`,
    `C ${cpx},${y1 + h} ${cpx},${y0 + h} ${x0},${y0 + h}`,
    'Z'
  ].join(' '));
  path.setAttribute('fill', `url(#${gradId})`);
  svg.appendChild(path);

  src.srcOffset += h;
  tgt.tgtOffset += h;
});

// 画节点
Object.values(nodeMap).forEach(n => {
  const rect = document.createElementNS(svgNS, 'rect');
  rect.setAttribute('x', n.x); rect.setAttribute('y', n.y);
  rect.setAttribute('width', nodeW); rect.setAttribute('height', n.h);
  rect.setAttribute('rx', '4');
  rect.setAttribute('fill', n.color);
  svg.appendChild(rect);

  // 标签
  const txt = document.createElementNS(svgNS, 'text');
  const isLast = n.layer === maxLayers - 1;
  const isSecondLast = n.layer === maxLayers - 2;
  // 右侧两层标签放左边，其余放右边
  if (isLast || isSecondLast) {
    txt.setAttribute('x', n.x - 8);
    txt.setAttribute('text-anchor', 'end');
  } else {
    txt.setAttribute('x', n.x + nodeW + 8);
    txt.setAttribute('text-anchor', 'start');
  }
  txt.setAttribute('y', n.y + n.h / 2 + 1);
  txt.setAttribute('dominant-baseline', 'middle');
  txt.setAttribute('font-size', '14');
  txt.setAttribute('font-weight', 'bold');
  txt.setAttribute('fill', '#333');
  txt.textContent = n.name;
  svg.appendChild(txt);
});
'''

# 为 L1 构建特殊引擎（maxLayers=4）
L1_full_engine = L1_engine + common_engine_tail

# L2/L3/L4 引擎（maxLayers=5）
default_engine = L3_engine + common_engine_tail

test_data = {
    'L1': L1_data + L1_full_engine,
    'L2': L2_data + default_engine,
    'L3': L3_data + default_engine,
    'L4': L4_data + default_engine,
}

for level, script in test_data.items():
    content = head + '\n' + script + '\n' + tail
    filename = f'sankey-{level}.html'
    with open(str(OUTPUT_DIR / filename), 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
