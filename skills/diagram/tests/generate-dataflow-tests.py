"""生成 dataflow L1-L4 测试 HTML 文件（完整 HTML 替换方式）"""

from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / "docs" / "assets" / "diagram" / "tests" / "html"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# dataflow 模板使用 HTML head（含 title/subtitle）+ script 结构
# 数据与引擎在同一 script 内，采用完整 HTML 方式生成每个级别

def make_html(title, subtitle, script_body):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="lib/base.css">
<style>
  body {{
    padding: 24px;
    -webkit-font-smoothing: antialiased;
  }}
  .title {{
    font-size: 22px;
    font-weight: 700;
    color: #1a1a2e;
    text-align: center;
    margin-bottom: 4px;
  }}
  .subtitle {{
    font-size: 14px;
    color: #888;
    text-align: center;
    margin-bottom: 24px;
  }}
  .diagram-wrap {{
    display: flex;
    justify-content: center;
  }}
</style>
</head>
<body>
  <div class="title">{title}</div>
  <div class="subtitle">{subtitle}</div>
  <div class="diagram-wrap">
    <svg id="df"></svg>
  </div>

<script src="lib/utils.js"></script>
<script>
{script_body}
</script>
</body>
</html>
'''


# 渲染引擎（从 "布局计算" 开始到文件末尾，所有级别共享）
ENGINE = r'''// ─── 布局计算 ───
// 列定义：each column has nodes and a group label
const columns = [
  { label: 'Sources',   nodes: sources,    style: 'src' },
  { label: 'Extract',   nodes: extract,    style: 'proc' },
  { label: 'Transform', nodes: transform,  style: 'proc' },
  { label: 'Load',      nodes: load,       style: 'proc' },
  { label: 'Destinations', nodes: destinations, style: 'dst' },
];

// 计算每列分组框尺寸
const maxRows = Math.max(...columns.map(c => c.nodes.length));
const maxGroupH = groupPadTop + maxRows * nodeH + (maxRows - 1) * rowGap + groupPadBot;
const groupW = nodeW + groupPadX * 2;

// 节点位置映射
const nodePos = {}; // id → { x, y, w, h }

// x 起始偏移
let curX = 0;
const groupRects = [];

columns.forEach((col, ci) => {
  const gx = curX;
  const rows = col.nodes.length;
  const groupH = groupPadTop + rows * nodeH + (rows - 1) * rowGap + groupPadBot;
  // 垂直居中对齐到最高列
  const gy = (maxGroupH - groupH) / 2;

  groupRects.push({ x: gx, y: gy, w: groupW, h: groupH, label: col.label, style: col.style });

  col.nodes.forEach((node, ri) => {
    const nx = gx + groupPadX;
    const ny = gy + groupPadTop + ri * (nodeH + rowGap);
    nodePos[node.id] = { x: nx, y: ny, w: nodeW, h: nodeH, node };
  });

  curX += groupW + colGap;
});

const totalW = curX - colGap;

// 监控区域
const monW = 160;
const monGap = 24;
const monTotalW = monitors.length * monW + (monitors.length - 1) * monGap;
const monX0 = (totalW - monTotalW) / 2;
const monY = maxGroupH + monitorY;

monitors.forEach((m, i) => {
  const mx = monX0 + i * (monW + monGap);
  nodePos[m.id] = { x: mx, y: monY, w: monW, h: nodeH, node: m };
});

const totalH = monitors.length > 0 ? monY + nodeH + 20 : maxGroupH + 20;

// 设置 SVG 尺寸
svg.setAttribute('width', totalW);
svg.setAttribute('height', totalH);
svg.setAttribute('viewBox', `0 0 ${totalW} ${totalH}`);

// ─── 辅助函数 ───
function el(tag, attrs) {
  const e = document.createElementNS(svgNS, tag);
  for (const [k, v] of Object.entries(attrs || {})) e.setAttribute(k, v);
  return e;
}

// ─── 箭头 marker ───
const defs = el('defs');
const marker = el('marker', {
  id: 'arrowhead', markerWidth: '8', markerHeight: '6',
  refX: '8', refY: '3', orient: 'auto', markerUnits: 'strokeWidth'
});
const arrowPath = el('polygon', { points: '0 0, 8 3, 0 6', fill: C.arrow });
marker.appendChild(arrowPath);
defs.appendChild(marker);
svg.appendChild(defs);

// ─── 1. 画连线（先画，在底层） ───
const lineGroup = el('g', { class: 'lines' });
svg.appendChild(lineGroup);

links.forEach(link => {
  const from = nodePos[link.from];
  const to = nodePos[link.to];
  if (!from || !to) return;

OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / 'docs' / 'assets' / 'diagram' / 'tests-html'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

  const x1 = from.x + from.w;
  const y1 = from.y + from.h / 2;
  const x2 = to.x;
  const y2 = to.y + to.h / 2;

  const dx = x2 - x1;
  const cp = dx * 0.45;

  const path = el('path', {
    d: `M ${x1},${y1} C ${x1 + cp},${y1} ${x2 - cp},${y2} ${x2},${y2}`,
    fill: 'none',
    stroke: C.arrow,
    'stroke-width': '1.5',
    'marker-end': 'url(#arrowhead)',
  });
  lineGroup.appendChild(path);

  // 数据标签
  if (link.label) {
    const mx = (x1 + x2) / 2;
    const my = (y1 + y2) / 2;

    // 背景
    const bg = el('rect', {
      x: mx - 30, y: my - 10, width: 60, height: 16, rx: 3,
      fill: '#ffffff', stroke: 'none',
    });
    lineGroup.appendChild(bg);

    const txt = el('text', {
      x: mx, y: my - 1,
      'text-anchor': 'middle', 'dominant-baseline': 'middle',
      'font-size': '10', fill: C.labelText,
      'font-family': "-apple-system, system-ui, 'PingFang SC', sans-serif",
    });
    txt.textContent = link.label;
    lineGroup.appendChild(txt);
  }
});

// ─── 2. 画分组框 ───
const nodeGroup = el('g', { class: 'nodes' });
svg.appendChild(nodeGroup);

groupRects.forEach(gr => {
  const colors = {
    src:  { bg: C.srcBg,  border: C.srcBorder },
    proc: { bg: C.procBg, border: C.procBorder },
    dst:  { bg: C.dstBg,  border: C.dstBorder },
  };
  const c = colors[gr.style];

  const rect = el('rect', {
    x: gr.x, y: gr.y, width: gr.w, height: gr.h, rx: 10,
    fill: c.bg, stroke: c.border, 'stroke-width': '1.5',
  });
  nodeGroup.appendChild(rect);

  const label = el('text', {
    x: gr.x + gr.w / 2, y: gr.y + 22,
    'text-anchor': 'middle', 'dominant-baseline': 'middle',
    'font-size': '12', 'font-weight': '600', fill: C.groupLabel,
    'font-family': "-apple-system, system-ui, 'PingFang SC', sans-serif",
  });
  label.textContent = gr.label;
  nodeGroup.appendChild(label);
});

// ─── 3. 画节点 ───
function drawNode(id, styleName) {
  const pos = nodePos[id];
  if (!pos) return;
  const n = pos.node;

  const colors = {
    src:  { bg: '#ffffff', border: C.srcBorder, text: '#5B21B6' },
    proc: { bg: '#ffffff', border: C.procBorder, text: '#1E40AF' },
    dst:  { bg: '#ffffff', border: C.dstBorder, text: '#065F46' },
    mon:  { bg: '#ffffff', border: C.monBorder, text: '#92400E' },
  };
  const c = colors[styleName];

  const rect = el('rect', {
    x: pos.x, y: pos.y, width: pos.w, height: pos.h, rx: nodeR,
    fill: c.bg, stroke: c.border, 'stroke-width': '1.5',
  });
  nodeGroup.appendChild(rect);

  // 主标签
  const labelY = n.sub ? pos.y + pos.h / 2 - 5 : pos.y + pos.h / 2;
  const txt = el('text', {
    x: pos.x + pos.w / 2, y: labelY,
    'text-anchor': 'middle', 'dominant-baseline': 'middle',
    'font-size': '13', 'font-weight': '600', fill: c.text,
    'font-family': "-apple-system, system-ui, 'PingFang SC', sans-serif",
  });
  txt.textContent = n.label;
  nodeGroup.appendChild(txt);

  // 副标签
  if (n.sub) {
    const sub = el('text', {
      x: pos.x + pos.w / 2, y: labelY + 14,
      'text-anchor': 'middle', 'dominant-baseline': 'middle',
      'font-size': '10', fill: C.labelText,
      'font-family': "-apple-system, system-ui, 'PingFang SC', sans-serif",
    });
    sub.textContent = n.sub;
    nodeGroup.appendChild(sub);
  }
}

sources.forEach(n => drawNode(n.id, 'src'));
extract.forEach(n => drawNode(n.id, 'proc'));
transform.forEach(n => drawNode(n.id, 'proc'));
load.forEach(n => drawNode(n.id, 'proc'));
destinations.forEach(n => drawNode(n.id, 'dst'));

// 基础设施层容器（仅在有监控节点时绘制）
if (monitors.length > 0) {
  const monContX = groupRects[0].x;
  const monContW = groupRects[groupRects.length - 1].x + groupRects[groupRects.length - 1].w - monContX;
  const monContY = monY - 28;
  const monContH = nodeH + 44;
  nodeGroup.appendChild(el('rect', {
    x: monContX, y: monContY, width: monContW, height: monContH,
    rx: '8', fill: C.monBg, stroke: C.monBorder, 'stroke-width': '1', 'stroke-opacity': '0.3'
  }));
  const monLbl = el('text', {
    x: monContX + 12, y: monContY + 14, 'font-size': '10', 'font-weight': '600',
    fill: '#92400E', 'text-anchor': 'start',
    'font-family': "-apple-system, system-ui, 'PingFang SC', sans-serif"
  });
  monLbl.textContent = '基础设施层 · 覆盖以上全部阶段';
  nodeGroup.appendChild(monLbl);

  monitors.forEach(n => drawNode(n.id, 'mon'));
}'''


# 公共布局参数和颜色方案
LAYOUT_AND_COLORS = '''const svg = document.getElementById('df');

// ─── 布局参数 ───
const nodeW = 140, nodeH = 38, nodeR = 8;
const colGap = 90;   // 列间距
const rowGap = 14;    // 同列节点间距
const groupPadX = 16, groupPadTop = 34, groupPadBot = 14;
const monitorY = 40;  // 监控区域与主流程的间距

// ─── 颜色方案 ───
const C = {
  srcBg: '#F5F3FF', srcBorder: '#A78BFA',
  procBg: '#EFF6FF', procBorder: '#93C5FD',
  dstBg: '#ECFDF5', dstBorder: '#6EE7B7',
  monBg: '#FFFBEB', monBorder: '#FCD34D',
  arrow: '#94A3B8',
  groupLabel: '#64748B',
  nodeText: '#1E293B',
  labelText: '#64748B',
};

'''


# ── L1: 最小化 ─ 2 源, 2 Extract, 1 Transform, 1 Load, 2 目标, 0 监控 ──
L1_DATA = '''// ─── 数据定义 ───
const sources = [
  { id: 'src_api',   label: 'REST API' },
  { id: 'src_db',    label: 'PostgreSQL' },
];

const extract = [
  { id: 'ext_http',   label: 'HTTP Poller' },
  { id: 'ext_cdc',    label: 'CDC Connector' },
];

const transform = [
  { id: 'tfm_clean',  label: '数据清洗' },
];

const load = [
  { id: 'ld_writer',  label: 'Batch Writer' },
];

const destinations = [
  { id: 'dst_dw',   label: '数据仓库', sub: 'OLAP' },
  { id: 'dst_lake', label: '数据湖', sub: '归档' },
];

const monitors = [];

// ─── 连线定义 ───
const links = [
  { from: 'src_api', to: 'ext_http',   label: 'JSON' },
  { from: 'src_db',  to: 'ext_cdc',    label: 'WAL' },
  { from: 'ext_http', to: 'tfm_clean', label: '' },
  { from: 'ext_cdc',  to: 'tfm_clean', label: '' },
  { from: 'tfm_clean', to: 'ld_writer', label: '' },
  { from: 'ld_writer', to: 'dst_dw',   label: '批量写入' },
  { from: 'ld_writer', to: 'dst_lake', label: 'Parquet' },
];

'''


# ── L2: 默认模板数据 ──
L2_DATA = '''// ─── 数据定义 ───
const sources = [
  { id: 'src_mysql',   label: 'MySQL 业务库' },
  { id: 'src_mongo',   label: 'MongoDB 日志库' },
  { id: 'src_kafka',   label: 'Kafka 实时流' },
  { id: 'src_csv',     label: 'CSV 文件上传' },
];

const extract = [
  { id: 'ext_cdc',      label: 'Debezium CDC' },
  { id: 'ext_logstash', label: 'Logstash' },
  { id: 'ext_consumer', label: 'Kafka Consumer' },
  { id: 'ext_parser',   label: 'File Parser' },
];

const transform = [
  { id: 'tfm_clean',  label: '数据清洗' },
  { id: 'tfm_map',    label: '字段映射' },
  { id: 'tfm_agg',    label: '数据聚合' },
];

const load = [
  { id: 'ld_ch',  label: 'ClickHouse Writer' },
  { id: 'ld_es',  label: 'Elasticsearch Writer' },
  { id: 'ld_s3',  label: 'S3 Writer' },
];

const destinations = [
  { id: 'dst_ch',  label: 'ClickHouse', sub: 'OLAP 分析' },
  { id: 'dst_es',  label: 'Elasticsearch', sub: '全文搜索' },
  { id: 'dst_s3',  label: 'S3', sub: '数据归档' },
];

const monitors = [
  { id: 'mon_airflow', label: 'Airflow 调度' },
  { id: 'mon_grafana', label: 'Grafana 监控' },
];

// ─── 连线定义 ───
const links = [
  { from: 'src_mysql', to: 'ext_cdc',      label: 'binlog' },
  { from: 'src_mongo', to: 'ext_logstash',  label: 'JSON docs' },
  { from: 'src_kafka', to: 'ext_consumer',  label: 'events' },
  { from: 'src_csv',   to: 'ext_parser',    label: 'CSV files' },
  { from: 'ext_cdc',      to: 'tfm_clean', label: '' },
  { from: 'ext_logstash', to: 'tfm_clean', label: '' },
  { from: 'ext_consumer', to: 'tfm_clean', label: '' },
  { from: 'ext_parser',   to: 'tfm_clean', label: '' },
  { from: 'tfm_clean', to: 'tfm_map', label: '' },
  { from: 'tfm_map',   to: 'tfm_agg', label: '' },
  { from: 'tfm_agg', to: 'ld_ch',  label: '' },
  { from: 'tfm_agg', to: 'ld_es',  label: '' },
  { from: 'tfm_agg', to: 'ld_s3',  label: '' },
  { from: 'ld_ch',  to: 'dst_ch',  label: 'OLAP 数据' },
  { from: 'ld_es',  to: 'dst_es',  label: '索引文档' },
  { from: 'ld_s3',  to: 'dst_s3',  label: 'Parquet' },
];

'''


# ── L3: 复杂 ─ 5 源, 5 Extract, 4 Transform, 4 Load, 4 目标, 3 监控 ──
L3_DATA = '''// ─── 数据定义 ───
const sources = [
  { id: 'src_mysql',   label: 'MySQL 主库' },
  { id: 'src_pg',      label: 'PostgreSQL' },
  { id: 'src_mongo',   label: 'MongoDB' },
  { id: 'src_kafka',   label: 'Kafka 集群' },
  { id: 'src_s3',      label: 'S3 Raw Data' },
];

const extract = [
  { id: 'ext_cdc1',     label: 'MySQL CDC' },
  { id: 'ext_cdc2',     label: 'PG CDC' },
  { id: 'ext_logstash', label: 'Logstash' },
  { id: 'ext_consumer', label: 'Kafka Consumer' },
  { id: 'ext_s3reader', label: 'S3 Reader' },
];

const transform = [
  { id: 'tfm_validate', label: '数据校验' },
  { id: 'tfm_clean',    label: '数据清洗' },
  { id: 'tfm_enrich',   label: '数据补全' },
  { id: 'tfm_agg',      label: '聚合计算' },
];

const load = [
  { id: 'ld_ch',     label: 'ClickHouse Writer' },
  { id: 'ld_es',     label: 'ES Writer' },
  { id: 'ld_hive',   label: 'Hive Writer' },
  { id: 'ld_redis',  label: 'Redis Writer' },
];

const destinations = [
  { id: 'dst_ch',    label: 'ClickHouse', sub: 'OLAP 分析' },
  { id: 'dst_es',    label: 'Elasticsearch', sub: '日志搜索' },
  { id: 'dst_hive',  label: 'Hive', sub: '离线数仓' },
  { id: 'dst_redis', label: 'Redis', sub: '实时缓存' },
];

const monitors = [
  { id: 'mon_airflow',  label: 'Airflow 调度' },
  { id: 'mon_grafana',  label: 'Grafana 监控' },
  { id: 'mon_alertmgr', label: 'AlertManager' },
];

// ─── 连线定义 ───
const links = [
  { from: 'src_mysql', to: 'ext_cdc1',     label: 'binlog' },
  { from: 'src_pg',    to: 'ext_cdc2',     label: 'WAL' },
  { from: 'src_mongo', to: 'ext_logstash', label: 'oplog' },
  { from: 'src_kafka', to: 'ext_consumer', label: 'events' },
  { from: 'src_s3',    to: 'ext_s3reader', label: 'CSV/JSON' },
  { from: 'ext_cdc1',     to: 'tfm_validate', label: '' },
  { from: 'ext_cdc2',     to: 'tfm_validate', label: '' },
  { from: 'ext_logstash', to: 'tfm_validate', label: '' },
  { from: 'ext_consumer', to: 'tfm_validate', label: '' },
  { from: 'ext_s3reader', to: 'tfm_validate', label: '' },
  { from: 'tfm_validate', to: 'tfm_clean',  label: '' },
  { from: 'tfm_clean',    to: 'tfm_enrich', label: '' },
  { from: 'tfm_enrich',   to: 'tfm_agg',    label: '' },
  { from: 'tfm_agg', to: 'ld_ch',    label: '' },
  { from: 'tfm_agg', to: 'ld_es',    label: '' },
  { from: 'tfm_agg', to: 'ld_hive',  label: '' },
  { from: 'tfm_agg', to: 'ld_redis', label: '' },
  { from: 'ld_ch',    to: 'dst_ch',    label: 'OLAP' },
  { from: 'ld_es',    to: 'dst_es',    label: '索引' },
  { from: 'ld_hive',  to: 'dst_hive',  label: 'ORC' },
  { from: 'ld_redis', to: 'dst_redis', label: 'K-V' },
];

'''


# ── L4: 压力测试 ─ 6 源, 6 Extract, 5 Transform, 5 Load, 5 目标, 4 监控 ──
L4_DATA = '''// ─── 数据定义 ───
const sources = [
  { id: 'src_mysql',    label: 'MySQL 业务库' },
  { id: 'src_pg',       label: 'PostgreSQL 分析库' },
  { id: 'src_mongo',    label: 'MongoDB 日志库' },
  { id: 'src_kafka',    label: 'Kafka 实时事件流' },
  { id: 'src_s3',       label: 'S3 原始文件' },
  { id: 'src_api',      label: '第三方 API 数据' },
];

const extract = [
  { id: 'ext_cdc_mysql',  label: 'MySQL CDC' },
  { id: 'ext_cdc_pg',     label: 'PG CDC' },
  { id: 'ext_logstash',   label: 'Logstash Agent' },
  { id: 'ext_consumer',   label: 'Kafka Consumer Group' },
  { id: 'ext_s3reader',   label: 'S3 Batch Reader' },
  { id: 'ext_http',       label: 'HTTP Connector' },
];

const transform = [
  { id: 'tfm_validate',   label: '数据质量校验' },
  { id: 'tfm_dedup',      label: '去重处理' },
  { id: 'tfm_clean',      label: '清洗 & 标准化' },
  { id: 'tfm_enrich',     label: '数据补全 & 关联' },
  { id: 'tfm_agg',        label: '多维聚合计算' },
];

const load = [
  { id: 'ld_ch',       label: 'ClickHouse Writer' },
  { id: 'ld_es',       label: 'Elasticsearch Writer' },
  { id: 'ld_hive',     label: 'Hive/Iceberg Writer' },
  { id: 'ld_redis',    label: 'Redis Cache Writer' },
  { id: 'ld_pg_dw',    label: 'PG DW Writer' },
];

const destinations = [
  { id: 'dst_ch',      label: 'ClickHouse', sub: 'OLAP 实时分析' },
  { id: 'dst_es',      label: 'Elasticsearch', sub: '全文检索' },
  { id: 'dst_hive',    label: 'Hive/Iceberg', sub: '离线数仓' },
  { id: 'dst_redis',   label: 'Redis Cluster', sub: '实时缓存' },
  { id: 'dst_pg_dw',   label: 'PG 数据仓库', sub: '报表分析' },
];

const monitors = [
  { id: 'mon_airflow',   label: 'Airflow 调度中心' },
  { id: 'mon_grafana',   label: 'Grafana 监控面板' },
  { id: 'mon_alertmgr',  label: 'AlertManager 告警' },
  { id: 'mon_datadog',   label: 'DataDog APM' },
];

// ─── 连线定义 ───
const links = [
  { from: 'src_mysql',  to: 'ext_cdc_mysql', label: 'binlog' },
  { from: 'src_pg',     to: 'ext_cdc_pg',    label: 'WAL log' },
  { from: 'src_mongo',  to: 'ext_logstash',  label: 'oplog' },
  { from: 'src_kafka',  to: 'ext_consumer',  label: 'events' },
  { from: 'src_s3',     to: 'ext_s3reader',  label: 'CSV/Parquet' },
  { from: 'src_api',    to: 'ext_http',      label: 'REST/JSON' },
  { from: 'ext_cdc_mysql', to: 'tfm_validate', label: '' },
  { from: 'ext_cdc_pg',   to: 'tfm_validate', label: '' },
  { from: 'ext_logstash',  to: 'tfm_validate', label: '' },
  { from: 'ext_consumer',  to: 'tfm_validate', label: '' },
  { from: 'ext_s3reader',  to: 'tfm_validate', label: '' },
  { from: 'ext_http',      to: 'tfm_validate', label: '' },
  { from: 'tfm_validate', to: 'tfm_dedup',  label: '' },
  { from: 'tfm_dedup',    to: 'tfm_clean',  label: '' },
  { from: 'tfm_clean',    to: 'tfm_enrich', label: '' },
  { from: 'tfm_enrich',   to: 'tfm_agg',    label: '' },
  { from: 'tfm_agg', to: 'ld_ch',    label: '' },
  { from: 'tfm_agg', to: 'ld_es',    label: '' },
  { from: 'tfm_agg', to: 'ld_hive',  label: '' },
  { from: 'tfm_agg', to: 'ld_redis', label: '' },
  { from: 'tfm_agg', to: 'ld_pg_dw', label: '' },
  { from: 'ld_ch',    to: 'dst_ch',    label: 'OLAP' },
  { from: 'ld_es',    to: 'dst_es',    label: '索引' },
  { from: 'ld_hive',  to: 'dst_hive',  label: 'ORC/Parquet' },
  { from: 'ld_redis', to: 'dst_redis', label: 'K-V' },
  { from: 'ld_pg_dw', to: 'dst_pg_dw', label: 'SQL' },
];

'''


# 各级别标题
titles = {
    'L1': ('简易数据管道', '最小化 ETL 流程示例'),
    'L2': ('数据处理管道 — ETL Pipeline', '从多源数据采集到多目标写入的完整数据流'),
    'L3': ('企业级数据集成平台', '多源异构数据采集 → 质量校验 → 多目标分发'),
    'L4': ('全域数据中台 — 数据管道架构', '6 数据源 × 5 阶段处理 × 5 目标写入 × 全链路监控'),
}

data_blocks = {
    'L1': L1_DATA,
    'L2': L2_DATA,
    'L3': L3_DATA,
    'L4': L4_DATA,
}

for level in ['L1', 'L2', 'L3', 'L4']:
    title, subtitle = titles[level]
    script_body = LAYOUT_AND_COLORS + data_blocks[level] + ENGINE
    content = make_html(title, subtitle, script_body)
    filename = f'dataflow-{level}.html'
    with open(str(OUTPUT_DIR / filename), 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
