#!/usr/bin/env node
/**
 * MD 预览工具：全局单例 HTTP server + GitHub 风格渲染 + 左侧目录 + 文件监听自动刷新。
 * 用法：node scripts/preview-md.mjs <path-to-md-file>
 *
 * 首次调用启动 server，后续调用复用已有 server，直接打开新文件预览。
 * 所有浏览器标签关闭 1 分钟后 server 自动退出。
 */
import { readFileSync, watchFile, unwatchFile, existsSync, writeFileSync, unlinkSync } from 'fs';
import { createServer } from 'http';
import { resolve, basename } from 'path';
import { exec } from 'child_process';
import http from 'http';

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

// 生成预览页面 HTML
function buildHTML(filePath) {
  const fileTitle = basename(filePath, '.md');
  const encodedPath = encodeURIComponent(filePath);
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${fileTitle}</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown-light.min.css">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    background: #f6f8fa;
    color: #1f2328;
  }

  .layout {
    display: flex;
    min-height: 100vh;
  }

  .toc-sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 280px;
    height: 100vh;
    overflow-y: auto;
    background: #ffffff;
    border-right: 1px solid #d0d7de;
    padding: 20px 0;
    z-index: 10;
  }

  .toc-sidebar::-webkit-scrollbar { width: 4px; }
  .toc-sidebar::-webkit-scrollbar-thumb { background: #d0d7de; border-radius: 2px; }

  .toc-title {
    padding: 0 20px 12px;
    font-size: 13px;
    font-weight: 600;
    color: #656d76;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 1px solid #d0d7de;
    margin-bottom: 8px;
  }

  .toc-list { list-style: none; padding: 0; }
  .toc-list li { margin: 0; }

  .toc-list a {
    display: block;
    padding: 4px 20px;
    font-size: 13px;
    color: #656d76;
    text-decoration: none;
    line-height: 1.5;
    border-left: 2px solid transparent;
    transition: all 0.15s ease;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .toc-list a:hover { color: #0969da; background: #f6f8fa; }

  .toc-list a.active {
    color: #0969da;
    border-left-color: #0969da;
    background: #ddf4ff;
    font-weight: 500;
  }

  .toc-list a.depth-2 { padding-left: 20px; font-weight: 500; }
  .toc-list a.depth-3 { padding-left: 36px; }
  .toc-list a.depth-4 { padding-left: 52px; font-size: 12px; }
  .toc-list a.depth-5 { padding-left: 64px; font-size: 12px; }
  .toc-list a.depth-6 { padding-left: 76px; font-size: 12px; }

  .main-content {
    margin-left: 280px;
    flex: 1;
    padding: 32px 40px;
    max-width: 100%;
  }

  .markdown-body {
    max-width: none;
    margin: 0;
    background: #ffffff;
    padding: 40px 48px;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }

  .file-path {
    max-width: none;
    margin: 0 0 12px;
    font-size: 12px;
    color: #656d76;
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace;
  }

  @media (max-width: 1000px) {
    .toc-sidebar { width: 240px; }
    .main-content { margin-left: 240px; padding: 24px 20px; }
    .markdown-body { padding: 24px; }
  }

  @media (max-width: 720px) {
    .toc-sidebar { display: none; }
    .main-content { margin-left: 0; }
  }
</style>
</head>
<body>
  <div class="layout">
    <nav class="toc-sidebar">
      <div class="toc-title">目录</div>
      <ul class="toc-list" id="toc"></ul>
    </nav>
    <main class="main-content">
      <div class="file-path">${filePath}</div>
      <article class="markdown-body" id="content"></article>
    </main>
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.1/marked.min.js"></script>
  <script>
    const FILE_PATH = '${encodedPath}';

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

      const tocList = document.getElementById('toc');
      tocList.innerHTML = '';
      const headings = document.querySelectorAll('#content h1, #content h2, #content h3, #content h4');

      headings.forEach(h => {
        const depth = parseInt(h.tagName[1]);
        if (depth > 4) return;
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = '#' + h.id;
        a.textContent = h.textContent;
        a.className = 'depth-' + depth;
        a.dataset.id = h.id;
        li.appendChild(a);
        tocList.appendChild(li);
      });

      setupScrollHighlight();
    }

    function setupScrollHighlight() {
      const tocLinks = document.querySelectorAll('.toc-list a');
      const headings = document.querySelectorAll('#content h1, #content h2, #content h3, #content h4');

      function updateActiveLink() {
        let current = '';
        for (const h of headings) {
          const rect = h.getBoundingClientRect();
          if (rect.top <= 80) current = h.id;
        }
        tocLinks.forEach(link => {
          link.classList.toggle('active', link.dataset.id === current);
        });
      }

      window.removeEventListener('scroll', window._tocScrollHandler);
      window._tocScrollHandler = updateActiveLink;
      window.addEventListener('scroll', updateActiveLink, { passive: true });
      updateActiveLink();

      tocLinks.forEach(link => {
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
