#!/usr/bin/env python3
"""Generate GitHub-styled HTML preview of a markdown file with auto TOC sidebar, open in browser."""
import sys, os, re, html as html_mod, webbrowser, tempfile, hashlib

file_path = sys.argv[1] if len(sys.argv) > 1 else ""
if not file_path or not os.path.isfile(file_path):
    print(f"File not found: {file_path}", file=sys.stderr)
    sys.exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Try markdown module first
try:
    import markdown
    body = markdown.markdown(content, extensions=["fenced_code", "tables", "toc", "nl2br"])
except ImportError:
    # Fallback: manual conversion
    text = html_mod.escape(content)
    text = re.sub(r'^######\s+(.+)$', r'<h6>\1</h6>', text, flags=re.M)
    text = re.sub(r'^#####\s+(.+)$', r'<h5>\1</h5>', text, flags=re.M)
    text = re.sub(r'^####\s+(.+)$', r'<h4>\1</h4>', text, flags=re.M)
    text = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', text, flags=re.M)
    text = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', text, flags=re.M)
    text = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', text, flags=re.M)
    text = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code class="language-\1">\2</code></pre>', text, flags=re.S)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'^\- (.+)$', r'<li>\1</li>', text, flags=re.M)
    text = re.sub(r'(<li>.*?</li>\n?)+', r'<ul>\g<0></ul>', text, flags=re.S)
    text = re.sub(r'\n\n+', '</p>\n<p>', text)
    body = f'<p>{text}</p>'

# Add IDs to headings for TOC links, and build TOC
toc_items = []
def add_heading_id(match):
    tag = match.group(1)
    attrs = match.group(2) or ""
    text = match.group(3)
    clean = re.sub(r'<[^>]+>', '', text)
    slug = re.sub(r'[^\w\s-]', '', clean.lower()).strip()
    slug = re.sub(r'[\s]+', '-', slug)
    if not slug:
        slug = hashlib.md5(clean.encode()).hexdigest()[:8]
    level = int(tag[1])
    toc_items.append((level, clean, slug))
    return f'<{tag} id="{slug}"{attrs}>{text}</{tag}>'

body = re.sub(r'<(h[1-6])(\s[^>]*)?>(.+?)</\1>', add_heading_id, body)

# Build TOC HTML
toc_html = '<nav class="toc"><div class="toc-title">目录</div><ul>'
for level, text, slug in toc_items:
    indent = (level - 1) * 12
    toc_html += f'<li style="padding-left:{indent}px"><a href="#{slug}">{html_mod.escape(text)}</a></li>'
toc_html += '</ul></nav>'

title = os.path.basename(file_path)
html_content = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_mod.escape(title)}</title>
<style>
:root {{
  --color-fg: #1f2328;
  --color-fg-muted: #656d76;
  --color-bg: #ffffff;
  --color-bg-subtle: #f6f8fa;
  --color-border: #d0d7de;
  --color-accent: #0969da;
  --color-accent-fg: #0550ae;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
  font-size: 16px; line-height: 1.5; color: var(--color-fg); background: var(--color-bg);
  display: flex; min-height: 100vh;
}}
/* TOC sidebar */
.toc {{
  position: fixed; top: 0; left: 0; width: 280px; height: 100vh;
  overflow-y: auto; padding: 24px 16px; border-right: 1px solid var(--color-border);
  background: var(--color-bg-subtle); font-size: 14px; z-index: 10;
}}
.toc-title {{
  font-weight: 600; font-size: 14px; color: var(--color-fg); margin-bottom: 12px;
  padding-bottom: 8px; border-bottom: 1px solid var(--color-border);
  text-transform: uppercase; letter-spacing: 0.5px;
}}
.toc ul {{ list-style: none; }}
.toc li {{
  margin: 2px 0; border-radius: 6px;
}}
.toc li a {{
  display: block; padding: 4px 8px; color: var(--color-fg-muted);
  text-decoration: none; border-radius: 6px; transition: all 0.15s;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}}
.toc li a:hover {{ color: var(--color-accent); background: #e8ecf0; }}
.toc li a.active {{ color: var(--color-accent); background: #ddf4ff; font-weight: 500; }}
/* Main content */
.content {{
  margin-left: 280px; max-width: 880px; width: 100%; padding: 32px 40px;
}}
.file-header {{
  font-size: 14px; color: var(--color-fg-muted); padding: 8px 0 16px;
  border-bottom: 1px solid var(--color-border); margin-bottom: 24px;
}}
/* GitHub Markdown styles */
.content h1, .content h2, .content h3, .content h4, .content h5, .content h6 {{
  margin-top: 24px; margin-bottom: 16px; font-weight: 600; line-height: 1.25;
}}
.content h1 {{ font-size: 2em; padding-bottom: 0.3em; border-bottom: 1px solid var(--color-border); }}
.content h2 {{ font-size: 1.5em; padding-bottom: 0.3em; border-bottom: 1px solid var(--color-border); }}
.content h3 {{ font-size: 1.25em; }}
.content h4 {{ font-size: 1em; }}
.content p {{ margin-bottom: 16px; }}
.content a {{ color: var(--color-accent); text-decoration: none; }}
.content a:hover {{ text-decoration: underline; }}
.content ul, .content ol {{ padding-left: 2em; margin-bottom: 16px; }}
.content li {{ margin-bottom: 4px; }}
.content li + li {{ margin-top: 4px; }}
.content pre {{
  background: var(--color-bg-subtle); border: 1px solid var(--color-border);
  border-radius: 6px; padding: 16px; overflow-x: auto; margin-bottom: 16px;
  font-size: 85%; line-height: 1.45;
}}
.content code {{
  background: rgba(175,184,193,0.2); padding: 0.2em 0.4em; border-radius: 6px;
  font-size: 85%; font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
}}
.content pre code {{ background: none; padding: 0; font-size: 100%; border-radius: 0; }}
.content blockquote {{
  border-left: 4px solid var(--color-border); padding: 0 16px; color: var(--color-fg-muted);
  margin-bottom: 16px;
}}
.content table {{ border-collapse: collapse; width: 100%; margin-bottom: 16px; }}
.content th, .content td {{
  border: 1px solid var(--color-border); padding: 6px 13px;
}}
.content th {{ background: var(--color-bg-subtle); font-weight: 600; }}
.content tr:nth-child(2n) {{ background: var(--color-bg-subtle); }}
.content img {{ max-width: 100%; }}
.content hr {{ height: 4px; padding: 0; margin: 24px 0; background: var(--color-border); border: 0; border-radius: 2px; }}
/* Responsive */
@media (max-width: 768px) {{
  .toc {{ display: none; }}
  .content {{ margin-left: 0; padding: 16px; }}
}}
/* Scrollspy active highlight */
</style>
</head>
<body>
{toc_html}
<main class="content">
<div class="file-header">{html_mod.escape(os.path.abspath(file_path))}</div>
{body}
</main>
<script>
// Scrollspy: highlight current heading in TOC
(function() {{
  const links = document.querySelectorAll('.toc a');
  const headings = [];
  links.forEach(a => {{
    const id = a.getAttribute('href').slice(1);
    const el = document.getElementById(id);
    if (el) headings.push({{ el, a }});
  }});
  function update() {{
    let current = headings[0];
    for (const h of headings) {{
      if (h.el.getBoundingClientRect().top <= 80) current = h;
    }}
    links.forEach(a => a.classList.remove('active'));
    if (current) current.a.classList.add('active');
  }}
  window.addEventListener('scroll', update);
  update();
}})();
</script>
</body></html>"""

out = os.path.join(tempfile.gettempdir(), "claude-md-preview.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html_content)

webbrowser.open("file://" + out)
print(f"Opened preview: {out}")
