"""
一键全量回归 — 生成测试 HTML → 截图 → 质量检测 → 汇总报告

改完模板后跑这一条命令即可：
  python regression.py                    # 全量 11 图表 × 4 级
  python regression.py class fishbone     # 只跑指定类型
  python regression.py --skip-generate    # 跳过生成，只截图+检测
  python regression.py --skip-screenshot  # 跳过截图，只生成+检测
"""

import sys
import os
import subprocess
import time
import argparse
from pathlib import Path

TESTS_DIR = Path(__file__).parent

# 11 种图表类型
ALL_TYPES = [
    'architecture', 'class', 'er', 'fishbone', 'flowchart',
    'journey', 'sequence', 'state', 'swimlane', 'swot', 'venn'
]


def run_step(name, cmd, cwd=None):
    """执行一个步骤，返回 (success, output)"""
    print(f'\n{"=" * 50}')
    print(f'  {name}')
    print(f'{"=" * 50}')
    start = time.time()
    result = subprocess.run(
        cmd, cwd=cwd or str(TESTS_DIR),
        capture_output=True, text=True, timeout=300
    )
    elapsed = time.time() - start
    output = result.stdout + result.stderr
    print(output)
    success = result.returncode == 0
    status = '\u2713' if success else '\u2717'
    print(f'{status} {name} ({elapsed:.1f}s)')
    return success, output


def main():
    parser = argparse.ArgumentParser(description='图表回归测试一键流水线')
    parser.add_argument('types', nargs='*', help='图表类型过滤（默认全部）')
    parser.add_argument('--skip-generate', action='store_true', help='跳过生成测试 HTML')
    parser.add_argument('--skip-screenshot', action='store_true', help='跳过截图')
    parser.add_argument('--skip-check', action='store_true', help='跳过质量检测')
    args = parser.parse_args()

    types = args.types if args.types else ALL_TYPES
    # 验证类型名
    for t in types:
        if t not in ALL_TYPES:
            print(f'Warning: unknown type "{t}", available: {", ".join(ALL_TYPES)}')

    print(f'Regression test for: {", ".join(types)}')
    print(f'Steps: generate={not args.skip_generate}, screenshot={not args.skip_screenshot}, check={not args.skip_check}')

    results = {}
    overall_start = time.time()

    # Step 1: 生成测试 HTML
    if not args.skip_generate:
        for t in types:
            gen_script = TESTS_DIR / f'generate-{t}-tests.py'
            if gen_script.exists():
                ok, _ = run_step(
                    f'Generate {t} L1-L4',
                    [sys.executable, str(gen_script)]
                )
                results[f'generate-{t}'] = ok
            else:
                print(f'  Warning: {gen_script.name} not found, skipping')
                results[f'generate-{t}'] = None

    # Step 2: 截图
    if not args.skip_screenshot:
        ok, _ = run_step(
            f'Screenshot ({", ".join(types)})',
            [sys.executable, str(TESTS_DIR / 'screenshot.py')] + types
        )
        results['screenshot'] = ok

    # Step 3: 质量检测
    if not args.skip_check:
        ok, _ = run_step(
            f'Quality check ({", ".join(types)})',
            [sys.executable, str(TESTS_DIR / 'quality-check.py')] + types
        )
        results['quality-check'] = ok

    # 汇总报告
    total_time = time.time() - overall_start
    print(f'\n{"=" * 50}')
    print(f'  REGRESSION REPORT')
    print(f'{"=" * 50}')

    all_pass = True
    for step, ok in results.items():
        if ok is None:
            status = '- SKIP'
        elif ok:
            status = '\u2713 PASS'
        else:
            status = '\u2717 FAIL'
            all_pass = False
        print(f'  {status}  {step}')

    print(f'\nTotal time: {total_time:.1f}s')
    if all_pass:
        print('\u2713 All steps passed!')
    else:
        print('\u2717 Some steps failed.')
        sys.exit(1)


if __name__ == '__main__':
    main()
