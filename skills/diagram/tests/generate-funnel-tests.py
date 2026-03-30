"""生成 funnel L1-L4 测试 HTML 文件"""
import re

# 读取模板
with open('../templates/html/funnel.html', 'r') as f:
    template = f.read()

# 提取 <script> 前的 HTML 部分
head = template[:template.index('<script>') + len('<script>')]

# 提取引擎部分：从 IIFE 内 colors 定义之后的渲染逻辑
# 我们替换整个 IIFE 内容，所以提取尾部
tail = '</script>\n</body>\n</html>\n'

# L1: 3 阶段，简单转化
L1 = '''
(function() {
  const data = [
    { name: '曝光',   value: 50000 },
    { name: '点击',   value: 18000 },
    { name: '转化',   value: 5400 }
  ];

  const colors = ['#3B82F6', '#10B981', '#F59E0B'];
  const lightBg = ['#EFF6FF', '#ECFDF5', '#FFFBEB'];

  const svgNS = 'http://www.w3.org/2000/svg';
  const svg = document.getElementById('funnel');

  const cx = 550;
  const topY = 30;
  const maxWidth = 800;
  const minWidth = 200;
  const totalHeight = 580;
  const gap = 6;
  const n = data.length;
  const stepH = (totalHeight - gap * (n - 1)) / n;
  const maxVal = data[0].value;

  function widthFor(val) {
    const ratio = val / maxVal;
    return minWidth + (maxWidth - minWidth) * ratio;
  }

  data.forEach((d, i) => {
    const y = topY + i * (stepH + gap);
    const w1 = widthFor(d.value);
    const w2 = i < n - 1 ? widthFor(data[i + 1].value) : w1 * 0.7;

    const x1L = cx - w1 / 2; const x1R = cx + w1 / 2;
    const x2L = cx - w2 / 2; const x2R = cx + w2 / 2;

    const path = document.createElementNS(svgNS, 'path');
    path.setAttribute('d', `M ${x1L},${y} L ${x1R},${y} L ${x2R},${y + stepH} L ${x2L},${y + stepH} Z`);
    path.setAttribute('fill', colors[i]);
    path.setAttribute('opacity', '0.85');
    svg.appendChild(path);

    const nameEl = document.createElementNS(svgNS, 'text');
    nameEl.setAttribute('x', cx - maxWidth / 2 - 20);
    nameEl.setAttribute('y', y + stepH / 2 + 5);
    nameEl.setAttribute('text-anchor', 'end');
    nameEl.setAttribute('font-size', '15');
    nameEl.setAttribute('font-weight', '600');
    nameEl.setAttribute('fill', '#1E293B');
    nameEl.textContent = d.name;
    svg.appendChild(nameEl);

    const valEl = document.createElementNS(svgNS, 'text');
    valEl.setAttribute('x', cx);
    valEl.setAttribute('y', y + stepH / 2 + 2);
    valEl.setAttribute('text-anchor', 'middle');
    valEl.setAttribute('font-size', '18');
    valEl.setAttribute('font-weight', '700');
    valEl.setAttribute('fill', '#ffffff');
    valEl.textContent = d.value.toLocaleString();
    svg.appendChild(valEl);

    const pct = (d.value / maxVal * 100).toFixed(1);
    const pctEl = document.createElementNS(svgNS, 'text');
    pctEl.setAttribute('x', cx);
    pctEl.setAttribute('y', y + stepH / 2 + 20);
    pctEl.setAttribute('text-anchor', 'middle');
    pctEl.setAttribute('font-size', '13');
    pctEl.setAttribute('fill', 'rgba(255,255,255,0.85)');
    pctEl.textContent = pct + '%';
    svg.appendChild(pctEl);

    if (i < n - 1) {
      const convRate = (data[i + 1].value / d.value * 100).toFixed(1);
      const arrowY = y + stepH + gap / 2;
      const ax = cx + maxWidth / 2 + 30;
      const arrow = document.createElementNS(svgNS, 'path');
      arrow.setAttribute('d', `M ${ax},${arrowY - 12} L ${ax},${arrowY + 12} M ${ax - 5},${arrowY + 7} L ${ax},${arrowY + 12} L ${ax + 5},${arrowY + 7}`);
      arrow.setAttribute('fill', 'none');
      arrow.setAttribute('stroke', '#94A3B8');
      arrow.setAttribute('stroke-width', '2');
      arrow.setAttribute('stroke-linecap', 'round');
      svg.appendChild(arrow);

      const convEl = document.createElementNS(svgNS, 'text');
      convEl.setAttribute('x', ax + 16);
      convEl.setAttribute('y', arrowY + 5);
      convEl.setAttribute('text-anchor', 'start');
      convEl.setAttribute('font-size', '14');
      convEl.setAttribute('font-weight', '600');
      convEl.setAttribute('fill', '#64748B');
      convEl.textContent = convRate + '%';
      svg.appendChild(convEl);
    }
  });
})();
'''

# L2: 5 阶段（默认模板数据）
L2 = '''
(function() {
  const data = [
    { name: '访问首页',   value: 100000 },
    { name: '浏览商品',   value: 68000 },
    { name: '加入购物车', value: 35200 },
    { name: '提交订单',   value: 18600 },
    { name: '完成支付',   value: 12400 }
  ];

  const colors = ['#3B82F6', '#10B981', '#F59E0B', '#F43F5E', '#8B5CF6'];

  const svgNS = 'http://www.w3.org/2000/svg';
  const svg = document.getElementById('funnel');

  const cx = 550;
  const topY = 30;
  const maxWidth = 800;
  const minWidth = 200;
  const totalHeight = 580;
  const gap = 6;
  const n = data.length;
  const stepH = (totalHeight - gap * (n - 1)) / n;
  const maxVal = data[0].value;

  function widthFor(val) {
    const ratio = val / maxVal;
    return minWidth + (maxWidth - minWidth) * ratio;
  }

  data.forEach((d, i) => {
    const y = topY + i * (stepH + gap);
    const w1 = widthFor(d.value);
    const w2 = i < n - 1 ? widthFor(data[i + 1].value) : w1 * 0.7;

    const x1L = cx - w1 / 2; const x1R = cx + w1 / 2;
    const x2L = cx - w2 / 2; const x2R = cx + w2 / 2;

    const path = document.createElementNS(svgNS, 'path');
    path.setAttribute('d', `M ${x1L},${y} L ${x1R},${y} L ${x2R},${y + stepH} L ${x2L},${y + stepH} Z`);
    path.setAttribute('fill', colors[i]);
    path.setAttribute('opacity', '0.85');
    svg.appendChild(path);

    const nameEl = document.createElementNS(svgNS, 'text');
    nameEl.setAttribute('x', cx - maxWidth / 2 - 20);
    nameEl.setAttribute('y', y + stepH / 2 + 5);
    nameEl.setAttribute('text-anchor', 'end');
    nameEl.setAttribute('font-size', '15');
    nameEl.setAttribute('font-weight', '600');
    nameEl.setAttribute('fill', '#1E293B');
    nameEl.textContent = d.name;
    svg.appendChild(nameEl);

    const valEl = document.createElementNS(svgNS, 'text');
    valEl.setAttribute('x', cx);
    valEl.setAttribute('y', y + stepH / 2 + 2);
    valEl.setAttribute('text-anchor', 'middle');
    valEl.setAttribute('font-size', '18');
    valEl.setAttribute('font-weight', '700');
    valEl.setAttribute('fill', '#ffffff');
    valEl.textContent = d.value.toLocaleString();
    svg.appendChild(valEl);

    const pct = (d.value / maxVal * 100).toFixed(1);
    const pctEl = document.createElementNS(svgNS, 'text');
    pctEl.setAttribute('x', cx);
    pctEl.setAttribute('y', y + stepH / 2 + 20);
    pctEl.setAttribute('text-anchor', 'middle');
    pctEl.setAttribute('font-size', '13');
    pctEl.setAttribute('fill', 'rgba(255,255,255,0.85)');
    pctEl.textContent = pct + '%';
    svg.appendChild(pctEl);

    if (i < n - 1) {
      const convRate = (data[i + 1].value / d.value * 100).toFixed(1);
      const arrowY = y + stepH + gap / 2;
      const ax = cx + maxWidth / 2 + 30;
      const arrow = document.createElementNS(svgNS, 'path');
      arrow.setAttribute('d', `M ${ax},${arrowY - 12} L ${ax},${arrowY + 12} M ${ax - 5},${arrowY + 7} L ${ax},${arrowY + 12} L ${ax + 5},${arrowY + 7}`);
      arrow.setAttribute('fill', 'none');
      arrow.setAttribute('stroke', '#94A3B8');
      arrow.setAttribute('stroke-width', '2');
      arrow.setAttribute('stroke-linecap', 'round');
      svg.appendChild(arrow);

      const convEl = document.createElementNS(svgNS, 'text');
      convEl.setAttribute('x', ax + 16);
      convEl.setAttribute('y', arrowY + 5);
      convEl.setAttribute('text-anchor', 'start');
      convEl.setAttribute('font-size', '14');
      convEl.setAttribute('font-weight', '600');
      convEl.setAttribute('fill', '#64748B');
      convEl.textContent = convRate + '%';
      svg.appendChild(convEl);
    }
  });
})();
'''

# L3: 7 阶段
L3 = '''
(function() {
  const data = [
    { name: '广告曝光',     value: 500000 },
    { name: '广告点击',     value: 185000 },
    { name: '落地页访问',   value: 120000 },
    { name: '注册账号',     value: 54000 },
    { name: '激活使用',     value: 28000 },
    { name: '首次付费',     value: 9800 },
    { name: '持续订阅',     value: 4200 }
  ];

  const colors = ['#3B82F6', '#10B981', '#F59E0B', '#F43F5E', '#8B5CF6', '#06B6D4', '#F97316'];

  const svgNS = 'http://www.w3.org/2000/svg';
  const svg = document.getElementById('funnel');

  const cx = 550;
  const topY = 20;
  const maxWidth = 800;
  const minWidth = 160;
  const totalHeight = 600;
  const gap = 4;
  const n = data.length;
  const stepH = (totalHeight - gap * (n - 1)) / n;
  const maxVal = data[0].value;

  function widthFor(val) {
    const ratio = val / maxVal;
    return minWidth + (maxWidth - minWidth) * ratio;
  }

  data.forEach((d, i) => {
    const y = topY + i * (stepH + gap);
    const w1 = widthFor(d.value);
    const w2 = i < n - 1 ? widthFor(data[i + 1].value) : w1 * 0.7;

    const x1L = cx - w1 / 2; const x1R = cx + w1 / 2;
    const x2L = cx - w2 / 2; const x2R = cx + w2 / 2;

    const path = document.createElementNS(svgNS, 'path');
    path.setAttribute('d', `M ${x1L},${y} L ${x1R},${y} L ${x2R},${y + stepH} L ${x2L},${y + stepH} Z`);
    path.setAttribute('fill', colors[i]);
    path.setAttribute('opacity', '0.85');
    svg.appendChild(path);

    const nameEl = document.createElementNS(svgNS, 'text');
    nameEl.setAttribute('x', cx - maxWidth / 2 - 20);
    nameEl.setAttribute('y', y + stepH / 2 + 5);
    nameEl.setAttribute('text-anchor', 'end');
    nameEl.setAttribute('font-size', '14');
    nameEl.setAttribute('font-weight', '600');
    nameEl.setAttribute('fill', '#1E293B');
    nameEl.textContent = d.name;
    svg.appendChild(nameEl);

    const valEl = document.createElementNS(svgNS, 'text');
    valEl.setAttribute('x', cx);
    valEl.setAttribute('y', y + stepH / 2 + 2);
    valEl.setAttribute('text-anchor', 'middle');
    valEl.setAttribute('font-size', '16');
    valEl.setAttribute('font-weight', '700');
    valEl.setAttribute('fill', '#ffffff');
    valEl.textContent = d.value.toLocaleString();
    svg.appendChild(valEl);

    const pct = (d.value / maxVal * 100).toFixed(1);
    const pctEl = document.createElementNS(svgNS, 'text');
    pctEl.setAttribute('x', cx);
    pctEl.setAttribute('y', y + stepH / 2 + 18);
    pctEl.setAttribute('text-anchor', 'middle');
    pctEl.setAttribute('font-size', '12');
    pctEl.setAttribute('fill', 'rgba(255,255,255,0.85)');
    pctEl.textContent = pct + '%';
    svg.appendChild(pctEl);

    if (i < n - 1) {
      const convRate = (data[i + 1].value / d.value * 100).toFixed(1);
      const arrowY = y + stepH + gap / 2;
      const ax = cx + maxWidth / 2 + 30;
      const arrow = document.createElementNS(svgNS, 'path');
      arrow.setAttribute('d', `M ${ax},${arrowY - 10} L ${ax},${arrowY + 10} M ${ax - 4},${arrowY + 6} L ${ax},${arrowY + 10} L ${ax + 4},${arrowY + 6}`);
      arrow.setAttribute('fill', 'none');
      arrow.setAttribute('stroke', '#94A3B8');
      arrow.setAttribute('stroke-width', '2');
      arrow.setAttribute('stroke-linecap', 'round');
      svg.appendChild(arrow);

      const convEl = document.createElementNS(svgNS, 'text');
      convEl.setAttribute('x', ax + 16);
      convEl.setAttribute('y', arrowY + 5);
      convEl.setAttribute('text-anchor', 'start');
      convEl.setAttribute('font-size', '13');
      convEl.setAttribute('font-weight', '600');
      convEl.setAttribute('fill', '#64748B');
      convEl.textContent = convRate + '%';
      svg.appendChild(convEl);
    }
  });
})();
'''

# L4: 9 阶段，超长名称
L4 = '''
(function() {
  const data = [
    { name: '全渠道广告曝光',       value: 2000000 },
    { name: '广告点击/互动',        value: 680000 },
    { name: '官网/APP 落地页访问', value: 420000 },
    { name: '免费注册/试用',        value: 156000 },
    { name: '完成新手引导',          value: 89000 },
    { name: '核心功能激活',          value: 52000 },
    { name: '首次付费转化',          value: 18500 },
    { name: '续费/升级',             value: 8200 },
    { name: '推荐新用户',            value: 2100 }
  ];

  const colors = ['#3B82F6', '#10B981', '#F59E0B', '#F43F5E', '#8B5CF6', '#06B6D4', '#F97316', '#64748B', '#10B981'];

  const svgNS = 'http://www.w3.org/2000/svg';
  const svg = document.getElementById('funnel');

  const cx = 550;
  const topY = 10;
  const maxWidth = 780;
  const minWidth = 120;
  const totalHeight = 620;
  const gap = 3;
  const n = data.length;
  const stepH = (totalHeight - gap * (n - 1)) / n;
  const maxVal = data[0].value;

  function widthFor(val) {
    const ratio = val / maxVal;
    return minWidth + (maxWidth - minWidth) * ratio;
  }

  data.forEach((d, i) => {
    const y = topY + i * (stepH + gap);
    const w1 = widthFor(d.value);
    const w2 = i < n - 1 ? widthFor(data[i + 1].value) : w1 * 0.7;

    const x1L = cx - w1 / 2; const x1R = cx + w1 / 2;
    const x2L = cx - w2 / 2; const x2R = cx + w2 / 2;

    const path = document.createElementNS(svgNS, 'path');
    path.setAttribute('d', `M ${x1L},${y} L ${x1R},${y} L ${x2R},${y + stepH} L ${x2L},${y + stepH} Z`);
    path.setAttribute('fill', colors[i]);
    path.setAttribute('opacity', '0.85');
    svg.appendChild(path);

    const nameEl = document.createElementNS(svgNS, 'text');
    nameEl.setAttribute('x', cx - maxWidth / 2 - 16);
    nameEl.setAttribute('y', y + stepH / 2 + 4);
    nameEl.setAttribute('text-anchor', 'end');
    nameEl.setAttribute('font-size', '13');
    nameEl.setAttribute('font-weight', '600');
    nameEl.setAttribute('fill', '#1E293B');
    nameEl.textContent = d.name;
    svg.appendChild(nameEl);

    const valEl = document.createElementNS(svgNS, 'text');
    valEl.setAttribute('x', cx);
    valEl.setAttribute('y', y + stepH / 2 + 1);
    valEl.setAttribute('text-anchor', 'middle');
    valEl.setAttribute('font-size', '14');
    valEl.setAttribute('font-weight', '700');
    valEl.setAttribute('fill', '#ffffff');
    valEl.textContent = d.value.toLocaleString();
    svg.appendChild(valEl);

    const pct = (d.value / maxVal * 100).toFixed(1);
    const pctEl = document.createElementNS(svgNS, 'text');
    pctEl.setAttribute('x', cx);
    pctEl.setAttribute('y', y + stepH / 2 + 16);
    pctEl.setAttribute('text-anchor', 'middle');
    pctEl.setAttribute('font-size', '11');
    pctEl.setAttribute('fill', 'rgba(255,255,255,0.85)');
    pctEl.textContent = pct + '%';
    svg.appendChild(pctEl);

    if (i < n - 1) {
      const convRate = (data[i + 1].value / d.value * 100).toFixed(1);
      const arrowY = y + stepH + gap / 2;
      const ax = cx + maxWidth / 2 + 26;
      const arrow = document.createElementNS(svgNS, 'path');
      arrow.setAttribute('d', `M ${ax},${arrowY - 8} L ${ax},${arrowY + 8} M ${ax - 4},${arrowY + 4} L ${ax},${arrowY + 8} L ${ax + 4},${arrowY + 4}`);
      arrow.setAttribute('fill', 'none');
      arrow.setAttribute('stroke', '#94A3B8');
      arrow.setAttribute('stroke-width', '1.5');
      arrow.setAttribute('stroke-linecap', 'round');
      svg.appendChild(arrow);

      const convEl = document.createElementNS(svgNS, 'text');
      convEl.setAttribute('x', ax + 14);
      convEl.setAttribute('y', arrowY + 4);
      convEl.setAttribute('text-anchor', 'start');
      convEl.setAttribute('font-size', '12');
      convEl.setAttribute('font-weight', '600');
      convEl.setAttribute('fill', '#64748B');
      convEl.textContent = convRate + '%';
      svg.appendChild(convEl);
    }
  });
})();
'''

test_data = {'L1': L1, 'L2': L2, 'L3': L3, 'L4': L4}

for level, script in test_data.items():
    content = head + '\n' + script + '\n' + tail
    filename = f'funnel-{level}.html'
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
