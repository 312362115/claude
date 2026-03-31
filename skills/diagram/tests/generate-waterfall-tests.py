"""生成 waterfall L1-L4 测试 HTML 文件"""

# 瀑布图模板头部
HEAD = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1200, height=800">
<title>瀑布图测试</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1200px; height: 800px;
    font-family: -apple-system, system-ui, 'PingFang SC', sans-serif;
    background: #ffffff;
    display: inline-block; text-align: center;
  }
  .title { font-size: 22px; font-weight: 700; color: #0F172A; margin-top: 28px; }
  .subtitle { font-size: 14px; color: #64748B; margin-top: 6px; }
  .legend {
    display: flex; gap: 32px; margin-top: 20px;
  }
  .legend-item {
    display: flex; align-items: center; gap: 8px;
    font-size: 14px; color: #64748B;
  }
  .legend-dot {
    width: 20px; height: 12px; border-radius: 3px;
  }
  .chart-wrap { margin-top: 16px; position: relative; }
</style>
</head>
<body>
  <div class="title">瀑布图测试</div>
  <div class="subtitle">单位：万元</div>
  <div class="legend">
    <div class="legend-item">
      <div class="legend-dot" style="background: #3B82F6"></div>
      起始/合计
    </div>
    <div class="legend-item">
      <div class="legend-dot" style="background: #10B981"></div>
      增加
    </div>
    <div class="legend-item">
      <div class="legend-dot" style="background: #F43F5E"></div>
      减少
    </div>
  </div>
  <div class="chart-wrap">
    <svg id="waterfall" width="1100" height="640" viewBox="0 0 1100 640"></svg>
  </div>
<script>
'''

TAIL = '</script>\n</body>\n</html>\n'

# 通用渲染引擎（接收 data 数组）
ENGINE = '''
  const colors = {
    start: '#3B82F6', total: '#3B82F6',
    increase: '#10B981', decrease: '#F43F5E'
  };

  const svgNS = 'http://www.w3.org/2000/svg';
  const svg = document.getElementById('waterfall');

  const chartLeft = 80, chartRight = 1060;
  const chartTop = 20, chartBottom = 560;
  const chartW = chartRight - chartLeft;
  const chartH = chartBottom - chartTop;

  // 计算累计值
  let running = 0;
  const bars = data.map(d => {
    if (d.type === 'start') {
      running = d.value;
      return { ...d, bottom: 0, top: d.value };
    } else if (d.type === 'total') {
      return { ...d, bottom: 0, top: running, value: running };
    } else {
      const prev = running;
      running += d.value;
      return d.value >= 0
        ? { ...d, bottom: prev, top: running }
        : { ...d, bottom: running, top: prev };
    }
  });

  const allVals = bars.flatMap(b => [b.bottom, b.top]);
  const dataMax = Math.ceil(Math.max(...allVals) / 1000) * 1000;
  const yRange = dataMax;

  function yPos(val) {
    return chartBottom - (val / yRange) * chartH;
  }

  // 网格线 + Y 轴
  const gridSteps = 5;
  const gridStep = yRange / gridSteps;
  for (let i = 0; i <= gridSteps; i++) {
    const val = gridStep * i;
    const y = yPos(val);
    const line = document.createElementNS(svgNS, 'line');
    line.setAttribute('x1', chartLeft); line.setAttribute('x2', chartRight);
    line.setAttribute('y1', y); line.setAttribute('y2', y);
    line.setAttribute('stroke', '#E2E8F0');
    line.setAttribute('stroke-dasharray', i === 0 ? 'none' : '4,4');
    svg.appendChild(line);

    const label = document.createElementNS(svgNS, 'text');
    label.setAttribute('x', chartLeft - 12); label.setAttribute('y', y + 4);
    label.setAttribute('text-anchor', 'end');
    label.setAttribute('font-size', '13'); label.setAttribute('fill', '#94A3B8');
    label.textContent = val.toLocaleString();
    svg.appendChild(label);
  }

  const n = bars.length;
  const barGap = 16;
  const barW = (chartW - barGap * (n + 1)) / n;

  bars.forEach((b, i) => {
    const x = chartLeft + barGap + i * (barW + barGap);
    const yTop = yPos(b.top);
    const yBottom = yPos(b.bottom);
    const h = Math.max(yBottom - yTop, 2);

    const rect = document.createElementNS(svgNS, 'rect');
    rect.setAttribute('x', x); rect.setAttribute('y', yTop);
    rect.setAttribute('width', barW); rect.setAttribute('height', h);
    rect.setAttribute('rx', '4');
    rect.setAttribute('fill', colors[b.type]);
    rect.setAttribute('opacity', '0.85');
    svg.appendChild(rect);

    const valEl = document.createElementNS(svgNS, 'text');
    valEl.setAttribute('x', x + barW / 2); valEl.setAttribute('y', yTop - 8);
    valEl.setAttribute('text-anchor', 'middle');
    valEl.setAttribute('font-size', '13'); valEl.setAttribute('font-weight', '700');
    valEl.setAttribute('fill', colors[b.type]);
    if (b.type === 'start' || b.type === 'total') {
      valEl.textContent = b.value.toLocaleString();
    } else if (b.type === 'increase') {
      valEl.textContent = '+' + b.value.toLocaleString();
    } else {
      valEl.textContent = b.value.toLocaleString();
    }
    svg.appendChild(valEl);

    // X 轴标签（长文本自动缩小字号）
    const nameEl = document.createElementNS(svgNS, 'text');
    nameEl.setAttribute('x', x + barW / 2);
    nameEl.setAttribute('y', chartBottom + 24);
    nameEl.setAttribute('text-anchor', 'middle');
    nameEl.setAttribute('font-size', b.name.length > 5 ? '12' : '14');
    nameEl.setAttribute('font-weight', '500');
    nameEl.setAttribute('fill', '#1E293B');
    nameEl.textContent = b.name;
    svg.appendChild(nameEl);

    if (i < n - 1) {
      const connY = b.type === 'decrease' ? yPos(b.bottom) : yPos(b.top);
      const nextX = chartLeft + barGap + (i + 1) * (barW + barGap);
      const conn = document.createElementNS(svgNS, 'line');
      conn.setAttribute('x1', x + barW); conn.setAttribute('x2', nextX);
      conn.setAttribute('y1', connY); conn.setAttribute('y2', connY);
      conn.setAttribute('stroke', '#CBD5E1');
      conn.setAttribute('stroke-width', '1.5');
      conn.setAttribute('stroke-dasharray', '4,3');
      svg.appendChild(conn);
    }
  });
'''

# L1: 4 项（起始 + 1增 + 1减 + 合计）
L1_DATA = '''
  const data = [
    { name: '期初', value: 3000, type: 'start' },
    { name: '收入', value: 2000, type: 'increase' },
    { name: '支出', value: -800, type: 'decrease' },
    { name: '期末', value: 0,    type: 'total' }
  ];
'''

# L2: 8 项（默认模板数据）
L2_DATA = '''
  const data = [
    { name: '期初利润', value: 5200, type: 'start' },
    { name: '主营收入', value: 3800, type: 'increase' },
    { name: '投资收益', value: 1200, type: 'increase' },
    { name: '其他收入', value: 600,  type: 'increase' },
    { name: '运营成本', value: -2400, type: 'decrease' },
    { name: '人力成本', value: -1800, type: 'decrease' },
    { name: '税费',     value: -900,  type: 'decrease' },
    { name: '期末利润', value: 0,    type: 'total' }
  ];
'''

# L3: 12 项
L3_DATA = '''
  const data = [
    { name: '年初余额',   value: 8500, type: 'start' },
    { name: '产品收入',   value: 4200, type: 'increase' },
    { name: '服务收入',   value: 2800, type: 'increase' },
    { name: '广告收入',   value: 1500, type: 'increase' },
    { name: '投资回报',   value: 900,  type: 'increase' },
    { name: '政府补贴',   value: 600,  type: 'increase' },
    { name: '人力成本',   value: -3200, type: 'decrease' },
    { name: '研发投入',   value: -2100, type: 'decrease' },
    { name: '营销费用',   value: -1800, type: 'decrease' },
    { name: '运营成本',   value: -1400, type: 'decrease' },
    { name: '税费',       value: -1200, type: 'decrease' },
    { name: '年末余额',   value: 0,    type: 'total' }
  ];
'''

# L4: 12 项，适配 1200px 宽度
L4_DATA = '''
  const data = [
    { name: 'FY23净利',   value: 12000, type: 'start' },
    { name: 'SaaS订阅',   value: 6800,  type: 'increase' },
    { name: '专业服务',     value: 3200,  type: 'increase' },
    { name: '硬件销售',     value: 2100,  type: 'increase' },
    { name: '投资收益',     value: 800,   type: 'increase' },
    { name: '人员薪酬',     value: -5200, type: 'decrease' },
    { name: '云设施',       value: -3800, type: 'decrease' },
    { name: '研发投入',     value: -2600, type: 'decrease' },
    { name: '市场营销',     value: -2200, type: 'decrease' },
    { name: '管理费用',     value: -1500, type: 'decrease' },
    { name: '所得税',       value: -1800, type: 'decrease' },
    { name: 'FY24净利',   value: 0,     type: 'total' }
  ];
'''

test_data = {
    'L1': L1_DATA,
    'L2': L2_DATA,
    'L3': L3_DATA,
    'L4': L4_DATA,
}

for level, data_block in test_data.items():
    content = HEAD + data_block + ENGINE + TAIL
    filename = f'waterfall-{level}.html'
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
