"""
单图截图/导出工具 — 给 SKILL.md 生成流程用

遵循 SKILL.md 3.1-3.2 规范：
- body 元素截图（紧贴内容，无多余空白）
- deviceScaleFactor: 2（Retina 2x 清晰输出）
- PNG 格式（默认）或 HTML 自包含格式

用法：
  python capture.py input.html output.png          # 默认 PNG 截图
  python capture.py input.html                     # 默认输出同名 .png
  python capture.py input.html -f html             # 输出自包含 HTML（内联所有依赖）
  python capture.py input.html output.html -f html # 指定输出路径
  python capture.py input.html -s 3                # 3x 缩放（PNG 模式）
"""

import sys
import os
import re
import argparse
import threading
import http.server
import socketserver
from pathlib import Path
from playwright.sync_api import sync_playwright

PORT = 18771
WAIT_MS = 800


def start_http_server(directory, port):
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *args: None
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(('', port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd


def inline_html(input_path):
    """将 HTML 中的外部 CSS/JS 引用内联，生成自包含文件"""
    html = input_path.read_text(encoding='utf-8')
    base_dir = input_path.parent

    # 内联 <link rel="stylesheet" href="...">
    def replace_css(m):
        href = m.group(1)
        css_path = base_dir / href
        if css_path.exists():
            css = css_path.read_text(encoding='utf-8')
            return f'<style>\n{css}\n</style>'
        return m.group(0)

    html = re.sub(r'<link\s+rel="stylesheet"\s+href="([^"]+)"[^>]*>', replace_css, html)

    # 内联 <script src="..."></script>
    def replace_js(m):
        src = m.group(1)
        js_path = base_dir / src
        if js_path.exists():
            js = js_path.read_text(encoding='utf-8')
            return f'<script>\n{js}\n</script>'
        return m.group(0)

    html = re.sub(r'<script\s+src="([^"]+)">\s*</script>', replace_js, html)

    return html


def main():
    parser = argparse.ArgumentParser(description='HTML → PNG/HTML 导出')
    parser.add_argument('input', help='输入 HTML 文件路径')
    parser.add_argument('output', nargs='?', help='输出文件路径（默认同名 .png 或 .html）')
    parser.add_argument('-f', '--format', choices=['png', 'html'], default='png',
                        help='输出格式（默认 png）')
    parser.add_argument('-s', '--scale', type=int, default=2, help='缩放倍数（PNG 模式，默认 2x）')
    parser.add_argument('-w', '--wait', type=int, default=WAIT_MS, help='渲染等待时间 ms（默认 800）')
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f'Error: {input_path} not found')
        sys.exit(1)

    # 确定输出路径
    suffix = '.html' if args.format == 'html' else '.png'
    if args.output:
        output_path = Path(args.output).resolve()
    else:
        output_path = input_path.with_suffix(suffix)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format == 'html':
        # HTML 模式：内联所有外部依赖，输出自包含文件
        html = inline_html(input_path)
        output_path.write_text(html, encoding='utf-8')
        size_kb = os.path.getsize(output_path) / 1024
        print(f'{output_path.name} ({size_kb:.0f}KB, self-contained HTML)')
    else:
        # PNG 模式：Playwright 截图
        httpd = start_http_server(str(input_path.parent), PORT)

        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(device_scale_factor=args.scale)
            page = context.new_page()

            page.goto(f'http://localhost:{PORT}/{input_path.name}',
                      wait_until='domcontentloaded', timeout=15000)
            page.wait_for_timeout(args.wait)

            # ELKjs 异步布局等待
            try:
                page.wait_for_function(
                    '''() => {
                        const svg = document.querySelector('svg');
                        if (!svg) return true;
                        return svg.querySelectorAll('rect, path, line, circle').length > 5;
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
