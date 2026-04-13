#!/usr/bin/env node
/**
 * MD 预览工具：全局单例 HTTP server + 专业蓝灰主题渲染 + 左侧目录 + 文件监听自动刷新。
 * 用法：node scripts/preview-md.mjs <path-to-md-file>
 *
 * 首次调用启动 server，后续调用复用已有 server，直接打开新文件预览。
 * 所有浏览器标签关闭 1 分钟后 server 自动退出。
 *
 * 样式来源：skills/shared/styles/base.css（与 HTML 报告共用）
 */
import { readFileSync, watchFile, unwatchFile, existsSync, writeFileSync, unlinkSync } from 'fs';
import { createServer } from 'http';
import { resolve, basename, dirname, extname, join } from 'path';
import { exec } from 'child_process';
import { fileURLToPath } from 'url';
import http from 'http';

// 读取共享样式
const __dirname = dirname(fileURLToPath(import.meta.url));
const BASE_CSS_PATH = resolve(__dirname, '../../shared/styles/base.css');
const baseCSS = readFileSync(BASE_CSS_PATH, 'utf-8');

// MIME types for static file serving
const MIME_TYPES = {
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.gif': 'image/gif', '.svg': 'image/svg+xml', '.webp': 'image/webp',
  '.ico': 'image/x-icon', '.bmp': 'image/bmp',
  '.css': 'text/css', '.js': 'text/javascript',
  '.pdf': 'application/pdf', '.json': 'application/json',
};

const mdPath = process.argv[2];
if (!mdPath) {
  console.error('用法: node scripts/preview-md.mjs <markdown-file>');
  process.exit(1);
}

const absPath = resolve(mdPath);
const LOCK_FILE = '/tmp/md-preview-server.json';

// 尝试连接已有 server
async function tryExistingServer() {
  if (!existsSync(LOCK_FILE)) return false;
  try {
    const info = JSON.parse(readFileSync(LOCK_FILE, 'utf-8'));
    // 注册文件并获取 URL
    return await new Promise((resolve) => {
      const postData = JSON.stringify({ file: absPath });
      const req = http.request({
        hostname: '127.0.0.1',
        port: info.port,
        path: '/api/watch',
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(postData) },
        timeout: 2000,
      }, (res) => {
        let body = '';
        res.on('data', c => body += c);
        res.on('end', () => {
          if (res.statusCode === 200) {
            const { url } = JSON.parse(body);
            resolve(url);
          } else {
            resolve(false);
          }
        });
      });
      req.on('error', () => resolve(false));
      req.on('timeout', () => { req.destroy(); resolve(false); });
      req.end(postData);
    });
  } catch {
    return false;
  }
}

// 主逻辑
const existingUrl = await tryExistingServer();
if (existingUrl) {
  console.log(`复用已有预览服务: ${existingUrl}`);
  const cmd = process.platform === 'darwin' ? 'open' : 'xdg-open';
  exec(`${cmd} "${existingUrl}"`);
  process.exit(0);
}

// --- 以下为 server 模式 ---

// 文件监听管理：{ absPath: { watchers: Set<res>, watched: boolean } }
const fileRegistry = new Map();

function registerFile(filePath) {
  if (fileRegistry.has(filePath)) return;
  fileRegistry.set(filePath, { watchers: new Set(), watched: false });
  startWatching(filePath);
}

function startWatching(filePath) {
  const entry = fileRegistry.get(filePath);
  if (entry.watched) return;
  watchFile(filePath, { interval: 500 }, () => {
    entry.watchers.forEach(res => {
      res.write('data: reload\n\n');
    });
  });
  entry.watched = true;
}

function addSSEClient(filePath, res) {
  registerFile(filePath);
  fileRegistry.get(filePath).watchers.add(res);
  cancelShutdown();
}

function removeSSEClient(filePath, res) {
  const entry = fileRegistry.get(filePath);
  if (!entry) return;
  entry.watchers.delete(res);
  scheduleShutdownIfEmpty();
}

function getTotalClients() {
  let total = 0;
  for (const entry of fileRegistry.values()) {
    total += entry.watchers.size;
  }
  return total;
}

// 自动关闭逻辑
let shutdownTimer = null;

function scheduleShutdownIfEmpty() {
  if (getTotalClients() > 0) return;
  shutdownTimer = setTimeout(() => {
    if (getTotalClients() === 0) {
      console.log('所有浏览器已断开，自动关闭预览服务');
      cleanup();
    }
  }, 60000);
}

function cancelShutdown() {
  if (shutdownTimer) {
    clearTimeout(shutdownTimer);
    shutdownTimer = null;
  }
}

function cleanup() {
  for (const [filePath, entry] of fileRegistry) {
    if (entry.watched) unwatchFile(filePath);
  }
  try { unlinkSync(LOCK_FILE); } catch {}
  server.close();
  process.exit(0);
}

// GitHub Alerts SVG icons
const CALLOUT_ICONS = {
  NOTE: '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM6.5 7.75A.75.75 0 0 1 7.25 7h1a.75.75 0 0 1 .75.75v2.75h.25a.75.75 0 0 1 0 1.5h-2a.75.75 0 0 1 0-1.5h.25v-2h-.25a.75.75 0 0 1-.75-.75ZM8 6a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"/></svg>',
  TIP: '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 1.5c-2.363 0-4 1.69-4 3.75 0 .984.424 1.625.984 2.304l.214.253c.223.264.47.556.673.848.284.411.537.896.621 1.49a.75.75 0 0 1-1.484.211c-.04-.282-.163-.547-.37-.847a8.456 8.456 0 0 0-.542-.68c-.084-.1-.173-.205-.268-.32C3.201 7.75 2.5 6.766 2.5 5.25 2.5 2.31 4.863 0 8 0s5.5 2.31 5.5 5.25c0 1.516-.701 2.5-1.328 3.259-.095.115-.184.22-.268.319-.207.245-.383.453-.541.681-.208.3-.33.565-.37.847a.751.751 0 0 1-1.485-.212c.084-.593.337-1.078.621-1.489.203-.292.45-.584.673-.848.075-.088.147-.173.213-.253.561-.679.985-1.32.985-2.304 0-2.06-1.637-3.75-4-3.75ZM5.75 12h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM6 15.25a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 0 1.5h-2.5a.75.75 0 0 1-.75-.75Z"/></svg>',
  IMPORTANT: '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v9.5A1.75 1.75 0 0 1 14.25 13H8.06l-2.573 2.573A1.458 1.458 0 0 1 3 14.543V13H1.75A1.75 1.75 0 0 1 0 11.25Zm1.75-.25a.25.25 0 0 0-.25.25v9.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h6.5a.25.25 0 0 0 .25-.25v-9.5a.25.25 0 0 0-.25-.25Zm7 2.25v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 9a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"/></svg>',
  WARNING: '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M6.457 1.047c.659-1.234 2.427-1.234 3.086 0l6.082 11.378A1.75 1.75 0 0 1 14.082 15H1.918a1.75 1.75 0 0 1-1.543-2.575Zm1.763.707a.25.25 0 0 0-.44 0L1.698 13.132a.25.25 0 0 0 .22.368h12.164a.25.25 0 0 0 .22-.368Zm.53 3.996v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 11a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"/></svg>',
  CAUTION: '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M4.47.22A.749.749 0 0 1 5 0h6c.199 0 .389.079.53.22l4.25 4.25c.141.14.22.331.22.53v6a.749.749 0 0 1-.22.53l-4.25 4.25A.749.749 0 0 1 11 16H5a.749.749 0 0 1-.53-.22L.22 11.53A.749.749 0 0 1 0 11V5c0-.199.079-.389.22-.53Zm.84 1.28L1.5 5.31v5.38l3.81 3.81h5.38l3.81-3.81V5.31L10.69 1.5ZM8 4a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75.75 0 0 1 8 4Zm0 8a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"/></svg>',
};
const CALLOUT_LABELS = { NOTE: 'Note', TIP: 'Tip', IMPORTANT: 'Important', WARNING: 'Warning', CAUTION: 'Caution' };

// 生成预览页面 HTML
function buildHTML(filePath) {
  const fileTitle = basename(filePath, '.md');
  const encodedPath = encodeURIComponent(filePath);
  const fileDir = dirname(filePath);
  const encodedDir = encodeURIComponent(fileDir);
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${fileTitle}</title>
<style>
${baseCSS}

/* ─── highlight.js 背景覆盖，保持与 base.css 一致 ─── */
pre code.hljs { background: #1e293b; padding: 16px 20px; }

/* ─── Preview-specific ─── */
#content {
  background: var(--c-surface);
  padding: 40px 48px 64px;
  border: 1px solid var(--c-border);
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
#content > *:last-child { margin-bottom: 0; }

.file-path {
  margin: 0 0 12px;
  font-size: 12px;
  color: var(--c-text-muted);
  font-family: var(--font-mono);
}

.export-btn {
  position: fixed;
  top: 16px;
  right: 20px;
  z-index: 200;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  color: var(--c-text);
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: 6px;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  transition: all 0.15s ease;
}
.export-btn:hover { background: var(--c-border-light); border-color: var(--c-primary); color: var(--c-primary); }
.export-btn svg { width: 16px; height: 16px; fill: currentColor; }

@media print {
  .export-btn, .file-path { display: none !important; }
}
</style>
</head>
<body>

<nav class="sidebar">
  <div class="sidebar-title">目录</div>
  <ul class="toc-list" id="toc"></ul>
</nav>

<button class="export-btn" onclick="exportHTML()" title="下载为 HTML">
  <svg viewBox="0 0 16 16"><path d="M3.5 1.75a.25.25 0 01.25-.25h3.168a.75.75 0 01.536.222l5.25 5.168a.75.75 0 01.226.534v6.826a.25.25 0 01-.25.25h-8.93a.25.25 0 01-.25-.25V1.75zM3.75 0A1.75 1.75 0 002 1.75v12.5c0 .966.784 1.75 1.75 1.75h8.5A1.75 1.75 0 0014 14.25V7.422a1.75 1.75 0 00-.512-1.243l-5.25-5.168A1.75 1.75 0 006.918 0H3.75z"/></svg>
  下载 HTML
</button>

<main class="content">
  <div class="file-path">${filePath}</div>
  <article id="content"></article>
</main>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.1/marked.min.js"></script>
<script>
window.__mermaidReady = new Promise(function(resolve) { window.__mermaidResolve = resolve; });
</script>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
window.__mermaid = mermaid;
/*
 * Mermaid 主题配置 — 对齐 diagram skill 设计规范
 *
 * 核心策略：
 * 1. themeVariables 控制基础色板
 * 2. themeCSS 注入 SVG 内部样式，实现节点分色、圆角、投影等 CSS 无法外部覆盖的效果
 */
/*
 * diagram skill 6 色色板：
 *   蓝  #DBEAFE / #93C5FD / #1E293B
 *   绿  #D1FAE5 / #6EE7B7 / #065F46
 *   紫  #EDE9FE / #C4B5FD / #5B21B6
 *   琥珀 #FEF3C7 / #FCD34D / #92400E
 *   玫红 #FECDD3 / #FDA4AF / #9F1239
 *   青  #CFFAFE / #67E8F9 / #155E75
 */
const MERMAID_CSS = \`
  /* ═══ 通用基础 ═══ */
  .node rect, .node polygon, .node circle, .node ellipse,
  .basic.label-container { filter: drop-shadow(0 1px 2px rgba(0,0,0,0.06)); }
  .node rect, .basic.label-container { rx: 6; ry: 6; }
  .nodeLabel, .node foreignObject div { font-weight: 500; line-height: 1.4; }
  .label { text-shadow: none; }
  .edgeLabel { font-size: 11px; }
  .edgeLabel .label rect { opacity: 0.9; rx: 3; ry: 3; }

  /* ═══ 流程图 — 节点按 nth-child 轮播 6 色 ═══ */
  .flowchart-link { stroke-width: 1.5px; }
  .marker { fill: #94A3B8; }

  /* 菱形（决策节点）— 始终琥珀色 */
  .node polygon { fill: #FEF3C7 !important; stroke: #FCD34D !important; }
  .node:has(polygon) .nodeLabel { color: #92400E !important; }

  /* 矩形节点 — 6 色轮播 */
  .node:nth-child(6n+1) .basic.label-container { fill: #DBEAFE; stroke: #93C5FD; }
  .node:nth-child(6n+2) .basic.label-container { fill: #D1FAE5; stroke: #6EE7B7; }
  .node:nth-child(6n+2) .nodeLabel { color: #065F46; }
  .node:nth-child(6n+3) .basic.label-container { fill: #EDE9FE; stroke: #C4B5FD; }
  .node:nth-child(6n+3) .nodeLabel { color: #5B21B6; }
  .node:nth-child(6n+4) .basic.label-container { fill: #CFFAFE; stroke: #67E8F9; }
  .node:nth-child(6n+4) .nodeLabel { color: #155E75; }
  .node:nth-child(6n+5) .basic.label-container { fill: #FECDD3; stroke: #FDA4AF; }
  .node:nth-child(6n+5) .nodeLabel { color: #9F1239; }
  .node:nth-child(6n+6) .basic.label-container { fill: #FEF3C7; stroke: #FCD34D; }
  .node:nth-child(6n+6) .nodeLabel { color: #92400E; }

  /* ═══ 子图/集群 — 6 色轮播（对齐 diagram 分层背景） ═══ */
  .cluster rect { rx: 10; ry: 10; stroke-width: 1.5px; }
  .cluster span, .cluster .nodeLabel { font-weight: 600; font-size: 13px; }
  .cluster:nth-child(6n+1) rect { fill: rgba(59,130,246,0.05); stroke: rgba(59,130,246,0.2); }
  .cluster:nth-child(6n+1) span { color: #3B82F6; }
  .cluster:nth-child(6n+2) rect { fill: rgba(16,185,129,0.05); stroke: rgba(16,185,129,0.2); }
  .cluster:nth-child(6n+2) span { color: #10B981; }
  .cluster:nth-child(6n+3) rect { fill: rgba(139,92,246,0.05); stroke: rgba(139,92,246,0.2); }
  .cluster:nth-child(6n+3) span { color: #8B5CF6; }
  .cluster:nth-child(6n+4) rect { fill: rgba(245,158,11,0.05); stroke: rgba(245,158,11,0.2); }
  .cluster:nth-child(6n+4) span { color: #F59E0B; }
  .cluster:nth-child(6n+5) rect { fill: rgba(244,63,94,0.05); stroke: rgba(244,63,94,0.2); }
  .cluster:nth-child(6n+5) span { color: #F43F5E; }
  .cluster:nth-child(6n+6) rect { fill: rgba(14,165,233,0.05); stroke: rgba(14,165,233,0.2); }
  .cluster:nth-child(6n+6) span { color: #0EA5E9; }

  /* ═══ 序列图 ═══ */
  .actor { rx: 6; ry: 6; filter: drop-shadow(0 1px 2px rgba(0,0,0,0.06)); }
  text.actor > tspan { font-weight: 600; font-size: 13px; }
  .messageLine0, .messageLine1 { stroke-width: 1.5px; }
  .messageText { font-size: 12px; font-weight: 500; }
  .loopText tspan { font-size: 11px; font-weight: 500; }
  .labelBox { rx: 3; ry: 3; }
  .actor-line { stroke-dasharray: 4 3; stroke: #CBD5E1; }
  .note { rx: 4; ry: 4; filter: drop-shadow(0 1px 2px rgba(0,0,0,0.04)); }
  /* 序列图/类图/状态图/ER图 — 节点分色通过 JS colorizeMermaidCharts() 后处理 */
  .activation0 { fill: #EFF6FF; stroke: #3B82F6; }
  .activation1 { fill: #ECFDF5; stroke: #10B981; }
  .activation2 { fill: #F5F3FF; stroke: #8B5CF6; }

  /* ═══ 类图 ═══ */
  [id^="classId-"] .label-container { rx: 8; ry: 8; filter: drop-shadow(0 1px 2px rgba(0,0,0,0.06)); }
  .relation { stroke-width: 1.5px; stroke: #94A3B8; }
  .cardinality { font-size: 10px; fill: #64748B; }

  /* ═══ 状态图 ═══ */
  [id^="state-"] .label-container { rx: 8; ry: 8; filter: drop-shadow(0 1px 2px rgba(0,0,0,0.06)); }

  /* ═══ ER 图 ═══ */
  [id^="entity-"] .label-container { rx: 8; ry: 8; filter: drop-shadow(0 1px 2px rgba(0,0,0,0.06)); }
  .relationshipLine { stroke-width: 1.5px; stroke: #94A3B8; }

  /* ═══ 甘特图 ═══ */
  .task { rx: 4; ry: 4; }
  .taskText { font-size: 11px; font-weight: 500; }
  .sectionTitle { font-weight: 600; font-size: 12px; }

  /* ═══ 饼图 ═══ */
  .pieCircle { filter: drop-shadow(0 2px 4px rgba(0,0,0,0.08)); }
  .pieTitleText { font-weight: 700; font-size: 16px; }
  .legend text { font-weight: 500; font-size: 12px; }
  .slice { font-weight: 600; }

  /* ═══ 思维导图 ═══ */
  .mindmap-node rect, .mindmap-node circle { filter: drop-shadow(0 1px 3px rgba(0,0,0,0.1)); }
  .mindmap-node .nodeLabel { font-weight: 500; }

  /* ═══ Journey 旅程图 ═══ */
  .section-type-0 { fill: #3B82F6 !important; }
  .section-type-1 { fill: #10B981 !important; }
  .section-type-2 { fill: #8B5CF6 !important; }
\`;

mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  themeCSS: MERMAID_CSS,
  themeVariables: {
    /* 主节点 — 蓝色系 */
    primaryColor: '#DBEAFE',
    primaryTextColor: '#1E293B',
    primaryBorderColor: '#93C5FD',

    /* 次要节点 — 绿色系 */
    secondaryColor: '#D1FAE5',
    secondaryBorderColor: '#6EE7B7',
    secondaryTextColor: '#065F46',

    /* 三级节点 — 紫色系 */
    tertiaryColor: '#EDE9FE',
    tertiaryBorderColor: '#C4B5FD',
    tertiaryTextColor: '#5B21B6',

    /* 连线 */
    lineColor: '#94A3B8',

    /* 字体 */
    fontFamily: '-apple-system, system-ui, "PingFang SC", "Noto Sans CJK SC", sans-serif',
    fontSize: '13px',

    /* 注释/备注 */
    noteBkgColor: '#FFFBEB',
    noteBorderColor: '#FCD34D',
    noteTextColor: '#92400E',

    /* 背景 */
    background: '#ffffff',
    mainBkg: '#DBEAFE',

    /* 文字 */
    textColor: '#1E293B',
    labelTextColor: '#64748B',

    /* 子图 */
    clusterBorder: '#93C5FD',
    clusterBkg: '#F0F7FF',

    /* 标签背景 */
    edgeLabelBackground: '#ffffff',

    /* 序列图 — 多色参与者 */
    actorBkg: '#DBEAFE',
    actorBorder: '#93C5FD',
    actorTextColor: '#1E293B',
    signalColor: '#475569',
    signalTextColor: '#475569',
    activationBorderColor: '#3B82F6',
    activationBkg: '#EFF6FF',
    sequenceNumberColor: '#ffffff',

    /* 甘特图 — 多色任务条 */
    gridColor: '#E2E8F0',
    todayLineColor: '#F43F5E',
    taskBkgColor: '#DBEAFE',
    taskBorderColor: '#93C5FD',
    taskTextColor: '#1E293B',
    activeTaskBkgColor: '#BFDBFE',
    activeTaskBorderColor: '#3B82F6',
    doneTaskBkgColor: '#D1FAE5',
    doneTaskBorderColor: '#6EE7B7',
    critBkgColor: '#FECACA',
    critBorderColor: '#F87171',
    sectionBkgColor: '#F8FAFC',
    altSectionBkgColor: '#F1F5F9',
    sectionBkgColor2: '#EFF6FF',

    /* 饼图 — 6色对齐 diagram 色板 */
    pie1: '#3B82F6',
    pie2: '#10B981',
    pie3: '#8B5CF6',
    pie4: '#F59E0B',
    pie5: '#F43F5E',
    pie6: '#0EA5E9',
    pie7: '#6366F1',
    pie8: '#EC4899',
    pieStrokeColor: '#ffffff',
    pieStrokeWidth: '2px',
    pieTitleTextSize: '16px',
    pieTitleTextColor: '#0F172A',
    pieSectionTextSize: '12px',
    pieSectionTextColor: '#ffffff',
    pieLegendTextSize: '12px',
    pieLegendTextColor: '#475569',
    pieOuterStrokeWidth: '0',

    /* 状态图 */
    labelColor: '#1E293B',
    altBackground: '#F8FAFC',
    compositeBackground: '#F8FAFC',
    compositeBorder: '#93C5FD',
    compositeTitleBackground: '#DBEAFE',

    /* 类图 — 提高饱和度 */
    classText: '#1E293B',

    /* 思维导图 */
    cScale0: '#3B82F6', cScaleLabel0: '#ffffff',
    cScale1: '#10B981', cScaleLabel1: '#ffffff',
    cScale2: '#8B5CF6', cScaleLabel2: '#ffffff',
    cScale3: '#F59E0B', cScaleLabel3: '#ffffff',
    cScale4: '#F43F5E', cScaleLabel4: '#ffffff',
    cScale5: '#0EA5E9', cScaleLabel5: '#ffffff',

    /* cScale 也用于 timeline / journey 配色 */
    cScalePeer0: '#DBEAFE', cScalePeer1: '#D1FAE5',
    cScalePeer2: '#EDE9FE', cScalePeer3: '#FEF3C7',
    cScalePeer4: '#FECACA', cScalePeer5: '#E0F2FE',

    /* ER 图 — 实体分色 */
    fill0: '#DBEAFE', fill1: '#D1FAE5',
    fill2: '#EDE9FE', fill3: '#FEF3C7',
    fill4: '#FECACA', fill5: '#E0F2FE',
    fill6: '#FCE7F3', fill7: '#FFF7ED',
  },
  flowchart: { curve: 'basis', padding: 20, htmlLabels: true, nodeSpacing: 60, rankSpacing: 50 },
  sequence: { mirrorActors: false, bottomMarginAdj: 2, useMaxWidth: false, messageMargin: 40, boxMargin: 8 },
  gantt: { useMaxWidth: false, fontSize: 11, barHeight: 24, barGap: 6, topPadding: 40, sectionFontSize: 12 },
  er: { useMaxWidth: false, fontSize: 13 },
  mindmap: { useMaxWidth: false, padding: 16 },
  timeline: { useMaxWidth: false },
  sankey: { useMaxWidth: false },
  journey: { useMaxWidth: false },
  class: { useMaxWidth: false },
  state: { useMaxWidth: false },
  c4: { useMaxWidth: false },
  pie: { useMaxWidth: false, textPosition: 0.75 },
});
window.__mermaidResolve();
</script>
<script>
  const FILE_PATH = '${encodedPath}';
  const FILE_DIR = '${encodedDir}';

  // GitHub Alerts callout 配置
  const CALLOUT_TYPES = {
    NOTE: { cls: 'callout-note', icon: '${CALLOUT_ICONS.NOTE.replace(/'/g, "\\'")}', label: 'Note' },
    TIP: { cls: 'callout-tip', icon: '${CALLOUT_ICONS.TIP.replace(/'/g, "\\'")}', label: 'Tip' },
    IMPORTANT: { cls: 'callout-important', icon: '${CALLOUT_ICONS.IMPORTANT.replace(/'/g, "\\'")}', label: 'Important' },
    WARNING: { cls: 'callout-warning', icon: '${CALLOUT_ICONS.WARNING.replace(/'/g, "\\'")}', label: 'Warning' },
    CAUTION: { cls: 'callout-caution', icon: '${CALLOUT_ICONS.CAUTION.replace(/'/g, "\\'")}', label: 'Caution' },
  };

  function resolveRelativePath(base, rel) {
    if (rel.startsWith('/') || rel.startsWith('http://') || rel.startsWith('https://') || rel.startsWith('data:')) {
      return null;
    }
    const baseParts = decodeURIComponent(base).split('/');
    const relParts = rel.split('/');
    for (const part of relParts) {
      if (part === '.' || part === '') continue;
      if (part === '..') baseParts.pop();
      else baseParts.push(part);
    }
    return baseParts.join('/');
  }

  function rewriteImagePaths() {
    document.querySelectorAll('#content img').forEach(img => {
      const src = img.getAttribute('src');
      if (!src) return;
      const absPath = resolveRelativePath(FILE_DIR, src);
      if (absPath) {
        img.src = '/api/file?path=' + encodeURIComponent(absPath);
      }
    });
  }

  // 将块级 img 包裹为 figure（仅当 img 是 <p> 的唯一子元素时）
  function wrapImagesInFigure() {
    document.querySelectorAll('#content p > img').forEach(img => {
      const p = img.parentElement;
      // 只处理 <p> 中仅含一个 img 的情况（块级图片）
      if (p.childNodes.length > 1) return;
      if (img.closest('figure')) return;
      const alt = img.getAttribute('alt');
      const figure = document.createElement('figure');
      p.parentNode.replaceChild(figure, p);
      figure.appendChild(img);
      if (alt && alt.trim()) {
        const caption = document.createElement('figcaption');
        caption.textContent = alt;
        figure.appendChild(caption);
      }
    });
  }

  // 转换 task list checkbox
  function renderTaskLists() {
    document.querySelectorAll('#content li').forEach(li => {
      const text = li.innerHTML;
      const checkedMatch = text.match(/^\\s*\\[x\\]\\s*/i);
      const uncheckedMatch = text.match(/^\\s*\\[ \\]\\s*/);
      if (checkedMatch || uncheckedMatch) {
        const checked = !!checkedMatch;
        const pattern = checked ? /^\\s*\\[x\\]\\s*/i : /^\\s*\\[ \\]\\s*/;
        li.innerHTML = text.replace(pattern, '');
        const cb = document.createElement('input');
        cb.type = 'checkbox';
        cb.disabled = true;
        cb.checked = checked;
        li.insertBefore(cb, li.firstChild);
        if (checked) {
          li.classList.add('task-done');
          // 包裹文字用于 line-through
          const span = document.createElement('span');
          while (li.childNodes.length > 1) {
            span.appendChild(li.childNodes[1]);
          }
          li.appendChild(span);
        }
        // 标记父 ul
        const ul = li.parentElement;
        if (ul && ul.tagName === 'UL') ul.classList.add('task-list');
      }
    });
  }

  // 渲染 terminal 代码块
  function renderTerminalBlocks() {
    document.querySelectorAll('pre > code.language-terminal').forEach(codeEl => {
      const pre = codeEl.parentElement;
      const content = codeEl.textContent;

      const container = document.createElement('div');
      container.className = 'terminal-block';

      // 从首行提取标题（如果首行是 # 注释）
      let title = 'Terminal';
      let body = content;
      const lines = content.split('\\n');
      if (lines[0] && lines[0].startsWith('# ')) {
        title = lines[0].slice(2).trim();
        body = lines.slice(1).join('\\n');
      }

      container.innerHTML =
        '<div class="terminal-header">' +
          '<span class="terminal-dot terminal-dot-r"></span>' +
          '<span class="terminal-dot terminal-dot-y"></span>' +
          '<span class="terminal-dot terminal-dot-g"></span>' +
          '<span class="terminal-title">' + title + '</span>' +
        '</div>' +
        '<pre class="terminal-body"><code>' + escapeHTML(body) + '</code></pre>';

      pre.parentNode.replaceChild(container, pre);
    });
  }

  // 渲染 flow 代码块
  // 含 ↓ 的块走竖向模式：主干列锁在 block 正中（grid 1fr/auto/1fr），
  //   横向扩展（→ 分支 / 注释）一律向右延伸，不影响主干对齐
  // 纯 → 的块走横向模式：整行居中
  function renderFlowBlocks() {
    const makeNode = text => {
      const node = document.createElement('span');
      const isDecision = text.includes('？') || text.includes('?');
      node.className = isDecision ? 'fc-decision' : 'fc-step';
      node.textContent = text;
      return node;
    };

    // 含 box-drawing / 树形绘制字符时，退化为 monospace 预格式化块
    const ASCII_ART_RE = /[│├└┌┐┘─━┃┏┓┗┛▼▲◀▶┼┤┬┴╭╮╯╰╱╲]/;

    document.querySelectorAll('pre > code.language-flow').forEach(codeEl => {
      const pre = codeEl.parentElement;
      const raw = codeEl.textContent.replace(/\\n+$/, '');

      // ASCII-art fallback：保留原排版，不拆 pill
      if (ASCII_ART_RE.test(raw)) {
        const block = document.createElement('pre');
        block.className = 'fc-block fc-block-ascii';
        const code = document.createElement('code');
        code.textContent = raw;
        block.appendChild(code);
        pre.parentNode.replaceChild(block, pre);
        return;
      }

      const lines = raw.split('\\n').filter(l => l.trim());

      const hasVArrow = lines.some(l => /^[↓↑]+$/.test(l.trim()));
      const container = document.createElement('div');
      container.className = 'fc-block ' + (hasVArrow ? 'fc-block-v' : 'fc-block-h');

      lines.forEach(line => {
        const trimmed = line.trim();

        // 竖向连接符
        if (/^[↓↑]+$/.test(trimmed)) {
          const arrow = document.createElement('div');
          arrow.className = 'fc-v-arrow';
          arrow.textContent = trimmed;
          container.appendChild(arrow);
          return;
        }

        const row = document.createElement('div');
        row.className = 'fc-row';

        // 横向流：首段是主干 leader，其余段向右延伸
        if (trimmed.includes('→')) {
          const parts = trimmed.split('→').map(s => s.trim()).filter(Boolean);
          const leader = makeNode(parts[0]);
          leader.classList.add('fc-leader');
          row.appendChild(leader);

          if (parts.length > 1) {
            const ext = document.createElement('div');
            ext.className = 'fc-ext';
            parts.slice(1).forEach(part => {
              const arrow = document.createElement('span');
              arrow.className = 'fc-h-arrow';
              arrow.textContent = '→';
              ext.appendChild(arrow);
              ext.appendChild(makeNode(part));
            });
            row.appendChild(ext);
          }
          container.appendChild(row);
          return;
        }

        // 普通步骤行（可能带括号注释）
        const noteMatch = trimmed.match(/^(.+?)([（(].+[）)])$/);
        if (noteMatch) {
          const leader = makeNode(noteMatch[1].trim());
          leader.classList.add('fc-leader');
          row.appendChild(leader);
          const note = document.createElement('div');
          note.className = 'fc-ext fc-note';
          note.textContent = noteMatch[2];
          row.appendChild(note);
        } else {
          const leader = makeNode(trimmed);
          leader.classList.add('fc-leader');
          row.appendChild(leader);
        }
        container.appendChild(row);
      });

      pre.parentNode.replaceChild(container, pre);
    });
  }

  // 给代码块添加语言标签
  function addCodeBlockLabels() {
    const LANG_DISPLAY = {
      js: 'JS', javascript: 'JS', ts: 'TS', typescript: 'TS',
      python: 'Python', py: 'Python', bash: 'Bash', sh: 'Shell', zsh: 'Shell',
      html: 'HTML', css: 'CSS', json: 'JSON', yaml: 'YAML', yml: 'YAML',
      sql: 'SQL', rust: 'Rust', go: 'Go', java: 'Java',
      markdown: 'MD', md: 'MD', xml: 'XML', toml: 'TOML',
      ruby: 'Ruby', php: 'PHP', swift: 'Swift', kotlin: 'Kotlin',
      c: 'C', cpp: 'C++', csharp: 'C#',
    };
    document.querySelectorAll('pre > code[class*="language-"]').forEach(codeEl => {
      const cls = [...codeEl.classList].find(c => c.startsWith('language-'));
      if (!cls) return;
      const lang = cls.replace('language-', '');
      // 跳过已处理的特殊语言
      if (['mermaid', 'terminal', 'flow'].includes(lang)) return;
      const label = LANG_DISPLAY[lang] || lang.toUpperCase();
      codeEl.parentElement.setAttribute('data-lang', label);
    });
  }

  function escapeHTML(str) {
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  // 渲染 Mermaid DSL 代码块
  async function renderDSLBlocks() {
    if (window.__mermaidReady) await window.__mermaidReady;

    const mermaidBlocks = document.querySelectorAll('pre > code.language-mermaid');
    if (mermaidBlocks.length > 0 && window.__mermaid) {
      let idx = 0;
      for (const codeEl of mermaidBlocks) {
        const pre = codeEl.parentElement;
        const src = codeEl.textContent;
        try {
          const id = 'mermaid-' + idx++;
          const { svg } = await window.__mermaid.render(id, src);
          const container = document.createElement('div');
          container.className = 'chart-container';
          container.innerHTML = '<div class="chart-inner">' + svg + '</div>';
          pre.parentNode.replaceChild(container, pre);
        } catch (e) {
          pre.style.borderLeft = '3px solid var(--c-danger)';
          pre.title = 'Mermaid 渲染失败: ' + e.message;
        }
      }
    }
  }

  // Mermaid 图表后处理 — 给无法通过 CSS nth-child 分色的图表元素上色
  const PALETTE = [
    { fill: '#DBEAFE', stroke: '#93C5FD', text: '#1E293B' },   // 蓝
    { fill: '#D1FAE5', stroke: '#6EE7B7', text: '#065F46' },   // 绿
    { fill: '#EDE9FE', stroke: '#C4B5FD', text: '#5B21B6' },   // 紫
    { fill: '#CFFAFE', stroke: '#67E8F9', text: '#155E75' },   // 青
    { fill: '#FECDD3', stroke: '#FDA4AF', text: '#9F1239' },   // 玫红
    { fill: '#FEF3C7', stroke: '#FCD34D', text: '#92400E' },   // 琥珀
  ];
  function colorizeMermaidCharts() {
    document.querySelectorAll('.chart-container svg').forEach(svg => {
      // 用 style 设置（内联样式优先级高于 themeCSS）
      function colorize(el, c) {
        el.style.fill = c.fill;
        el.style.stroke = c.stroke;
      }

      // 序列图 — 参与者分色（top + bottom）
      const actorTops = svg.querySelectorAll('rect.actor.actor-top');
      const actorBots = svg.querySelectorAll('rect.actor.actor-bottom');
      actorTops.forEach((rect, i) => colorize(rect, PALETTE[i % PALETTE.length]));
      actorBots.forEach((rect, i) => colorize(rect, PALETTE[i % PALETTE.length]));

      // 类图 — classId 节点分色
      svg.querySelectorAll('[id^="classId-"]').forEach((node, i) => {
        const c = PALETTE[i % PALETTE.length];
        node.querySelectorAll('.label-container, rect.basic').forEach(r => colorize(r, c));
      });

      // 状态图 — state 节点分色
      svg.querySelectorAll('[id^="state-"]:not([id*="start"]):not([id*="end"])').forEach((node, i) => {
        const c = PALETTE[i % PALETTE.length];
        node.querySelectorAll('.label-container, rect.basic').forEach(r => colorize(r, c));
      });

      // ER 图 — entity 节点分色
      svg.querySelectorAll('[id^="entity-"]').forEach((node, i) => {
        const c = PALETTE[i % PALETTE.length];
        node.querySelectorAll('.label-container, rect.basic').forEach(r => colorize(r, c));
      });

      // XY Chart — 柱状图条形 + 折线颜色
      // diagram skill 色板（实色，用于柱状图和折线图）
      const CHART_COLORS = ['#3B82F6', '#10B981', '#8B5CF6', '#F59E0B', '#F43F5E', '#0EA5E9'];
      const CHART_LIGHT = ['#DBEAFE', '#D1FAE5', '#EDE9FE', '#FEF3C7', '#FECDD3', '#CFFAFE'];

      // 检测 xychart：有 .background 类的 rect 且没有 .node
      const bgRect = svg.querySelector('rect.background');
      const hasNodes = svg.querySelector('.node');
      if (bgRect && !hasNodes) {
        // 柱状图 — 所有非背景/非轴线 rect
        const allRects = svg.querySelectorAll('rect:not(.background)');
        const barRects = [...allRects].filter(r => {
          const fill = r.getAttribute('fill');
          // 排除轴线区域的 rect（通常是透明或白色）
          return fill && fill !== '#ffffff' && fill !== 'none' && !r.getAttribute('class');
        });
        barRects.forEach((r, i) => {
          r.style.fill = CHART_COLORS[0];
          r.style.opacity = (0.65 + 0.35 * (i / Math.max(barRects.length - 1, 1))).toFixed(2);
          r.style.rx = '3';
          r.style.ry = '3';
        });

        // 折线图 — 非轴线的 path（排除 stroke="#1E293B" 的轴线）
        const allPaths = svg.querySelectorAll('path');
        let lineIdx = 0;
        allPaths.forEach(p => {
          const stroke = p.getAttribute('stroke');
          const fill = p.getAttribute('fill');
          if (stroke && stroke !== '#1E293B' && stroke !== 'none' && fill === 'none') {
            p.style.stroke = CHART_COLORS[lineIdx % CHART_COLORS.length];
            p.style.strokeWidth = '2.5px';
            lineIdx++;
          }
        });
      }
    });
  }

  // 转换 GitHub Alerts: > [!NOTE] 等
  function renderGitHubAlerts() {
    document.querySelectorAll('#content blockquote').forEach(bq => {
      const firstP = bq.querySelector('p');
      if (!firstP) return;
      const text = firstP.innerHTML;
      const match = text.match(/^\\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\\]\\s*/);
      if (!match) return;
      const type = match[1];
      const config = CALLOUT_TYPES[type];
      if (!config) return;
      // 转换为 callout
      const callout = document.createElement('div');
      callout.className = 'callout ' + config.cls;
      // 标题行
      const title = document.createElement('div');
      title.className = 'callout-title';
      title.innerHTML = config.icon + ' ' + config.label;
      callout.appendChild(title);
      // 移除 [!TYPE] 标记
      firstP.innerHTML = text.replace(match[0], '');
      if (!firstP.innerHTML.trim()) {
        firstP.remove();
      }
      // 移动内容
      while (bq.firstChild) {
        callout.appendChild(bq.firstChild);
      }
      bq.parentNode.replaceChild(callout, bq);
    });
  }

  async function renderMarkdown(md) {
    marked.setOptions({ gfm: true, breaks: false });

    const renderer = new marked.Renderer();
    const slugCounts = {};

    renderer.heading = function(text, level, raw) {
      var plain = (raw || text).replace(/<[^>]+>/g, '');
      var slug = plain.toLowerCase().replace(/[^\\w\\u4e00-\\u9fff]+/g, '-').replace(/(^-|-$)/g, '');
      if (slugCounts[slug] !== undefined) {
        slugCounts[slug]++;
        slug = slug + '-' + slugCounts[slug];
      } else {
        slugCounts[slug] = 0;
      }
      return '<h' + level + ' id="' + slug + '">' + text + '</h' + level + '>';
    };

    document.getElementById('content').innerHTML = marked.parse(md, { renderer });

    // 语法高亮（跳过 mermaid/terminal/flow 等自定义渲染块）
    const SKIP_LANGS = ['language-mermaid', 'language-terminal', 'language-flow'];
    document.querySelectorAll('pre code').forEach(block => {
      if (!SKIP_LANGS.some(cls => block.classList.contains(cls))) {
        hljs.highlightElement(block);
      }
    });

    // 后处理
    rewriteImagePaths();
    wrapImagesInFigure();
    renderTaskLists();
    renderGitHubAlerts();
    renderTerminalBlocks();
    renderFlowBlocks();
    await renderDSLBlocks();
    colorizeMermaidCharts();
    addCodeBlockLabels();

    // 生成目录
    const tocList = document.getElementById('toc');
    tocList.innerHTML = '';
    const headings = document.querySelectorAll('#content h1, #content h2, #content h3, #content h4');

    headings.forEach(h => {
      const depth = parseInt(h.tagName[1]);
      if (depth > 4) return;
      const li = document.createElement('li');
      li.className = 'toc-item' + (depth >= 2 ? ' depth-' + depth : '');
      const a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = h.textContent;
      a.dataset.id = h.id;
      li.appendChild(a);
      tocList.appendChild(li);
    });

    setupScrollHighlight();
  }

  function setupScrollHighlight() {
    const tocItems = document.querySelectorAll('.toc-item');
    const headings = document.querySelectorAll('#content h1, #content h2, #content h3, #content h4');

    function updateActiveLink() {
      let current = '';
      for (const h of headings) {
        const rect = h.getBoundingClientRect();
        if (rect.top <= 80) current = h.id;
      }
      tocItems.forEach(item => {
        const link = item.querySelector('a');
        if (link && link.dataset.id === current) {
          item.classList.add('active');
        } else {
          item.classList.remove('active');
        }
      });
    }

    window.removeEventListener('scroll', window._tocScrollHandler);
    window._tocScrollHandler = updateActiveLink;
    window.addEventListener('scroll', updateActiveLink, { passive: true });
    updateActiveLink();

    tocItems.forEach(item => {
      const link = item.querySelector('a');
      if (!link) return;
      link.addEventListener('click', e => {
        e.preventDefault();
        const target = document.getElementById(link.dataset.id);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          history.replaceState(null, '', '#' + link.dataset.id);
        }
      });
    });
  }

  async function loadAndRender() {
    const res = await fetch('/api/content?file=' + FILE_PATH);
    const md = await res.text();
    await renderMarkdown(md);
  }

  // 导出自包含 HTML（含渲染好的图表 + 目录 + 滚动高亮）
  function exportHTML() {
    // 克隆当前页面，移除不需要的元素
    const clone = document.documentElement.cloneNode(true);
    // 移除导出按钮、文件路径、SSE 脚本、Mermaid/marked CDN 脚本
    clone.querySelectorAll('.export-btn, .file-path, script').forEach(el => el.remove());
    // 注入目录滚动高亮脚本
    const tocScript = clone.ownerDocument.createElement('script');
    tocScript.textContent = '(' + function() {
      var items = document.querySelectorAll('.toc-item');
      var headings = document.querySelectorAll('#content h1,#content h2,#content h3,#content h4');
      function update() {
        var cur = '';
        for (var h of headings) { if (h.getBoundingClientRect().top <= 80) cur = h.id; }
        items.forEach(function(item) {
          var a = item.querySelector('a');
          item.classList.toggle('active', a && a.dataset.id === cur);
        });
      }
      window.addEventListener('scroll', update, { passive: true });
      update();
      items.forEach(function(item) {
        var a = item.querySelector('a');
        if (a) a.addEventListener('click', function(e) {
          e.preventDefault();
          var t = document.getElementById(a.dataset.id);
          if (t) t.scrollIntoView({ behavior: 'smooth' });
        });
      });
    } + ')();';
    clone.querySelector('body').appendChild(tocScript);

    const html = '<!DOCTYPE html>\\n' + clone.outerHTML;
    const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = document.title + '.html';
    a.click();
    URL.revokeObjectURL(a.href);
  }

  loadAndRender();

  const evtSource = new EventSource('/api/events?file=' + FILE_PATH);
  evtSource.onmessage = () => { loadAndRender(); };
</script>
</body>
</html>`;
}

// HTTP server
const server = createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');

  if (url.pathname === '/api/content' && req.method === 'GET') {
    const filePath = decodeURIComponent(url.searchParams.get('file') || '');
    try {
      const content = readFileSync(filePath, 'utf-8');
      res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end(content);
    } catch (err) {
      res.writeHead(500);
      res.end('读取文件失败: ' + err.message);
    }
  } else if (url.pathname === '/api/events' && req.method === 'GET') {
    const filePath = decodeURIComponent(url.searchParams.get('file') || '');
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    });
    res.write('\n');
    addSSEClient(filePath, res);
    req.on('close', () => removeSSEClient(filePath, res));
  } else if (url.pathname === '/api/watch' && req.method === 'POST') {
    // 注册新文件（来自后续脚本调用）
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const { file } = JSON.parse(body);
        registerFile(file);
        const port = server.address().port;
        const previewUrl = `http://127.0.0.1:${port}/preview?file=${encodeURIComponent(file)}`;
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ url: previewUrl }));
      } catch (err) {
        res.writeHead(400);
        res.end('Invalid request');
      }
    });
  } else if (url.pathname === '/preview' && req.method === 'GET') {
    const filePath = decodeURIComponent(url.searchParams.get('file') || '');
    if (!filePath || !existsSync(filePath)) {
      res.writeHead(404);
      res.end('文件不存在: ' + filePath);
      return;
    }
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(buildHTML(filePath));
  } else if (url.pathname === '/api/file' && req.method === 'GET') {
    // 静态文件服务：支持图片等资源加载
    const filePath = decodeURIComponent(url.searchParams.get('path') || '');
    if (!filePath || !existsSync(filePath)) {
      res.writeHead(404);
      res.end('文件不存在: ' + filePath);
      return;
    }
    try {
      const ext = extname(filePath).toLowerCase();
      const mime = MIME_TYPES[ext] || 'application/octet-stream';
      const content = readFileSync(filePath);
      res.writeHead(200, {
        'Content-Type': mime,
        'Cache-Control': 'public, max-age=300',
      });
      res.end(content);
    } catch (err) {
      res.writeHead(500);
      res.end('读取文件失败: ' + err.message);
    }
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

// 注册首个文件
registerFile(absPath);

// 启动 server
server.listen(0, '127.0.0.1', () => {
  const port = server.address().port;
  const previewUrl = `http://127.0.0.1:${port}/preview?file=${encodeURIComponent(absPath)}`;

  // 写入 lock 文件
  writeFileSync(LOCK_FILE, JSON.stringify({ port, pid: process.pid }), 'utf-8');

  console.log(`预览服务已启动: http://127.0.0.1:${port}`);
  console.log(`预览文件: ${absPath}`);
  console.log('所有浏览器关闭 1 分钟后自动退出');

  const cmd = process.platform === 'darwin' ? 'open' : 'xdg-open';
  exec(`${cmd} "${previewUrl}"`);
});

process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);
