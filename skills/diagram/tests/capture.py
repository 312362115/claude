"""
单图截图工具 — 给 SKILL.md 生成流程用

遵循 SKILL.md 3.1-3.2 规范：
- body 元素截图（紧贴内容，无多余空白）
- deviceScaleFactor: 2（Retina 2x 清晰输出）
- PNG 格式

用法：
  python capture.py input.html output.png
  python capture.py input.html                # 默认输出同名 .png
  python capture.py input.html -s 3           # 3x 缩放
"""

import sys
import os
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
    handler.log_message = lambda *args: None  # 静默日志
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(('', port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd


def main():
    parser = argparse.ArgumentParser(description='HTML → PNG 截图（遵循 SKILL.md 规范）')
    parser.add_argument('input', help='输入 HTML 文件路径')
    parser.add_argument('output', nargs='?', help='输出 PNG 文件路径（默认同名 .png）')
    parser.add_argument('-s', '--scale', type=int, default=2, help='缩放倍数（默认 2x）')
    parser.add_argument('-w', '--wait', type=int, default=WAIT_MS, help='渲染等待时间 ms（默认 800）')
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f'Error: {input_path} not found')
        sys.exit(1)

    if args.output:
        output_path = Path(args.output).resolve()
    else:
        output_path = input_path.with_suffix('.png')

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 启动 HTTP 服务（在 HTML 所在目录）
    httpd = start_http_server(str(input_path.parent), PORT)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(device_scale_factor=args.scale)
        page = context.new_page()

        page.goto(f'http://localhost:{PORT}/{input_path.name}', wait_until='domcontentloaded', timeout=15000)
        page.wait_for_timeout(args.wait)

        page.locator('body').screenshot(path=str(output_path), type='png')
        browser.close()

    httpd.shutdown()

    size_kb = os.path.getsize(output_path) / 1024
    print(f'{output_path.name} ({size_kb:.0f}KB, {args.scale}x)')


if __name__ == '__main__':
    main()
