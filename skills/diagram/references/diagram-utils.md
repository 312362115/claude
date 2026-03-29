# 图表公共工具库（diagram-utils）

> 所有动态布局模板共享的标准函数集。生成图表时内联到 HTML `<script>` 中。

---

## 使用方式

不是独立 JS 文件。Claude 生成图表时，将所需函数直接内联到 HTML 的 `<script>` 标签中。按需引入——只嵌入当前图表用到的函数。

---

## 一、SVG 基础工具

```javascript
var NS = 'http://www.w3.org/2000/svg';

// 创建 SVG 元素
function el(tag, attrs) {
  var e = document.createElementNS(NS, tag);
  if (attrs) for (var k in attrs) e.setAttribute(k, attrs[k]);
  return e;
}

// 创建文本元素
function txt(str, x, y, opts) {
  opts = opts || {};
  var t = el('text', {
    x: x, y: y,
    'font-size': opts.size || 13,
    'font-weight': opts.weight || 'normal',
    'font-family': opts.font || "-apple-system, system-ui, 'PingFang SC', sans-serif",
    fill: opts.color || '#334155',
    'text-anchor': opts.anchor || 'middle',
    'dominant-baseline': opts.baseline || 'central'
  });
  t.textContent = str;
  return t;
}
```

---

## 二、文字与尺寸计算

```javascript
// 估算文字渲染宽度（中英文混排）
// 中文字符按 fontSize 宽度，英文按 0.6 * fontSize
function measureText(str, fontSize) {
  var w = 0;
  for (var i = 0; i < str.length; i++) {
    w += str.charCodeAt(i) > 127 ? fontSize : fontSize * 0.6;
  }
  return w;
}

// 根据文字内容计算节点宽高
// opts: { padX, padY, fontSize, minW, minH, maxW }
function calcNodeSize(label, opts) {
  opts = opts || {};
  var padX = opts.padX || 16;
  var padY = opts.padY || 10;
  var fontSize = opts.fontSize || 13;
  var w = measureText(label, fontSize) + padX * 2;
  var h = fontSize + padY * 2;
  return {
    w: Math.min(Math.max(w, opts.minW || 80), opts.maxW || 300),
    h: Math.max(h, opts.minH || 32)
  };
}

// 多行文字：计算最宽行的宽度和总高度
function calcMultilineSize(lines, opts) {
  opts = opts || {};
  var fontSize = opts.fontSize || 13;
  var lineH = opts.lineHeight || fontSize * 1.6;
  var padX = opts.padX || 16;
  var padY = opts.padY || 10;
  var maxW = 0;
  lines.forEach(function(line) {
    var w = measureText(line, fontSize);
    if (w > maxW) maxW = w;
  });
  return {
    w: maxW + padX * 2,
    h: lines.length * lineH + padY * 2
  };
}
```

---

## 三、碰撞检测

```javascript
// 检测两个矩形是否重叠（含可选间距）
function isOverlap(a, b, gap) {
  gap = gap || 0;
  return !(a.x + a.w + gap <= b.x ||
           b.x + b.w + gap <= a.x ||
           a.y + a.h + gap <= b.y ||
           b.y + b.h + gap <= a.y);
}

// 检测节点数组中的所有重叠对
// 每个节点需有 { x, y, w, h } 属性
function findOverlaps(nodes, minGap) {
  minGap = minGap || 0;
  var pairs = [];
  for (var i = 0; i < nodes.length; i++) {
    for (var j = i + 1; j < nodes.length; j++) {
      if (isOverlap(nodes[i], nodes[j], minGap)) {
        pairs.push([i, j]);
      }
    }
  }
  return pairs;
}

// 推开重叠节点（简单策略：沿重叠方向各推一半）
function resolveOverlaps(nodes, minGap, maxIterations) {
  minGap = minGap || 8;
  maxIterations = maxIterations || 10;
  for (var iter = 0; iter < maxIterations; iter++) {
    var pairs = findOverlaps(nodes, minGap);
    if (pairs.length === 0) break;
    pairs.forEach(function(pair) {
      var a = nodes[pair[0]], b = nodes[pair[1]];
      var dx = (a.x + a.w / 2) - (b.x + b.w / 2);
      var dy = (a.y + a.h / 2) - (b.y + b.h / 2);
      // 沿主方向推开
      if (Math.abs(dx) > Math.abs(dy)) {
        var push = (a.w / 2 + b.w / 2 + minGap - Math.abs(dx)) / 2;
        if (dx >= 0) { a.x += push; b.x -= push; }
        else { a.x -= push; b.x += push; }
      } else {
        var push = (a.h / 2 + b.h / 2 + minGap - Math.abs(dy)) / 2;
        if (dy >= 0) { a.y += push; b.y -= push; }
        else { a.y -= push; b.y += push; }
      }
    });
  }
}
```

---

## 四、连线工具

```javascript
// 直线连接（从 source 边缘到 target 边缘）
// direction: 'tb'(上下), 'lr'(左右), 'auto'(自动判断)
function connectNodes(src, tgt, direction) {
  if (direction === 'auto') {
    var dx = Math.abs((tgt.x + tgt.w / 2) - (src.x + src.w / 2));
    var dy = Math.abs((tgt.y + tgt.h / 2) - (src.y + src.h / 2));
    direction = dy > dx ? 'tb' : 'lr';
  }
  if (direction === 'tb') {
    var x1 = src.x + src.w / 2, x2 = tgt.x + tgt.w / 2;
    var y1 = src.y + src.h, y2 = tgt.y;
    if (src.y > tgt.y) { y1 = src.y; y2 = tgt.y + tgt.h; }
    return { x1: x1, y1: y1, x2: x2, y2: y2 };
  } else {
    var x1 = src.x + src.w, x2 = tgt.x;
    var y1 = src.y + src.h / 2, y2 = tgt.y + tgt.h / 2;
    if (src.x > tgt.x) { x1 = src.x; x2 = tgt.x + tgt.w; }
    return { x1: x1, y1: y1, x2: x2, y2: y2 };
  }
}

// 贝塞尔曲线连线（更美观）
function bezierPath(x1, y1, x2, y2, direction) {
  if (direction === 'tb') {
    var cy = (y1 + y2) / 2;
    return 'M' + x1 + ',' + y1 + ' C' + x1 + ',' + cy + ' ' + x2 + ',' + cy + ' ' + x2 + ',' + y2;
  } else {
    var cx = (x1 + x2) / 2;
    return 'M' + x1 + ',' + y1 + ' C' + cx + ',' + y1 + ' ' + cx + ',' + y2 + ' ' + x2 + ',' + y2;
  }
}

// L 形折线连线（先水平/垂直再转向）
function elbowPath(x1, y1, x2, y2, direction) {
  if (direction === 'tb') {
    var midY = (y1 + y2) / 2;
    return 'M' + x1 + ',' + y1 + ' L' + x1 + ',' + midY + ' L' + x2 + ',' + midY + ' L' + x2 + ',' + y2;
  } else {
    var midX = (x1 + x2) / 2;
    return 'M' + x1 + ',' + y1 + ' L' + midX + ',' + y1 + ' L' + midX + ',' + y2 + ' L' + x2 + ',' + y2;
  }
}
```

---

## 五、画布自适应

```javascript
// 根据所有节点计算最小画布尺寸
// 返回 { w, h, offsetX, offsetY } — offset 用于整体平移
function calcCanvasSize(nodes, opts) {
  opts = opts || {};
  var pad = opts.padding || 24;
  var minW = opts.minW || 1000;
  var minH = opts.minH || 400;
  var minX = Infinity, minY = Infinity, maxX = 0, maxY = 0;
  nodes.forEach(function(n) {
    if (n.x < minX) minX = n.x;
    if (n.y < minY) minY = n.y;
    if (n.x + n.w > maxX) maxX = n.x + n.w;
    if (n.y + n.h > maxY) maxY = n.y + n.h;
  });
  var contentW = maxX - minX + pad * 2;
  var contentH = maxY - minY + pad * 2;
  return {
    w: Math.max(contentW, minW),
    h: Math.max(contentH, minH),
    offsetX: -minX + pad + Math.max(0, (minW - contentW) / 2),
    offsetY: -minY + pad
  };
}
```

---

## 六、验证检查

```javascript
// 验证图表质量，返回问题列表
function validateDiagram(nodes, lines, canvas) {
  var issues = [];

  // 1. 节点重叠
  var overlaps = findOverlaps(nodes, 8);
  overlaps.forEach(function(pair) {
    issues.push({ type: 'overlap', severity: 'error', a: pair[0], b: pair[1] });
  });

  // 2. 内容超出画布
  nodes.forEach(function(n, i) {
    if (n.x < 0 || n.y < 0 || n.x + n.w > canvas.w || n.y + n.h > canvas.h) {
      issues.push({ type: 'out_of_bounds', severity: 'error', node: i });
    }
  });

  // 3. 间距不足
  for (var i = 0; i < nodes.length; i++) {
    for (var j = i + 1; j < nodes.length; j++) {
      var a = nodes[i], b = nodes[j];
      var dx = Math.abs((a.x + a.w / 2) - (b.x + b.w / 2)) - (a.w + b.w) / 2;
      var dy = Math.abs((a.y + a.h / 2) - (b.y + b.h / 2)) - (a.h + b.h) / 2;
      var gap = Math.max(dx, dy);
      if (gap >= 0 && gap < 20) {
        issues.push({ type: 'too_close', severity: 'warn', a: i, b: j, gap: gap });
      }
    }
  }

  return issues;
}
```

---

## 七、配色（Theme）

所有模板的 theme 对象从 design-system.md 的配色表取值。以下是标准 theme 接口，按用途分区。

### 通用字段（所有图表都有）

```javascript
var theme = {
  // 标题（所有模板统一：左上角 16px bold）
  title: { color: '#1a1a2e' },       // N-8 近似
  subtitle: { color: '#888888' },

  // 连线（所有结构图共用）
  line: { color: '#94A3B8', width: 1.5, label: '#64748B' },  // N-5, N-6
};
```

### 流程图/泳道图节点色

```javascript
  // 节点类型 → 配色（来自语义色 + 主题色序列）
  node:      { bg: '#EFF6FF', border: '#93C5FD', text: '#1E293B' },  // C-1 浅底/中间/N-7
  highlight: { bg: '#3B82F6', border: '#3B82F6', text: '#FFFFFF' },  // C-1 实心
  decision:  { bg: '#FFFBEB', border: '#FCD34D', text: '#92400E' },  // C-3 Amber
  success:   { bg: '#ECFDF5', border: '#6EE7B7', text: '#065F46' },  // C-2 Emerald
  error:     { bg: '#FFF1F2', border: '#FDA4AF', text: '#9F1239' },  // C-4 Rose
  external:  { bg: '#F8FAFC', border: '#CBD5E1', text: '#64748B' },  // N-1/N-4/N-6
  datastore: { bg: '#F5F3FF', border: '#C4B5FD', text: '#5B21B6' },  // C-5 Violet

  // 连线（判断分支）
  lineYes: { color: '#10B981', width: 2 },   // 语义：成功
  lineNo:  { color: '#F43F5E', width: 2 },   // 语义：错误
```

### ER 图表色

```javascript
  // 表类型 → 表头配色
  tableTypes: {
    core:     { headerBg: '#3B82F6', headerText: '#FFFFFF', pkColor: '#3B82F6' },  // C-1
    normal:   { headerBg: '#10B981', headerText: '#FFFFFF', pkColor: '#10B981' },  // C-2
    junction: { headerBg: '#64748B', headerText: '#FFFFFF', pkColor: '#64748B' }   // N-6
  },
  field: { text: '#1E293B', type: '#94A3B8', fk: '#8B5CF6', divider: '#F1F5F9' },
  table: { bg: '#FFFFFF', border: '#E2E8F0' },
```

### 类图类型色

```javascript
  typeColors: {
    'class':     { header: '#3B82F6', border: 'rgba(59,130,246,0.3)' },   // C-1
    'interface': { header: '#10B981', border: 'rgba(16,185,129,0.3)' },   // C-2
    'abstract':  { header: '#8B5CF6', border: 'rgba(139,92,246,0.3)' },   // C-5
    'enum':      { header: '#F59E0B', border: 'rgba(245,158,11,0.3)' }    // C-3
  },
  depLine: { color: '#B0B8C4', width: 1 },  // 依赖线（更细更淡）
```

### 分层/分组色（架构图、流程图分组、泳道标题）

```javascript
  // 6 色循环，半透明背景 + 实色标签
  layers: [
    { bg: 'rgba(102,126,234,0.06)', border: 'rgba(102,126,234,0.15)', color: '#667eea' },
    { bg: 'rgba(67,233,123,0.06)',  border: 'rgba(67,233,123,0.15)',  color: '#43e97b' },
    { bg: 'rgba(79,172,254,0.06)',  border: 'rgba(79,172,254,0.15)',  color: '#4facfe' },
    { bg: 'rgba(245,158,11,0.06)',  border: 'rgba(245,158,11,0.15)',  color: '#f59e0b' },
    { bg: 'rgba(139,92,246,0.06)',  border: 'rgba(139,92,246,0.15)',  color: '#8b5cf6' },
    { bg: 'rgba(244,63,94,0.06)',   border: 'rgba(244,63,94,0.15)',   color: '#f43f5e' }
  ],

  // 泳道标题色（实色背景）
  laneHeaders: [
    { bg: '#3B82F6', text: '#FFFFFF' },  // C-1
    { bg: '#10B981', text: '#FFFFFF' },  // C-2
    { bg: '#F59E0B', text: '#FFFFFF' },  // C-3
    { bg: '#8B5CF6', text: '#FFFFFF' },  // C-5
    { bg: '#06B6D4', text: '#FFFFFF' },  // C-6
    { bg: '#F43F5E', text: '#FFFFFF' }   // C-4
  ],
```

### 统计图序列色

```javascript
  series: ['#667eea', '#f5576c', '#43e97b', '#4facfe', '#fa8231', '#a55eea', '#fc5c65', '#26de81'],
```

### 使用规则

- **不硬编码颜色**：所有颜色从 theme 对象取值
- **每个模板只引入需要的字段**：流程图不需要 `tableTypes`，ER 图不需要 `decision`
- **颜色值来源**：全部来自 `design-system.md` 的配色表，对应关系用注释标明（如 `// C-1`）
- **title/subtitle 统一**：所有模板使用相同的标题颜色和字号（16px/12px），不在 theme 里定义 size（避免声明了不用的混乱）

---

## 八、标准 SVG defs

常用的 SVG 定义（箭头 marker、阴影 filter），所有模板复用：

```javascript
function addStandardDefs(svg, theme) {
  theme = theme || defaultTheme;
  var defs = el('defs');

  // 标准箭头
  var arrow = el('marker', {
    id: 'arrow', markerWidth: 8, markerHeight: 6,
    refX: 8, refY: 3, orient: 'auto'
  });
  arrow.appendChild(el('path', {
    d: 'M0,0.5 L7,3 L0,5.5',
    fill: 'none', stroke: theme.line.color,
    'stroke-width': 1.2, 'stroke-linecap': 'round'
  }));
  defs.appendChild(arrow);

  // 成功箭头（绿色）
  var arrowG = el('marker', {
    id: 'arrow-g', markerWidth: 8, markerHeight: 6,
    refX: 8, refY: 3, orient: 'auto'
  });
  arrowG.appendChild(el('path', {
    d: 'M0,0.5 L7,3 L0,5.5',
    fill: 'none', stroke: theme.lineSuccess.color,
    'stroke-width': 1.2, 'stroke-linecap': 'round'
  }));
  defs.appendChild(arrowG);

  // 错误箭头（红色）
  var arrowR = el('marker', {
    id: 'arrow-r', markerWidth: 8, markerHeight: 6,
    refX: 8, refY: 3, orient: 'auto'
  });
  arrowR.appendChild(el('path', {
    d: 'M0,0.5 L7,3 L0,5.5',
    fill: 'none', stroke: theme.lineError.color,
    'stroke-width': 1.2, 'stroke-linecap': 'round'
  }));
  defs.appendChild(arrowR);

  // 节点阴影
  var shadow = el('filter', {
    id: 'shadow', x: '-10%', y: '-10%', width: '130%', height: '140%'
  });
  shadow.appendChild(el('feDropShadow', {
    dx: 0, dy: 2, stdDeviation: 3, 'flood-color': 'rgba(0,0,0,0.06)'
  }));
  defs.appendChild(shadow);

  svg.appendChild(defs);
}
```

---

## 九、渲染顺序规范

所有模板必须按以下顺序渲染 SVG 元素：

```javascript
// 1. 背景层（层容器、泳道背景等）
var bgGroup = el('g');
svg.appendChild(bgGroup);

// 2. 连线层（箭头、关系线）
var lineGroup = el('g');
svg.appendChild(lineGroup);

// 3. 节点层（节点矩形、文字、图标）
var nodeGroup = el('g');
svg.appendChild(nodeGroup);
```

这确保连线不会遮挡节点，节点不会被背景覆盖。
