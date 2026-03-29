/**
 * 图表质量自动检测脚本
 * 在 Playwright browser_evaluate 中执行
 * 返回检测结果对象
 */
function checkDiagramQuality() {
  var results = { pass: true, checks: [], errors: [] };

  function check(name, level, passed, detail) {
    results.checks.push({ name: name, level: level, passed: passed, detail: detail || '' });
    if (!passed) {
      results.pass = false;
      results.errors.push('[' + level + '] ' + name + ': ' + (detail || 'FAIL'));
    }
  }

  var svg = document.querySelector('svg');
  var body = document.body;
  var isHtmlTemplate = !svg || svg.children.length === 0;  // swot/journey 等 HTML/CSS 模板

  // ========== A 级：基础渲染 ==========
  if (isHtmlTemplate) {
    // HTML/CSS 模板：检查 body 有内容
    check('页面有内容', 'A', body.children.length > 0 && body.scrollHeight > 100, 'height=' + body.scrollHeight);
    check('有标题', 'E', !!document.querySelector('h1, h2, [class*=title]') || body.textContent.length > 10);
    check('body inline-block', 'E', window.getComputedStyle(body).display === 'inline-block', 'display=' + window.getComputedStyle(body).display);
    var bg = window.getComputedStyle(body).backgroundColor;
    check('白色背景', 'E', bg === 'rgb(255, 255, 255)');
    results.summary = results.checks.filter(function(c) { return c.passed; }).length + '/' + results.checks.length;
    results.nodeCount = 0;
    results.textCount = 0;
    results.isHtml = true;
    return results;
  }

  check('画布存在', 'A', !!svg, svg ? 'found' : 'no SVG element');
  if (!svg) return results;

  var svgW = parseFloat(svg.getAttribute('width') || 0);
  var svgH = parseFloat(svg.getAttribute('height') || 0);
  check('画布有尺寸', 'A', svgW > 0 && svgH > 0, svgW + '×' + svgH);
  check('画布有内容', 'A', svg.children.length > 2, svg.children.length + ' children');
  check('body 有内容', 'A', body.scrollWidth > 48, 'scrollWidth=' + body.scrollWidth);

  // ========== B 级：布局规则 ==========
  // B1: 节点不重叠
  var rects = [];
  svg.querySelectorAll('rect, polygon, ellipse, circle').forEach(function(el) {
    var bbox = el.getBBox();
    if (bbox.width > 10 && bbox.height > 10) {  // 忽略小元素（箭头、装饰）
      rects.push({ x: bbox.x, y: bbox.y, w: bbox.width, h: bbox.height, tag: el.tagName });
    }
  });

  var overlaps = 0;
  for (var i = 0; i < rects.length; i++) {
    for (var j = i + 1; j < rects.length; j++) {
      var a = rects[i], b = rects[j];
      // 计算交叉面积
      var ix = Math.max(a.x, b.x);
      var iy = Math.max(a.y, b.y);
      var iw = Math.min(a.x + a.w, b.x + b.w) - ix;
      var ih = Math.min(a.y + a.h, b.y + b.h) - iy;
      if (iw > 0 && ih > 0) {
        var interArea = iw * ih;
        // 排除：交叉面积太小（边界触碰）、包含关系、容器关系
        if (interArea > 100) {
          var M = 10;
          var aContainsB = a.x - M <= b.x && a.y - M <= b.y && a.x + a.w + M >= b.x + b.w && a.y + a.h + M >= b.y + b.h;
          var bContainsA = b.x - M <= a.x && b.y - M <= a.y && b.x + b.w + M >= a.x + a.w && b.y + b.h + M >= a.y + a.h;
          var areaA = a.w * a.h, areaB = b.w * b.h;
          var areaRatio = Math.max(areaA, areaB) / Math.min(areaA, areaB);
          var isContainer = areaRatio > 3;
          if (!aContainsB && !bContainsA && !isContainer) {
            overlaps++;
          }
        }
      }
    }
  }
  check('节点不重叠', 'B', overlaps === 0, overlaps + ' 对重叠');

  // B2: 内容不越界
  var outOfBounds = 0;
  rects.forEach(function(r) {
    if (r.x < -5 || r.y < -5 || r.x + r.w > svgW + 5 || r.y + r.h > svgH + 5) {
      outOfBounds++;
    }
  });
  check('内容不越界', 'B', outOfBounds === 0, outOfBounds + ' 个越界');

  // B3: 文字不截断（检查 text 元素是否在 SVG 范围内）
  var truncated = 0;
  svg.querySelectorAll('text').forEach(function(t) {
    var bbox = t.getBBox();
    if (bbox.width > 0 && (bbox.x + bbox.width > svgW + 10 || bbox.x < -10)) {
      truncated++;
    }
  });
  check('文字不截断', 'B', truncated === 0, truncated + ' 个截断');

  // ========== E 级：设计规范 ==========
  // E1: 标题检测（兼容 SVG text 14-16px bold 或 HTML h1/h2）
  var texts = svg.querySelectorAll('text');
  var hasTitle = false;
  texts.forEach(function(t) {
    var fs = parseInt(t.getAttribute('font-size') || '0');
    var fw = t.getAttribute('font-weight');
    if (fs >= 14 && fs <= 22 && (fw === '700' || fw === 'bold')) hasTitle = true;
  });
  // 也检查 HTML 标题元素
  if (!hasTitle) {
    hasTitle = !!document.querySelector('h1, h2, .title');
  }
  check('有标题', 'E', hasTitle);

  // E2: body inline-block
  var bodyDisplay = window.getComputedStyle(body).display;
  check('body inline-block', 'E', bodyDisplay === 'inline-block', 'display=' + bodyDisplay);

  // E3: 白色背景
  var bodyBg = window.getComputedStyle(body).backgroundColor;
  var isWhite = bodyBg === 'rgb(255, 255, 255)' || bodyBg === '#ffffff' || bodyBg === 'white';
  check('白色背景', 'E', isWhite, 'bg=' + bodyBg);

  // E4: 节点配色在允许范围内
  var allowedFills = [
    '#EFF6FF', '#ECFDF5', '#FFFBEB', '#FFF1F2', '#F5F3FF', '#F8FAFC',  // 浅底色
    '#3B82F6', '#10B981', '#F59E0B', '#F43F5E', '#8B5CF6', '#06B6D4',  // 主色
    '#FFFFFF', '#ffffff', 'none', '#1E293B', '#0F172A',                   // 基础色
    '#64748B', '#94A3B8', '#CBD5E1', '#E2E8F0', '#F1F5F9',              // 灰色系
  ].map(function(c) { return c.toLowerCase(); });

  // 不严格检测，只统计非标准色数量
  var nonStandardColors = 0;
  svg.querySelectorAll('rect, polygon, ellipse, circle').forEach(function(el) {
    var fill = (el.getAttribute('fill') || '').toLowerCase();
    if (fill && fill !== 'none' && !fill.startsWith('rgba') && !fill.startsWith('url') && allowedFills.indexOf(fill) === -1) {
      nonStandardColors++;
    }
  });
  check('配色规范', 'E', nonStandardColors <= 3, nonStandardColors + ' 个非标准色');

  // ========== 视觉检测（间距均匀性） ==========
  // 计算相邻节点间的最小间距
  var gaps = [];
  for (var i = 0; i < rects.length; i++) {
    for (var j = i + 1; j < rects.length; j++) {
      var a = rects[i], b = rects[j];
      var dx = Math.max(0, Math.max(a.x, b.x) - Math.min(a.x + a.w, b.x + b.w));
      var dy = Math.max(0, Math.max(a.y, b.y) - Math.min(a.y + a.h, b.y + b.h));
      var gap = Math.sqrt(dx * dx + dy * dy);
      if (gap > 0 && gap < 200) gaps.push(gap);  // 只看相近节点
    }
  }
  if (gaps.length > 0) {
    var minGap = Math.min.apply(null, gaps);
    check('最小间距 ≥ 8px', 'B', minGap >= 8, 'min gap=' + minGap.toFixed(1) + 'px');
  }

  // 统计汇总
  var passCount = results.checks.filter(function(c) { return c.passed; }).length;
  results.summary = passCount + '/' + results.checks.length + ' passed';
  results.nodeCount = rects.length;
  results.textCount = texts.length;

  return results;
}

checkDiagramQuality();
