"""
图表回归测试截图脚本

遵循 SKILL.md 3.1-3.2 规范：
- body 元素截图（紧贴内容，无多余空白）
- deviceScaleFactor: 2（Retina 2x 清晰输出）
- PNG 格式

用法：
  python screenshot.py                    # 截全部 HTML
  python screenshot.py class              # 只截 class-L1~L4
  python screenshot.py class-L2           # 只截 class-L2
  python screenshot.py class fishbone     # 截 class + fishbone
"""

import sys
import os
import threading
import http.server
import socketserver
from pathlib import Path
from playwright.sync_api import sync_playwright

TESTS_DIR = Path(__file__).parent
OUTPUT_DIR = TESTS_DIR / '../../../docs/assets/diagram/tests'
PORT = 18770
DEVICE_SCALE_FACTOR = 2
WAIT_MS = 800  # ELKjs 异步布局等待时间


def start_http_server(directory, port):
    """启动本地 HTTP 服务"""
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(('', port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd


def main():
    filters = sys.argv[1:]

    # 扫描所有 HTML 测试文件
    all_files = sorted([
        f.stem for f in TESTS_DIR.glob('*.html')
    ])

    # 过滤
    if filters:
        targets = [
            f for f in all_files
            if any(f == flt or f.startswith(flt + '-') for flt in filters)
        ]
    else:
        targets = all_files

    if not targets:
        print('No matching HTML files found.')
        sys.exit(1)

    print(f'Will screenshot {len(targets)} files ({DEVICE_SCALE_FACTOR}x):')
    for f in targets:
        print(f'  {f}')

    # 确保输出目录存在
    output_dir = OUTPUT_DIR.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # 启动 HTTP 服务
    httpd = start_http_server(str(TESTS_DIR), PORT)
    print(f'HTTP server on port {PORT}')

    success = 0
    fail = 0

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(device_scale_factor=DEVICE_SCALE_FACTOR)
        page = context.new_page()

        for f in targets:
            try:
                page.goto(f'http://localhost:{PORT}/{f}.html', wait_until='domcontentloaded', timeout=15000)
                page.wait_for_timeout(WAIT_MS)

                out_path = str(output_dir / f'{f}.png')
                page.locator('body').screenshot(path=out_path, type='png')

                size_kb = os.path.getsize(out_path) / 1024
                print(f'  \u2713 {f}.png ({size_kb:.0f}KB)')
                success += 1
            except Exception as e:
                print(f'  \u2717 {f}: {e}')
                fail += 1

        browser.close()

    httpd.shutdown()
    print(f'\nDone: {success} succeeded, {fail} failed.')
    if fail > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
