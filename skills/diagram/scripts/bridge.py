"""
Diagram Bridge — JSON 配置 → PNG/HTML 图表

统一图表生成入口，供 deep-research 等技能调用。
接收 JSON 配置，调用 Diagram 模板生成图表，输出 PNG 或自包含 HTML。

用法：
  python bridge.py --type bar --config data.json --output chart.png
  python bridge.py --type pie --config data.json --output chart.html -f html
  echo '{"type":"pie",...}' | python bridge.py --output chart.png

JSON 配置格式见各适配器的 docstring，或参考 docs/specs/2026-03-31-diagram-bridge-design.md
"""

import sys
import os
import json
import argparse
import re
import tempfile
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
TEMPLATES_DIR = SCRIPTS_DIR / '../templates/html'
LIB_DIR = TEMPLATES_DIR / 'lib'


# ─── HTML 组装 ───

def _safe_inline(js_content):
    """转义 JS 中的 </script> 防止被浏览器误解析"""
    return js_content.replace('</script>', '<\\/script>')


def make_html(title, subtitle, svg_id, body_class, scripts, chart_js):
    """组装完整的 HTML 页面
    SVG 初始尺寸为占位值，各适配器的 JS 会在运行时动态设置实际尺寸。
    """
    lib_css = (LIB_DIR / 'base.css').read_text(encoding='utf-8')
    lib_utils = _safe_inline((LIB_DIR / 'utils.js').read_text(encoding='utf-8'))

    script_tags = ''
    for s in scripts:
        js = _safe_inline((LIB_DIR / s).read_text(encoding='utf-8'))
        script_tags += f'<script>\n{js}\n</script>\n'

    # 提供 setSvgSize 辅助函数，各适配器调用它来设置 SVG 实际尺寸
    size_helper = '''function setSvgSize(svg, w, h) {
  svg.setAttribute('width', w);
  svg.setAttribute('height', h);
  svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
}'''

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
{lib_css}
body {{
  display: flex; flex-direction: column; align-items: center;
}}
.title {{ font-size: 22px; font-weight: 700; color: #1a1a2e; margin-top: 28px; }}
.subtitle {{ font-size: 14px; color: #888; margin-top: 6px; }}
.chart-wrap {{ margin-top: 20px; position: relative; }}
</style>
</head>
<body class="{body_class}">
  <div class="title">{title}</div>
  <div class="subtitle">{subtitle}</div>
  <div class="chart-wrap">
    <svg id="{svg_id}"></svg>
  </div>
<script>
{lib_utils}
{size_helper}
</script>
{script_tags}
<script>
{chart_js}
</script>
</body>
</html>
'''


# ─── 图表适配器 ───

def adapt_bar(config):
    """柱状图
    JSON data: { categories: [...], series: [{name, values}] }
    """
    d = config['data']
    cats = json.dumps(d['categories'], ensure_ascii=False)
    series = json.dumps(d['series'], ensure_ascii=False)

    return make_html(
        config.get('title', '柱状图'),
        config.get('subtitle', ''),
        'chart', 'auto-size', [],
        f'''(function() {{
  const svg = document.getElementById('chart');
  const categories = {cats};
  const series = {series};

  const colors = ['#667eea', '#f5576c', '#43e97b', '#4facfe', '#fa8231', '#a55eea'];
  const N = categories.length;
  const M = series.length;

  // 动态计算尺寸
  const padL = 80, padR = 40, padT = 20, padB = 70;
  const groupW = Math.max(Math.min(120, 900 / N), 50);
  const chartW = groupW * N;
  const chartH = Math.min(Math.max(400, N * 30), 580);
  const svgW = padL + chartW + padR;
  const svgH = padT + chartH + padB;
  setSvgSize(svg, svgW, svgH);

  const barW = Math.min(groupW * 0.7 / M, 60);
  const barGap = 4;

  // Y 轴范围
  const allVals = series.flatMap(s => s.values);
  const maxVal = Math.max(...allVals) * 1.15;

  // Y 轴网格
  const ticks = 5;
  for (let i = 0; i <= ticks; i++) {{
    const y = padT + chartH - (i / ticks) * chartH;
    const val = (maxVal * i / ticks);
    svg.appendChild(el('line', {{ x1: padL, y1: y, x2: padL + chartW, y2: y,
      stroke: '#E2E8F0', 'stroke-width': 1 }}));
    svg.appendChild(el('text', {{ x: padL - 12, y: y + 4,
      'text-anchor': 'end', 'font-size': 12, fill: '#94A3B8' }},
      val >= 1000 ? (val/1000).toFixed(0) + 'k' : val.toFixed(0)));
  }}

  // 柱子
  series.forEach((s, si) => {{
    s.values.forEach((v, ci) => {{
      const x = padL + ci * groupW + (groupW - M * (barW + barGap) + barGap) / 2 + si * (barW + barGap);
      const h = (v / maxVal) * chartH;
      const y = padT + chartH - h;

      // 渐变
      const gradId = 'g' + si + '_' + ci;
      const defs = svg.querySelector('defs') || svg.appendChild(el('defs'));
      const grad = el('linearGradient', {{ id: gradId, x1: '0', y1: '0', x2: '0', y2: '1' }});
      const s1 = el('stop', {{ offset: '0%', 'stop-color': colors[si], 'stop-opacity': '0.9' }});
      const s2 = el('stop', {{ offset: '100%', 'stop-color': colors[si], 'stop-opacity': '0.6' }});
      grad.appendChild(s1); grad.appendChild(s2);
      defs.appendChild(grad);

      svg.appendChild(el('rect', {{ x: x, y: y, width: barW, height: h,
        rx: 3, fill: 'url(#' + gradId + ')' }}));

      // 数值标签
      svg.appendChild(el('text', {{ x: x + barW/2, y: y - 6,
        'text-anchor': 'middle', 'font-size': 11, 'font-weight': 600, fill: colors[si] }},
        v >= 1000 ? (v/1000).toFixed(1) + 'k' : String(v)));
    }});
  }});

  // X 轴标签
  categories.forEach((c, i) => {{
    svg.appendChild(el('text', {{ x: padL + i * groupW + groupW/2, y: padT + chartH + 24,
      'text-anchor': 'middle', 'font-size': 13, fill: '#64748B' }}, c));
  }});

  // 图例
  const legendY = padT + chartH + 48;
  const legendStartX = svgW/2 - (series.length * 120)/2;
  series.forEach((s, i) => {{
    const lx = legendStartX + i * 120;
    svg.appendChild(el('rect', {{ x: lx, y: legendY - 8, width: 16, height: 10, rx: 2, fill: colors[i] }}));
    svg.appendChild(el('text', {{ x: lx + 22, y: legendY, 'font-size': 12, fill: '#64748B' }}, s.name));
  }});
}})();'''
    )


def adapt_line(config):
    """折线图
    JSON data: { categories: [...], series: [{name, values}] }
    """
    d = config['data']
    cats = json.dumps(d['categories'], ensure_ascii=False)
    series = json.dumps(d['series'], ensure_ascii=False)

    return make_html(
        config.get('title', '折线图'),
        config.get('subtitle', ''),
        'chart', 'auto-size', [],
        f'''(function() {{
  const svg = document.getElementById('chart');
  const categories = {cats};
  const series = {series};

  const colors = ['#667eea', '#f5576c', '#43e97b', '#4facfe', '#fa8231'];
  const N = categories.length;

  // 动态计算尺寸
  const padL = 80, padR = 40, padT = 20, padB = 70;
  const pointGap = Math.max(Math.min(80, 900 / N), 30);
  const chartW = pointGap * (N - 1) + 40;
  const chartH = Math.min(Math.max(400, N * 20), 580);
  const svgW = padL + chartW + padR;
  const svgH = padT + chartH + padB;
  setSvgSize(svg, svgW, svgH);

  const allVals = series.flatMap(s => s.values);
  const maxVal = Math.max(...allVals) * 1.15;

  // Y 轴网格
  for (let i = 0; i <= 5; i++) {{
    const y = padT + chartH - (i / 5) * chartH;
    const val = maxVal * i / 5;
    svg.appendChild(el('line', {{ x1: padL, y1: y, x2: padL + chartW, y2: y,
      stroke: '#E2E8F0', 'stroke-width': 1 }}));
    svg.appendChild(el('text', {{ x: padL - 12, y: y + 4,
      'text-anchor': 'end', 'font-size': 12, fill: '#94A3B8' }},
      val >= 1000 ? (val/1000).toFixed(0) + 'k' : val.toFixed(0)));
  }}

  // 折线
  series.forEach((s, si) => {{
    const points = s.values.map((v, i) => {{
      const x = padL + (i / (N - 1)) * chartW;
      const y = padT + chartH - (v / maxVal) * chartH;
      return [x, y];
    }});

    // 面积
    const areaD = 'M ' + points.map(p => p.join(',')).join(' L ') +
      ' L ' + (padL + chartW) + ',' + (padT + chartH) +
      ' L ' + padL + ',' + (padT + chartH) + ' Z';
    svg.appendChild(el('path', {{ d: areaD, fill: colors[si], opacity: 0.08 }}));

    // 线
    const lineD = 'M ' + points.map(p => p.join(',')).join(' L ');
    svg.appendChild(el('path', {{ d: lineD, fill: 'none', stroke: colors[si],
      'stroke-width': 2.5, 'stroke-linejoin': 'round' }}));

    // 数据点
    points.forEach(([x, y]) => {{
      svg.appendChild(el('circle', {{ cx: x, cy: y, r: 4,
        fill: colors[si], stroke: '#fff', 'stroke-width': 2 }}));
    }});
  }});

  // X 轴标签
  categories.forEach((c, i) => {{
    const x = padL + (i / (N - 1)) * chartW;
    svg.appendChild(el('text', {{ x: x, y: padT + chartH + 24,
      'text-anchor': 'middle', 'font-size': 12, fill: '#64748B' }}, c));
  }});

  // 图例
  const legendY = padT + chartH + 48;
  const legendStartX = svgW/2 - (series.length * 120)/2;
  series.forEach((s, i) => {{
    const lx = legendStartX + i * 120;
    svg.appendChild(el('line', {{ x1: lx, y1: legendY - 3, x2: lx + 16, y2: legendY - 3,
      stroke: colors[i], 'stroke-width': 2.5 }}));
    svg.appendChild(el('text', {{ x: lx + 22, y: legendY, 'font-size': 12, fill: '#64748B' }}, s.name));
  }});
}})();'''
    )


def adapt_pie(config):
    """饼图/环形图
    JSON data: { items: [{name, value}] }
    """
    d = config['data']
    items = json.dumps(d['items'], ensure_ascii=False)

    # 读取 pie 模板的渲染引擎（从 total 计算之后）
    template = (TEMPLATES_DIR / 'pie.html').read_text(encoding='utf-8')
    # 提取从 "// 布局参数" 到 </script> 的引擎代码
    engine_match = re.search(r'(// 布局参数.*?)</script>', template, re.DOTALL)
    engine = engine_match.group(1) if engine_match else ''

    return make_html(
        config.get('title', '饼图'),
        config.get('subtitle', ''),
        'pie', 'auto-size', [],
        f'''const data = {items};
const colors = [
  'rgba(102,126,234,0.75)', 'rgba(245,87,108,0.75)', 'rgba(79,172,254,0.75)',
  'rgba(67,233,123,0.75)',  'rgba(250,130,49,0.75)',  'rgba(165,94,234,0.75)',
  'rgba(252,92,101,0.75)',  'rgba(38,222,129,0.75)',  'rgba(102,126,234,0.55)',
  'rgba(245,87,108,0.55)',  'rgba(79,172,254,0.55)',  'rgba(67,233,123,0.55)'
];
const total = data.reduce((s, d) => s + d.value, 0);

{engine}'''
    )


def adapt_radar(config):
    """雷达图
    JSON data: { labels: [...], series: [{name, values, color?, fill?}] }
    """
    d = config['data']
    labels = json.dumps(d['labels'], ensure_ascii=False)
    series_data = d['series']
    default_colors = [
        ('rgba(102,126,234,0.8)', 'rgba(102,126,234,0.12)'),
        ('rgba(245,87,108,0.8)', 'rgba(245,87,108,0.12)'),
        ('rgba(67,233,123,0.8)', 'rgba(67,233,123,0.12)'),
        ('rgba(79,172,254,0.8)', 'rgba(79,172,254,0.12)'),
    ]
    for i, s in enumerate(series_data):
        if 'color' not in s:
            s['color'] = default_colors[i % len(default_colors)][0]
        if 'fill' not in s:
            s['fill'] = default_colors[i % len(default_colors)][1]
    series = json.dumps(series_data, ensure_ascii=False)

    # 读取 radar 模板引擎
    template = (TEMPLATES_DIR / 'radar.html').read_text(encoding='utf-8')
    engine_match = re.search(r'(function pt\(angle.*?)\s*</script>', template, re.DOTALL)
    engine = engine_match.group(1) if engine_match else ''
    # 修复：动态计算 max 值，替换模板中硬编码的 /100
    all_values = [v for s in series_data for v in s['values']]
    max_val = max(all_values) if all_values else 100
    engine = engine.replace('v / 100', f'v / {max_val}')

    axes = len(d['labels'])

    # 构建图例 HTML
    legend_items = ''.join(
        f'<div class="legend-item"><div class="legend-rect" style="background: {s["color"]}"></div>{s["name"]}</div>'
        for s in series_data
    )

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
{(LIB_DIR / 'base.css').read_text(encoding='utf-8')}
body {{ display: flex; flex-direction: column; align-items: center; }}
.title {{ font-size: 22px; font-weight: 700; color: #1a1a2e; margin-top: 28px; }}
.subtitle {{ font-size: 14px; color: #888; margin-top: 6px; }}
.legend {{ display: flex; gap: 28px; margin-top: 18px; }}
.legend-item {{ display: flex; align-items: center; gap: 8px; font-size: 14px; color: #555; }}
.legend-rect {{ width: 20px; height: 12px; border-radius: 3px; }}
.chart-wrap {{ margin-top: 12px; }}
</style>
</head>
<body class="auto-size">
  <div class="title">{config.get('title', '雷达图')}</div>
  <div class="subtitle">{config.get('subtitle', '')}</div>
  <div class="legend">{legend_items}</div>
  <div class="chart-wrap">
    <svg id="radar"></svg>
  </div>
<script>
{_safe_inline((LIB_DIR / 'utils.js').read_text(encoding='utf-8'))}
function setSvgSize(svg, w, h) {{
  svg.setAttribute('width', w);
  svg.setAttribute('height', h);
  svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
}}
</script>
<script>
const svg = document.getElementById('radar');
const axes = {axes};
const levels = 5;
const labels = {labels};
const series = {series};

// 动态计算尺寸：根据标签长度和轴数调整
const R = Math.min(220, 260);
const labelMargin = 80;  // 标签到雷达边缘的距离
const svgW = (R + labelMargin) * 2 + 60;
const svgH = (R + labelMargin) * 2 + 20;
const cx = svgW / 2, cy = svgH / 2;
setSvgSize(svg, svgW, svgH);

{engine}
</script>
</body>
</html>
'''
    return html


def adapt_heatmap(config):
    """热力图
    JSON data: { xLabels: [...], yLabels: [...], data: [[x,y,value], ...] }
    """
    d = config['data']
    x_labels = json.dumps(d['xLabels'], ensure_ascii=False)
    y_labels = json.dumps(d['yLabels'], ensure_ascii=False)
    raw_data = json.dumps(d['data'], ensure_ascii=False)

    return make_html(
        config.get('title', '热力图'),
        config.get('subtitle', ''),
        'hm', 'auto-size', [],
        f'''(function() {{
  const svg = document.getElementById('hm');
  const xLabels = {x_labels};
  const yLabels = {y_labels};
  const rawData = {raw_data};

  const cols = xLabels.length;
  const rows = yLabels.length;

  // 布局：自动计算格子尺寸
  const ox = 80, oy = 20;
  const maxGridW = 1000, maxGridH = 580;
  const gap = 2;
  const cellW = Math.min(Math.floor((maxGridW - gap * (cols - 1)) / cols), 50);
  const cellH = Math.min(Math.floor((maxGridH - gap * (rows - 1)) / rows), 70);
  const gridW = cols * (cellW + gap) - gap;
  const gridH = rows * (cellH + gap) - gap;

  // 数值范围
  const allVals = rawData.map(d => d[2]);
  const minVal = Math.min(...allVals);
  const maxVal = Math.max(...allVals);
  const valRange = maxVal - minVal || 1;

  // 色阶：蓝→红
  const colorStops = [
    [0,   [232,244,253]],
    [0.2, [179,217,247]],
    [0.4, [108,180,238]],
    [0.6, [58,143,214]],
    [0.75,[232,117,90]],
    [0.9, [217,69,53]],
    [1,   [185,28,28]]
  ];

  function valToColor(v) {{
    const t = (v - minVal) / valRange;
    let lo = colorStops[0], hi = colorStops[colorStops.length - 1];
    for (let i = 0; i < colorStops.length - 1; i++) {{
      if (t >= colorStops[i][0] && t <= colorStops[i + 1][0]) {{
        lo = colorStops[i]; hi = colorStops[i + 1]; break;
      }}
    }}
    const p = (t - lo[0]) / (hi[0] - lo[0] || 1);
    const r = Math.round(lo[1][0] + (hi[1][0] - lo[1][0]) * p);
    const g = Math.round(lo[1][1] + (hi[1][1] - lo[1][1]) * p);
    const b = Math.round(lo[1][2] + (hi[1][2] - lo[1][2]) * p);
    return 'rgb(' + r + ',' + g + ',' + b + ')';
  }}

  // 动态计算 SVG 尺寸，确保内容不溢出
  const xLabelH = 28;  // x 轴标签区域高度
  const legendPadR = 80;  // 色阶图例右侧留白
  const svgW = ox + gridW + legendPadR;
  const svgH = oy + gridH + xLabelH + 10;  // +10 底部留白
  setSvgSize(svg, svgW, svgH);

  // 画格子
  rawData.forEach(([xi, yi, v]) => {{
    const x = ox + xi * (cellW + gap);
    const y = oy + yi * (cellH + gap);
    svg.appendChild(el('rect', {{ x: x, y: y, width: cellW, height: cellH, rx: 3, fill: valToColor(v) }}));
    if (cellW >= 28 && cellH >= 20) {{
      const norm = (v - minVal) / valRange;
      svg.appendChild(el('text', {{ x: x + cellW/2, y: y + cellH/2 + 1,
        'text-anchor': 'middle', 'dominant-baseline': 'middle',
        'font-size': 12, 'font-weight': 500, fill: norm > 0.6 ? '#fff' : '#333' }}, String(v)));
    }}
  }});

  // X 轴标签
  xLabels.forEach((label, i) => {{
    svg.appendChild(el('text', {{ x: ox + i * (cellW + gap) + cellW/2, y: oy + gridH + 22,
      'text-anchor': 'middle', 'font-size': 12, fill: '#555' }}, label));
  }});

  // Y 轴标签
  yLabels.forEach((label, i) => {{
    svg.appendChild(el('text', {{ x: ox - 12, y: oy + i * (cellH + gap) + cellH/2 + 1,
      'text-anchor': 'end', 'dominant-baseline': 'middle',
      'font-size': 13, 'font-weight': 'bold', fill: '#555' }}, label));
  }});

  // 色阶图例
  const lgX = ox + gridW + 30, lgY = oy, lgW = 16, lgH = gridH;
  const defs = svg.querySelector('defs') || svg.appendChild(el('defs'));
  const grad = el('linearGradient', {{ id: 'hm-grad', x1: '0', y1: '1', x2: '0', y2: '0' }});
  colorStops.forEach(([pct, _]) => {{
    const stop = el('stop', {{ offset: (pct * 100) + '%', 'stop-color': valToColor(minVal + pct * valRange) }});
    grad.appendChild(stop);
  }});
  defs.appendChild(grad);
  svg.appendChild(el('rect', {{ x: lgX, y: lgY, width: lgW, height: lgH, rx: 4, fill: 'url(#hm-grad)' }}));
  [0, 0.5, 1].forEach(t => {{
    const v = Math.round(minVal + t * valRange);
    const y = lgY + lgH - t * lgH;
    svg.appendChild(el('text', {{ x: lgX + lgW + 8, y: y + 1,
      'dominant-baseline': 'middle', 'font-size': 12, fill: '#666' }}, String(v)));
  }});
}})();'''
    )


def adapt_scatter(config):
    """散点图/气泡图
    JSON data: { series: [{name, data: [[x, y], ...] 或 [[x, y, size], ...]}],
                 xLabel?: "X轴", yLabel?: "Y轴" }
    """
    d = config['data']
    series = json.dumps(d['series'], ensure_ascii=False)
    x_label = json.dumps(d.get('xLabel', ''), ensure_ascii=False)
    y_label = json.dumps(d.get('yLabel', ''), ensure_ascii=False)

    # 构建图例 HTML
    default_colors = [
        'rgba(102,126,234,0.5)', 'rgba(245,87,108,0.5)', 'rgba(67,233,123,0.5)',
        'rgba(79,172,254,0.5)', 'rgba(250,130,49,0.5)', 'rgba(165,94,234,0.5)'
    ]
    legend_items = ''
    for i, s in enumerate(d['series']):
        color = default_colors[i % len(default_colors)]
        legend_items += f'<div class="legend-item"><div class="legend-dot" style="background: {color}"></div>{s["name"]}</div>'

    lib_css = (LIB_DIR / 'base.css').read_text(encoding='utf-8')
    lib_utils = _safe_inline((LIB_DIR / 'utils.js').read_text(encoding='utf-8'))

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
{lib_css}
body {{ display: flex; flex-direction: column; align-items: center; }}
.title {{ font-size: 22px; font-weight: 700; color: #1a1a2e; margin-top: 28px; }}
.subtitle {{ font-size: 14px; color: #888; margin-top: 6px; }}
.legend {{ display: flex; gap: 28px; margin-top: 18px; }}
.legend-item {{ display: flex; align-items: center; gap: 8px; font-size: 14px; color: #555; }}
.legend-dot {{ width: 14px; height: 14px; border-radius: 50%; }}
.chart-wrap {{ margin-top: 16px; }}
</style>
</head>
<body class="auto-size">
  <div class="title">{config.get('title', '散点图')}</div>
  <div class="subtitle">{config.get('subtitle', '')}</div>
  <div class="legend">{legend_items}</div>
  <div class="chart-wrap">
    <svg id="scatter"></svg>
  </div>
<script>
{lib_utils}
function setSvgSize(svg, w, h) {{
  svg.setAttribute('width', w);
  svg.setAttribute('height', h);
  svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
}}
</script>
<script>
(function() {{
  const svg = document.getElementById('scatter');
  const series = {series};
  const xLabel = {x_label};
  const yLabel = {y_label};
  const colors = [
    ['rgba(102,126,234,0.35)', 'rgba(102,126,234,0.5)'],
    ['rgba(245,87,108,0.35)', 'rgba(245,87,108,0.5)'],
    ['rgba(67,233,123,0.35)', 'rgba(67,233,123,0.5)'],
    ['rgba(79,172,254,0.35)', 'rgba(79,172,254,0.5)'],
    ['rgba(250,130,49,0.35)', 'rgba(250,130,49,0.5)'],
    ['rgba(165,94,234,0.35)', 'rgba(165,94,234,0.5)']
  ];

  // 动态计算尺寸
  const totalPts = series.reduce((s, se) => s + se.data.length, 0);
  const padL = 80, padR = 40, padT = 10, padB = 70;
  const chartW = Math.max(600, Math.min(1000, totalPts * 15 + 400));
  const chartH = Math.max(400, Math.min(560, chartW * 0.55));
  const svgW = padL + chartW + padR;
  const svgH = padT + chartH + padB;
  setSvgSize(svg, svgW, svgH);

  // 数据范围
  const allPts = series.flatMap(s => s.data);
  const xMin = 0, xMax = Math.max(...allPts.map(p => p[0])) * 1.1;
  const yMin = 0, yMax = Math.max(...allPts.map(p => p[1])) * 1.1;

  function px(x) {{ return padL + (x / xMax) * chartW; }}
  function py(y) {{ return padT + chartH - (y / yMax) * chartH; }}

  // 背景 + 网格
  svg.appendChild(el('rect', {{ x: padL, y: padT, width: chartW, height: chartH, fill: '#f8f9fc', stroke: '#eef0f5' }}));
  for (let i = 0; i <= 5; i++) {{
    const y = padT + chartH - (i / 5) * chartH;
    const val = (yMax * i / 5);
    svg.appendChild(el('line', {{ x1: padL, y1: y, x2: padL + chartW, y2: y,
      stroke: '#e8e8ef', 'stroke-dasharray': '4,3' }}));
    svg.appendChild(el('text', {{ x: padL - 12, y: y + 4,
      'text-anchor': 'end', 'font-size': 12, fill: '#666' }},
      val >= 1000 ? (val/1000).toFixed(0) + 'k' : val.toFixed(0)));
  }}
  for (let i = 0; i <= 5; i++) {{
    const x = padL + (i / 5) * chartW;
    const val = (xMax * i / 5);
    svg.appendChild(el('line', {{ x1: x, y1: padT, x2: x, y2: padT + chartH,
      stroke: '#e8e8ef', 'stroke-dasharray': '4,3' }}));
    svg.appendChild(el('text', {{ x: x, y: padT + chartH + 20,
      'text-anchor': 'middle', 'font-size': 12, fill: '#666' }},
      val >= 1000 ? (val/1000).toFixed(0) + 'k' : val.toFixed(0)));
  }}

  // 坐标轴线
  svg.appendChild(el('line', {{ x1: padL, y1: padT + chartH, x2: padL + chartW, y2: padT + chartH, stroke: '#c0c3d0' }}));
  svg.appendChild(el('line', {{ x1: padL, y1: padT, x2: padL, y2: padT + chartH, stroke: '#c0c3d0' }}));

  // 轴标题
  if (xLabel) svg.appendChild(el('text', {{ x: padL + chartW/2, y: padT + chartH + 48,
    'text-anchor': 'middle', 'font-size': 14, 'font-weight': 'bold', fill: '#555' }}, xLabel));
  if (yLabel) {{
    const t = el('text', {{ x: 20, y: padT + chartH/2,
      'text-anchor': 'middle', 'font-size': 14, 'font-weight': 'bold', fill: '#555',
      transform: 'rotate(-90, 20, ' + (padT + chartH/2) + ')' }}, yLabel);
    svg.appendChild(t);
  }}

  // 散点
  series.forEach((s, si) => {{
    const [fill, stroke] = colors[si % colors.length];
    s.data.forEach(p => {{
      const r = p.length > 2 ? Math.max(Math.sqrt(p[2]) * 2.5, 4) : 6;
      svg.appendChild(el('circle', {{ cx: px(p[0]), cy: py(p[1]), r: r,
        fill: fill, stroke: stroke, 'stroke-width': 1 }}));
    }});
  }});
}})();
</script>
</body>
</html>
'''
    return html


def adapt_waterfall(config):
    """瀑布图
    JSON data: { items: [{name, value, type: 'start'|'increase'|'decrease'|'total'}] }
    """
    d = config['data']
    items = json.dumps(d['items'], ensure_ascii=False)

    # 构建图例 HTML
    legend_html = '''<div class="legend">
    <div class="legend-item"><div class="legend-dot" style="background: #3B82F6"></div>起始/合计</div>
    <div class="legend-item"><div class="legend-dot" style="background: #10B981"></div>增加</div>
    <div class="legend-item"><div class="legend-dot" style="background: #F43F5E"></div>减少</div>
  </div>'''

    lib_css = (LIB_DIR / 'base.css').read_text(encoding='utf-8')
    lib_utils = _safe_inline((LIB_DIR / 'utils.js').read_text(encoding='utf-8'))

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
{lib_css}
.title {{ font-size: 22px; font-weight: 700; color: #0F172A; margin-top: 28px; }}
.subtitle {{ font-size: 14px; color: #64748B; margin-top: 6px; }}
.legend {{ display: flex; gap: 32px; margin-top: 20px; }}
.legend-item {{ display: flex; align-items: center; gap: 8px; font-size: 14px; color: #64748B; }}
.legend-dot {{ width: 20px; height: 12px; border-radius: 3px; }}
.chart-wrap {{ margin-top: 16px; position: relative; }}
</style>
</head>
<body class="auto-size">
  <div class="title">{config.get('title', '瀑布图')}</div>
  <div class="subtitle">{config.get('subtitle', '')}</div>
  {legend_html}
  <div class="chart-wrap">
    <svg id="waterfall"></svg>
  </div>
<script>
{lib_utils}
function setSvgSize(svg, w, h) {{
  svg.setAttribute('width', w);
  svg.setAttribute('height', h);
  svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
}}
</script>
<script>
(function() {{
  const data = {items};
  const colors = {{ start: '#3B82F6', total: '#3B82F6', increase: '#10B981', decrease: '#F43F5E' }};
  const svg = document.getElementById('waterfall');

  // 计算累计值
  let running = 0;
  const bars = data.map(d => {{
    if (d.type === 'start') {{
      running = d.value;
      return {{ ...d, bottom: 0, top: d.value }};
    }} else if (d.type === 'total') {{
      return {{ ...d, bottom: 0, top: running, value: running }};
    }} else {{
      const prev = running;
      running += d.value;
      return d.value >= 0
        ? {{ ...d, bottom: prev, top: running }}
        : {{ ...d, bottom: running, top: prev }};
    }}
  }});

  // 动态计算尺寸
  const n = bars.length;
  const barGap = 16;
  const barW = Math.max(40, Math.min(80, 900 / n));
  const chartW = n * (barW + barGap) + barGap;
  const chartH = Math.min(Math.max(400, n * 40), 560);
  const chartLeft = 80, chartTop = 20;
  const chartRight = chartLeft + chartW;
  const chartBottom = chartTop + chartH;
  const svgW = chartRight + 40;
  const svgH = chartBottom + 70;
  setSvgSize(svg, svgW, svgH);

  const allVals = bars.flatMap(b => [b.bottom, b.top]);
  const dataMax = Math.ceil(Math.max(...allVals) / 1000) * 1000;
  const yRange = dataMax;

  function yPos(val) {{ return chartBottom - (val / yRange) * chartH; }}

  // 网格
  for (let i = 0; i <= 5; i++) {{
    const val = (yRange / 5) * i;
    const y = yPos(val);
    svg.appendChild(el('line', {{ x1: chartLeft, y1: y, x2: chartRight, y2: y,
      stroke: '#E2E8F0', 'stroke-dasharray': i === 0 ? 'none' : '4,4' }}));
    svg.appendChild(el('text', {{ x: chartLeft - 12, y: y + 4,
      'text-anchor': 'end', 'font-size': 13, fill: '#94A3B8' }}, val.toLocaleString()));
  }}

  // 柱子（n, barGap, barW 已在上方尺寸计算时定义）

  bars.forEach((b, i) => {{
    const x = chartLeft + barGap + i * (barW + barGap);
    const yTop = yPos(b.top);
    const yBottom = yPos(b.bottom);
    const h = Math.max(yBottom - yTop, 2);

    svg.appendChild(el('rect', {{ x: x, y: yTop, width: barW, height: h,
      rx: 4, fill: colors[b.type], opacity: 0.85 }}));

    // 数值标签
    let label;
    if (b.type === 'start' || b.type === 'total') label = b.value.toLocaleString();
    else if (b.type === 'decrease') label = b.value.toLocaleString();
    else label = '+' + b.value.toLocaleString();
    svg.appendChild(el('text', {{ x: x + barW/2, y: yTop - 8,
      'text-anchor': 'middle', 'font-size': 13, 'font-weight': 700, fill: colors[b.type] }}, label));

    // X 轴标签
    svg.appendChild(el('text', {{ x: x + barW/2, y: chartBottom + 24,
      'text-anchor': 'middle', 'font-size': 14, 'font-weight': 500, fill: '#1E293B' }}, b.name));

    // 连接线
    if (i < n - 1) {{
      const nextX = chartLeft + barGap + (i + 1) * (barW + barGap);
      const connY = b.type === 'decrease' ? yPos(b.bottom) : yPos(b.top);
      svg.appendChild(el('line', {{ x1: x + barW, y1: connY, x2: nextX, y2: connY,
        stroke: '#CBD5E1', 'stroke-width': 1.5, 'stroke-dasharray': '4,3' }}));
    }}
  }});
}})();
</script>
</body>
</html>
'''
    return html


def adapt_funnel(config):
    """漏斗图
    JSON data: { stages: [{name, value}] }
    """
    d = config['data']
    stages = json.dumps(d['stages'], ensure_ascii=False)

    return make_html(
        config.get('title', '漏斗图'),
        config.get('subtitle', ''),
        'funnel', 'auto-size', [],
        f'''(function() {{
  const data = {stages};
  const colors = ['#3B82F6', '#10B981', '#F59E0B', '#F43F5E', '#8B5CF6', '#06B6D4', '#F97316', '#64748B', '#10B981'];
  const svg = document.getElementById('funnel');

  const n = data.length;
  const gap = 4;
  const topY = 20;
  const maxWidth = Math.max(500, Math.min(800, n * 100 + 200));
  const minWidth = Math.max(120, maxWidth * 0.2);
  const stepH = Math.max(40, Math.min(80, 500 / n));
  const totalHeight = n * (stepH + gap) - gap;
  const svgW = maxWidth + 200;  // 左右留白给标签和转化率
  const svgH = topY + totalHeight + 30;
  const cx = svgW / 2;
  setSvgSize(svg, svgW, svgH);
  const maxVal = data[0].value;

  function widthFor(val) {{ return minWidth + (maxWidth - minWidth) * (val / maxVal); }}

  data.forEach((d, i) => {{
    const y = topY + i * (stepH + gap);
    const w1 = widthFor(d.value);
    const w2 = i < n - 1 ? widthFor(data[i + 1].value) : w1 * 0.7;
    const x1L = cx - w1/2, x1R = cx + w1/2;
    const x2L = cx - w2/2, x2R = cx + w2/2;

    svg.appendChild(el('path', {{
      d: 'M '+x1L+','+y+' L '+x1R+','+y+' L '+x2R+','+(y+stepH)+' L '+x2L+','+(y+stepH)+' Z',
      fill: colors[i], opacity: 0.85
    }}));

    svg.appendChild(el('text', {{ x: cx - maxWidth/2 - 20, y: y + stepH/2 + 5,
      'text-anchor': 'end', 'font-size': 14, 'font-weight': 600, fill: '#1E293B' }}, d.name));

    svg.appendChild(el('text', {{ x: cx, y: y + stepH/2 + 2,
      'text-anchor': 'middle', 'font-size': 16, 'font-weight': 700, fill: '#fff' }},
      d.value.toLocaleString()));

    const pct = (d.value / maxVal * 100).toFixed(1);
    svg.appendChild(el('text', {{ x: cx, y: y + stepH/2 + 18,
      'text-anchor': 'middle', 'font-size': 12, fill: 'rgba(255,255,255,0.85)' }}, pct + '%'));

    if (i < n - 1) {{
      const convRate = (data[i+1].value / d.value * 100).toFixed(1);
      const arrowY = y + stepH + gap/2;
      const ax = cx + maxWidth/2 + 30;
      svg.appendChild(el('path', {{
        d: 'M '+ax+','+(arrowY-10)+' L '+ax+','+(arrowY+10)+' M '+(ax-4)+','+(arrowY+6)+' L '+ax+','+(arrowY+10)+' L '+(ax+4)+','+(arrowY+6),
        fill: 'none', stroke: '#94A3B8', 'stroke-width': 2, 'stroke-linecap': 'round'
      }}));
      svg.appendChild(el('text', {{ x: ax + 16, y: arrowY + 5,
        'text-anchor': 'start', 'font-size': 13, 'font-weight': 600, fill: '#64748B' }}, convRate + '%'));
    }}
  }});
}})();'''
    )


def adapt_treemap(config):
    """矩形树图（Treemap）
    JSON: { title, subtitle?, data: { name, children: [{name, value, children?}] } }
    """
    d = config['data']
    root_json = json.dumps(d.get('root', d), ensure_ascii=False)

    template_path = TEMPLATES_DIR / 'treemap.html'
    template = template_path.read_text(encoding='utf-8')

    # 提取 JS 渲染引擎（配色到图例之间的代码）
    import re as _re
    js_match = _re.search(r'// ========== 配色 ==========(.*?)// ========== 图例 ==========', template, _re.DOTALL)
    engine_js = js_match.group(0) if js_match else ''

    # 提取图例代码
    legend_match = _re.search(r'// ========== 图例 ==========(.*?)\}\)\(\);', template, _re.DOTALL)
    legend_js = '// ========== 图例 ==========' + legend_match.group(1) if legend_match else ''

    return make_html(
        config.get('title', 'Treemap'),
        config.get('subtitle', ''),
        'canvas', 'auto-size', [],
        f'''(function() {{
  var svg = document.getElementById('canvas');
  var SANS = "-apple-system, system-ui, 'PingFang SC', sans-serif";
  var data = {root_json};
  {_safe_inline(engine_js)}
  {_safe_inline(legend_js)}
}})();'''
    )


def adapt_combo(config):
    """柱线混合图（Combo Chart）
    JSON: { title, subtitle?, data: { categories, series: [{name, type:'bar'|'line', values, yAxis?, format?}] } }
    """
    d = config['data']
    data_json = json.dumps(d, ensure_ascii=False)

    template_path = TEMPLATES_DIR / 'combo.html'
    template = template_path.read_text(encoding='utf-8')

    # 提取配色到图例之间的完整渲染逻辑
    import re as _re
    js_match = _re.search(r'// ========== 配色 ==========(.*?)\}\)\(\);', template, _re.DOTALL)
    engine_js = js_match.group(1) if js_match else ''

    return make_html(
        config.get('title', 'Combo Chart'),
        config.get('subtitle', ''),
        'canvas', 'auto-size', [],
        f'''(function() {{
  var svg = document.getElementById('canvas');
  var SANS = "-apple-system, system-ui, 'PingFang SC', sans-serif";
  var data = {data_json};
  // ========== 配色 ==========
  {_safe_inline(engine_js)}
}})();'''
    )


# ─── 适配器注册 ───

ADAPTERS = {
    'bar': adapt_bar,
    'line': adapt_line,
    'pie': adapt_pie,
    'radar': adapt_radar,
    'funnel': adapt_funnel,
    'heatmap': adapt_heatmap,
    'scatter': adapt_scatter,
    'waterfall': adapt_waterfall,
    'treemap': adapt_treemap,
    'combo': adapt_combo,
}


def list_types():
    return sorted(ADAPTERS.keys())


# ─── 主程序 ───

def main():
    parser = argparse.ArgumentParser(
        description='Diagram Bridge — JSON → PNG/HTML',
        epilog=f'支持图表类型: {", ".join(list_types())}'
    )
    parser.add_argument('--type', '-t', help='图表类型（如 bar, pie, radar）')
    parser.add_argument('--config', '-c', help='JSON 配置文件路径（省略则从 stdin 读取）')
    parser.add_argument('--output', '-o', required=True, help='输出文件路径（.png 或 .html）')
    parser.add_argument('--format', '-f', choices=['png', 'html'], help='输出格式（默认从扩展名推断）')
    parser.add_argument('--scale', '-s', type=int, default=2, help='PNG 缩放倍数（默认 2x）')
    args = parser.parse_args()

    # 读取 JSON 配置
    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = json.load(sys.stdin)

    # 图表类型
    chart_type = args.type or config.get('type')
    if not chart_type:
        print(f'Error: 需要指定图表类型 --type，支持: {", ".join(list_types())}')
        sys.exit(1)

    if chart_type not in ADAPTERS:
        print(f'Error: 不支持的图表类型 "{chart_type}"，支持: {", ".join(list_types())}')
        sys.exit(1)

    # 输出格式
    output_path = Path(args.output).resolve()
    fmt = args.format or ('html' if output_path.suffix == '.html' else 'png')

    # 生成 HTML
    html = ADAPTERS[chart_type](config)

    if fmt == 'html':
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding='utf-8')
        size_kb = os.path.getsize(output_path) / 1024
        print(f'{output_path.name} ({size_kb:.0f}KB, self-contained HTML)')
    else:
        # 写临时 HTML → Playwright 截图 → PNG
        import threading
        import http.server
        import socketserver
        from playwright.sync_api import sync_playwright

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_html = Path(tmpdir) / 'chart.html'
            tmp_html.write_text(html, encoding='utf-8')

            # 启动 HTTP 服务
            os.chdir(tmpdir)
            handler = http.server.SimpleHTTPRequestHandler
            handler.log_message = lambda *a: None
            socketserver.TCPServer.allow_reuse_address = True
            httpd = socketserver.TCPServer(('', 18773), handler)
            thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            thread.start()

            output_path.parent.mkdir(parents=True, exist_ok=True)

            with sync_playwright() as p:
                browser = p.chromium.launch()
                context = browser.new_context(device_scale_factor=args.scale)
                page = context.new_page()

                page.goto('http://localhost:18773/chart.html',
                          wait_until='domcontentloaded', timeout=15000)
                page.wait_for_timeout(800)

                # ELKjs 等待
                try:
                    page.wait_for_function(
                        '''() => {
                            const svg = document.querySelector('svg');
                            if (!svg) return true;
                            return svg.querySelectorAll('rect, path, line, circle').length > 3;
                        }''',
                        timeout=5000
                    )
                except:
                    pass

                page.locator('body').screenshot(path=str(output_path), type='png')
                browser.close()

            httpd.shutdown()

        size_kb = os.path.getsize(output_path) / 1024
        print(f'{output_path.name} ({size_kb:.0f}KB, {args.scale}x)')


if __name__ == '__main__':
    main()
