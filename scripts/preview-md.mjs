#!/usr/bin/env node
/**
 * MD 预览工具：将 markdown 文件渲染为 GitHub 风格 HTML，左侧目录，浏览器打开。
 * 用法：node scripts/preview-md.mjs <path-to-md-file>
 */
import { readFileSync, writeFileSync, mkdtempSync } from 'fs';
import { resolve, basename } from 'path';
import { tmpdir } from 'os';
import { exec } from 'child_process';

const mdPath = process.argv[2];
if (!mdPath) {
  console.error('用法: node scripts/preview-md.mjs <markdown-file>');
  process.exit(1);
}

const absPath = resolve(mdPath);
const mdContent = readFileSync(absPath, 'utf-8');
const title = basename(absPath, '.md');

// 转义 JS 模板字符串中的特殊字符
const escaped = mdContent
  .replace(/\\/g, '\\\\')
  .replace(/`/g, '\\`')
  .replace(/\$/g, '\\$');

const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${title}</title>
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

  /* 左侧目录 */
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

  .toc-sidebar::-webkit-scrollbar {
    width: 4px;
  }

  .toc-sidebar::-webkit-scrollbar-thumb {
    background: #d0d7de;
    border-radius: 2px;
  }

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

  .toc-list {
    list-style: none;
    padding: 0;
  }

  .toc-list li {
    margin: 0;
  }

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

  .toc-list a:hover {
    color: #0969da;
    background: #f6f8fa;
  }

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

  /* 主内容 */
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

  /* 文件路径提示 */
  .file-path {
    max-width: none;
    margin: 0 0 12px;
    font-size: 12px;
    color: #656d76;
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace;
  }

  /* 响应式 */
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
      <div class="file-path">${absPath}</div>
      <article class="markdown-body" id="content"></article>
    </main>
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.1/marked.min.js"></script>
  <script>
    const md = \`${escaped}\`;

    // 渲染 markdown
    marked.setOptions({
      gfm: true,
      breaks: false,
    });

    // 自定义 heading renderer，给标题加 id
    const renderer = new marked.Renderer();
    const slugCounts = {};

    renderer.heading = function(text, level, raw) {
      // marked 12.x: heading(text, level, raw)
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

    // 生成目录
    const headings = document.querySelectorAll('#content h1, #content h2, #content h3, #content h4, #content h5, #content h6');
    const tocList = document.getElementById('toc');

    headings.forEach(h => {
      const depth = parseInt(h.tagName[1]);
      // 只展示 h1-h4
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

    // 滚动高亮当前目录项
    const tocLinks = document.querySelectorAll('.toc-list a');
    const headingElements = Array.from(headings).filter(h => parseInt(h.tagName[1]) <= 4);

    function updateActiveLink() {
      let current = '';
      for (const h of headingElements) {
        const rect = h.getBoundingClientRect();
        if (rect.top <= 80) {
          current = h.id;
        }
      }
      tocLinks.forEach(link => {
        link.classList.toggle('active', link.dataset.id === current);
      });
    }

    window.addEventListener('scroll', updateActiveLink, { passive: true });
    updateActiveLink();

    // 点击目录平滑滚动
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
  </script>
</body>
</html>`;

// 写入临时文件并打开
const tmpDir = mkdtempSync(resolve(tmpdir(), 'md-preview-'));
const htmlPath = resolve(tmpDir, `${title}.html`);
writeFileSync(htmlPath, html, 'utf-8');

// macOS 用 open，Linux 用 xdg-open
const cmd = process.platform === 'darwin' ? 'open' : 'xdg-open';
exec(`${cmd} "${htmlPath}"`, (err) => {
  if (err) {
    console.error('打开浏览器失败:', err.message);
    console.log('HTML 文件已生成:', htmlPath);
  } else {
    console.log('已在浏览器中打开:', htmlPath);
  }
});
