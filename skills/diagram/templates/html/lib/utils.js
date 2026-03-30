/**
 * 图表公共工具函数 — 所有模板共享
 * 用法：<script src="lib/utils.js"></script>
 */

// SVG 命名空间（兼容 NS / svgNS 两种写法）
var NS = 'http://www.w3.org/2000/svg';
var svgNS = NS;

/**
 * 创建 SVG 元素并设置属性
 * @param {string} tag - SVG 标签名
 * @param {Object} attrs - 属性键值对
 * @param {string} [text] - 可选文本内容
 */
function el(tag, attrs, text) {
  var e = document.createElementNS(NS, tag);
  if (attrs) for (var k in attrs) e.setAttribute(k, attrs[k]);
  if (text !== undefined) e.textContent = text;
  return e;
}

/**
 * 中英混合文本宽度测量
 * 中文字符按 fontSize 宽度计算，英文/数字按 0.6 倍
 * @param {string} str - 待测量文本
 * @param {number} fontSize - 字号
 */
function measureText(str, fontSize) {
  var w = 0;
  for (var i = 0; i < str.length; i++) {
    w += str.charCodeAt(i) > 127 ? fontSize : fontSize * 0.6;
  }
  return w;
}

// 缩写别名（部分模板使用 mt 代替 measureText）
var mt = measureText;
