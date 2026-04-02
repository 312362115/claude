#!/usr/bin/env python3
"""自动检测并安装 deep-research 技能所需的依赖。

处理 macOS externally-managed-environment 限制：
优先使用 venv，回退到 --user 安装。
"""

import subprocess
import sys
import os

# 虚拟环境路径
VENV_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.venv')
VENV_PYTHON = os.path.join(VENV_DIR, 'bin', 'python3')


def ensure_venv():
    """确保虚拟环境存在，返回 venv 中的 python 路径。"""
    if os.path.exists(VENV_PYTHON):
        return VENV_PYTHON

    print(f'正在创建虚拟环境: {VENV_DIR}')
    subprocess.check_call([sys.executable, '-m', 'venv', VENV_DIR])
    return VENV_PYTHON


def pip_install(python_path, package):
    """在指定 Python 环境中安装包。"""
    subprocess.check_call([python_path, '-m', 'pip', 'install', package, '-q'],
                          stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def check_and_install():
    """检测并安装依赖，返回安装结果摘要。"""
    results = {}

    # 确保 venv 存在
    python = ensure_venv()

    # 1. matplotlib
    ret = subprocess.run([python, '-c', 'import matplotlib; print(matplotlib.__version__)'],
                         capture_output=True, text=True)
    if ret.returncode == 0:
        results['matplotlib'] = f'已安装 (v{ret.stdout.strip()})'
    else:
        print('正在安装 matplotlib...')
        pip_install(python, 'matplotlib')
        ret = subprocess.run([python, '-c', 'import matplotlib; print(matplotlib.__version__)'],
                             capture_output=True, text=True)
        results['matplotlib'] = f'已安装 (v{ret.stdout.strip()})'

    # 2. numpy（matplotlib 依赖，但显式确认）
    ret = subprocess.run([python, '-c', 'import numpy; print(numpy.__version__)'],
                         capture_output=True, text=True)
    if ret.returncode == 0:
        results['numpy'] = f'已安装 (v{ret.stdout.strip()})'

    # 打印结果
    print(f'\n虚拟环境: {VENV_DIR}')
    print(f'Python: {python}')
    print('\n依赖检测结果:')
    for dep, status in results.items():
        print(f'  {dep}: {status}')

    return results


if __name__ == '__main__':
    check_and_install()
