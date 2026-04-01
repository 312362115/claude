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

.pdf-btn {
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
.pdf-btn:hover { background: var(--c-border-light); border-color: var(--c-primary); color: var(--c-primary); }
.pdf-btn svg { width: 16px; height: 16px; fill: currentColor; }

@media print {
  .pdf-btn, .file-path { display: none !important; }
}
</style>
</head>
<body>

<nav class="sidebar">
  <div class="sidebar-title">目录</div>
  <ul class="toc-list" id="toc"></ul>
</nav>

<button class="pdf-btn" onclick="window.print()" title="下载为 PDF">
  <svg viewBox="0 0 16 16"><path d="M4.75 7.5a.75.75 0 000 1.5h6.5a.75.75 0 000-1.5h-6.5zM4.75 10.5a.75.75 0 000 1.5h4.5a.75.75 0 000-1.5h-4.5zM13.5 1h-11A1.5 1.5 0 001 2.5v11A1.5 1.5 0 002.5 15h11a1.5 1.5 0 001.5-1.5v-11A1.5 1.5 0 0013.5 1zm0 1.5v2h-11v-2h11zm-11 11V6h11v7.5h-11z"/></svg>
  下载 PDF
</button>

<main class="content">
  <div class="file-path">${filePath}</div>
  <article id="content"></article>
</main>

<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.1/marked.min.js"></script>
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

  function renderMarkdown(md) {
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

    // 后处理
    rewriteImagePaths();
    wrapImagesInFigure();
    renderTaskLists();
    renderGitHubAlerts();

    // 生成目录
    const tocList = document.getElementById('toc');
    tocList.innerHTML = '';
    const headings = document.querySelectorAll('#content h1, #content h2, #content h3, #content h4');

    headings.forEach(h => {
      const depth = parseInt(h.tagName[1]);
      if (depth > 4) return;
      const li = document.createElement('li');
      li.className = 'toc-item' + (depth >= 3 ? ' depth-' + depth : '');
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
    renderMarkdown(md);
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
