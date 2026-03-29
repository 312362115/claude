"""
质量检测封装 — 用 Playwright 执行 quality-check.js

对测试 HTML 逐个执行 DOM 质量检测，输出 pass/fail 汇总。

检测项（来自 quality-check.js）：
- A 级：画布存在、有尺寸、有内容
- B 级：节点不重叠、内容不越界、文字不截断、最小间距 ≥ 8px
- E 级：有标题、body inline-block、白色背景、配色规范

用法：
  python quality-check.py                    # 检测全部 HTML
  python quality-check.py class              # 只检测 class-L1~L4
  python quality-check.py class-L2           # 只检测 class-L2
"""

import sys
import os
import threading
import http.server
import socketserver
from pathlib import Path
from playwright.sync_api import sync_playwright

TESTS_DIR = Path(__file__).parent
QC_JS = TESTS_DIR / 'quality-check.js'
PORT = 18772
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


def main():
    filters = sys.argv[1:]

    # 读取 quality-check.js
    if not QC_JS.exists():
        print(f'Error: {QC_JS} not found')
        sys.exit(1)
    qc_script = QC_JS.read_text()

    # 扫描 HTML
    all_files = sorted([f.stem for f in TESTS_DIR.glob('*.html')])
    if filters:
        targets = [f for f in all_files if any(f == flt or f.startswith(flt + '-') for flt in filters)]
    else:
        targets = all_files

    if not targets:
        print('No matching HTML files found.')
        sys.exit(1)

    print(f'Quality check {len(targets)} files:\n')

    httpd = start_http_server(str(TESTS_DIR), PORT)

    total_pass = 0
    total_fail = 0
    failures = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(device_scale_factor=2)
        page = context.new_page()

        for f in targets:
            try:
                page.goto(f'http://localhost:{PORT}/{f}.html', wait_until='domcontentloaded', timeout=15000)
                page.wait_for_timeout(WAIT_MS)

                result = page.evaluate(qc_script)

                status = '\u2713 PASS' if result.get('pass') else '\u2717 FAIL'
                summary = result.get('summary', '?')
                nodes = result.get('nodeCount', 0)
                texts = result.get('textCount', 0)

                if result.get('pass'):
                    print(f'  {status}  {f}  ({summary}, {nodes} nodes, {texts} texts)')
                    total_pass += 1
                else:
                    errors = result.get('errors', [])
                    print(f'  {status}  {f}  ({summary})')
                    for err in errors:
                        print(f'         {err}')
                    total_fail += 1
                    failures.append(f)

            except Exception as e:
                print(f'  \u2717 ERROR  {f}: {e}')
                total_fail += 1
                failures.append(f)

        browser.close()

    httpd.shutdown()

    # 汇总
    print(f'\n{"=" * 50}')
    print(f'Total: {total_pass} passed, {total_fail} failed out of {len(targets)}')
    if failures:
        print(f'Failed: {", ".join(failures)}')
        sys.exit(1)
    else:
        print('All checks passed!')


if __name__ == '__main__':
    main()
