#!/usr/bin/env python3
"""验证 deep-research → diagram skill 图表生成链路。

跑完即验证：bridge.py 10 种统计图 + capture.py 结构图截图链路均可用。

用法：
  python verify-chart-pipeline.py           # 全量验证
  python verify-chart-pipeline.py --quick   # 只验证 bridge.py（跳过截图）
"""

import subprocess
import json
import sys
import os
import tempfile
from pathlib import Path

BRIDGE = Path.home() / '.claude/skills/diagram/scripts/bridge.py'
CAPTURE = Path.home() / '.claude/skills/diagram/scripts/capture.py'
TESTS_HTML = Path.home() / '.claude/docs/assets/diagram/tests-html'

# 10 种统计图的最小配置
STAT_CONFIGS = {
    'bar': {'type': 'bar', 'title': 'Test Bar', 'data': {
        'categories': ['A', 'B', 'C'], 'series': [{'name': 's1', 'values': [10, 20, 30]}]}},
    'line': {'type': 'line', 'title': 'Test Line', 'data': {
        'categories': ['A', 'B', 'C'], 'series': [{'name': 's1', 'values': [10, 20, 15]}]}},
    'pie': {'type': 'pie', 'title': 'Test Pie', 'data': {
        'items': [{'name': 'A', 'value': 60}, {'name': 'B', 'value': 40}]}},
    'radar': {'type': 'radar', 'title': 'Test Radar', 'data': {
        'labels': ['X', 'Y', 'Z'], 'series': [{'name': 's1', 'values': [80, 60, 90]}]}},
    'heatmap': {'type': 'heatmap', 'title': 'Test Heatmap', 'data': {
        'xLabels': ['A', 'B'], 'yLabels': ['X', 'Y'],
        'data': [[0, 0, 5], [0, 1, 3], [1, 0, 7], [1, 1, 9]]}},
    'scatter': {'type': 'scatter', 'title': 'Test Scatter', 'data': {
        'xLabel': 'X', 'yLabel': 'Y',
        'series': [{'name': 's1', 'data': [[1, 2], [3, 4], [5, 6]]}]}},
    'funnel': {'type': 'funnel', 'title': 'Test Funnel', 'data': {
        'stages': [{'name': 'A', 'value': 100}, {'name': 'B', 'value': 60}, {'name': 'C', 'value': 30}]}},
    'waterfall': {'type': 'waterfall', 'title': 'Test Waterfall', 'data': {
        'items': [{'name': '起', 'value': 100, 'type': 'start'},
                  {'name': '+', 'value': 20, 'type': 'increase'},
                  {'name': '终', 'value': 120, 'type': 'total'}]}},
    'treemap': {'type': 'treemap', 'title': 'Test Treemap', 'data': {
        'items': [{'name': 'A', 'value': 60}, {'name': 'B', 'value': 40}]}},
    'combo': {'type': 'combo', 'title': 'Test Combo', 'data': {
        'categories': ['A', 'B', 'C'],
        'bars': [{'name': 'bar', 'values': [10, 20, 30]}],
        'lines': [{'name': 'line', 'values': [5, 15, 10]}]}},
}

# 29 种结构图全量验证（从 tests-html 取 L1）
STRUCT_ALL = [
    'architecture', 'c4', 'class', 'combo', 'dataflow', 'decision-tree',
    'er', 'fishbone', 'flowchart', 'funnel', 'gantt', 'git-graph',
    'heatmap', 'journey', 'kanban', 'mindmap', 'network', 'orgchart',
    'pie', 'radar', 'sankey', 'sequence', 'state', 'swimlane',
    'swot', 'timeline', 'treemap', 'venn', 'waterfall'
]


def verify_bridge(name, config, tmpdir, fmt='html'):
    """验证 bridge.py 生成一种图表"""
    cfg_path = os.path.join(tmpdir, f'{name}.json')
    ext = 'html' if fmt == 'html' else 'png'
    out_path = os.path.join(tmpdir, f'{name}.{ext}')

    with open(cfg_path, 'w') as f:
        json.dump(config, f, ensure_ascii=False)

    cmd = ['python3', str(BRIDGE), '-c', cfg_path, '-o', out_path, '-f', fmt]
    ret = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

    if ret.returncode != 0:
        return False, f'exit {ret.returncode}: {ret.stderr[:120]}'

    if not os.path.exists(out_path):
        return False, 'output file not created'

    size = os.path.getsize(out_path)
    if size < 100:
        return False, f'output too small ({size}B)'

    # HTML 模式检查是否包含 SVG
    if fmt == 'html':
        with open(out_path, 'r') as f:
            content = f.read()
        if '<svg' not in content:
            return False, 'no <svg> in HTML output'

    return True, f'{ext} {size // 1024}KB'


def verify_capture(name, tmpdir):
    """验证 capture.py 能截图结构图 HTML"""
    src = TESTS_HTML / f'{name}.html'
    if not src.exists():
        return False, f'{src.name} not found'

    out_path = os.path.join(tmpdir, f'{name}.png')
    cmd = ['python3', str(CAPTURE), str(src), out_path]
    ret = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

    if ret.returncode != 0:
        return False, f'exit {ret.returncode}: {ret.stderr[:120]}'

    if not os.path.exists(out_path):
        return False, 'PNG not created'

    size = os.path.getsize(out_path)
    if size < 1000:
        return False, f'PNG too small ({size}B)'

    return True, f'png {size // 1024}KB'


REPORT_DIR = Path.home() / '.claude/docs/tests'


def write_report(results, total, passed):
    """将验证结果写入 docs/tests/deep-research-chart-pipeline.md"""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    from datetime import datetime
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    lines = [
        f'# Deep-Research 图表生成链路验证',
        f'',
        f'> 最近执行：{now}',
        f'',
        f'## 结果：{passed}/{total} passed',
        f'',
    ]

    # 按类别分组
    categories = {}
    for key, (ok, msg) in results.items():
        cat = key.split('-', 1)[0]
        categories.setdefault(cat, []).append((key, ok, msg))

    cat_labels = {
        'bridge_html': '统计图 HTML（bridge.py → HTML）',
        'bridge_png': '统计图 PNG（bridge.py → PNG）',
        'capture': '结构图 PNG（capture.py → PNG）',
    }

    for cat, items in categories.items():
        label = cat_labels.get(cat, cat)
        cat_pass = sum(1 for _, ok, _ in items if ok)
        lines.append(f'### {label}（{cat_pass}/{len(items)}）')
        lines.append('')
        lines.append('| 图表类型 | 状态 | 详情 |')
        lines.append('|---------|------|------|')
        for key, ok, msg in items:
            name = key.split('-', 1)[1] if '-' in key else key
            status = '✅' if ok else '❌'
            lines.append(f'| {name} | {status} | {msg} |')
        lines.append('')

    lines.append('## 执行命令')
    lines.append('')
    lines.append('```bash')
    lines.append('python skills/deep-research/tests/verify-chart-pipeline.py        # 全量')
    lines.append('python skills/deep-research/tests/verify-chart-pipeline.py --quick # 仅 HTML')
    lines.append('```')

    report_path = REPORT_DIR / 'deep-research-chart-pipeline.md'
    with open(report_path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'\n报告已写入: {report_path}')


def main():
    quick = '--quick' in sys.argv

    with tempfile.TemporaryDirectory(prefix='chart-verify-') as tmpdir:
        results = {}  # key → (ok, msg)
        total = 0
        passed = 0

        # ── bridge.py HTML 输出（10 种统计图）──
        print('=== bridge.py → HTML (10 种统计图) ===')
        for name, config in STAT_CONFIGS.items():
            total += 1
            ok, msg = verify_bridge(name, config, tmpdir, 'html')
            status = '✓' if ok else '✗'
            print(f'  {status} {name:12s} {msg}')
            results[f'bridge_html-{name}'] = (ok, msg)
            if ok:
                passed += 1

        # ── bridge.py PNG 输出（抽样 3 种）──
        if not quick:
            print('\n=== bridge.py → PNG (抽样 3 种) ===')
            for name in ['bar', 'pie', 'radar']:
                total += 1
                ok, msg = verify_bridge(name, STAT_CONFIGS[name], tmpdir, 'png')
                status = '✓' if ok else '✗'
                print(f'  {status} {name:12s} {msg}')
                results[f'bridge_png-{name}'] = (ok, msg)
                if ok:
                    passed += 1

        # ── capture.py 结构图截图（29 种全量）──
        if not quick:
            print(f'\n=== capture.py → PNG (29 种结构图) ===')
            for t in STRUCT_ALL:
                name = f'{t}-L1'
                total += 1
                ok, msg = verify_capture(name, tmpdir)
                status = '✓' if ok else '✗'
                print(f'  {status} {name:20s} {msg}')
                results[f'capture-{name}'] = (ok, msg)
                if ok:
                    passed += 1

        # ── 汇总 ──
        print(f'\n{"=" * 40}')
        print(f'  {passed}/{total} passed')
        if passed == total:
            print('  ✓ 图表生成链路全部正常')
        else:
            failed = [k for k, (v, _) in results.items() if not v]
            print(f'  ✗ 失败项: {", ".join(failed)}')

        # 写入报告
        write_report(results, total, passed)

        if passed != total:
            sys.exit(1)


if __name__ == '__main__':
    main()
