"""生成 git-graph L1-L4 测试 HTML 文件"""
import re
import os

if not os.path.exists('lib'):
    os.symlink('../templates/html/lib', 'lib')

with open('../templates/html/git-graph.html', 'r') as f:
    template = f.read()

# 提取引擎（从 配色 到文件末尾）
engine_match = re.search(r'(  // ========== 配色（按 branch） ==========.*)</script>\n</body>\n</html>', template, re.DOTALL)
engine = engine_match.group(1)

header = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, system-ui, 'PingFang SC', sans-serif; background: #fff; display: flex; flex-direction: column; align-items: center; }
  .title { font-size: 22px; font-weight: 700; color: #1a1a2e; margin-top: 28px; }
  .subtitle { font-size: 14px; color: #888; margin-top: 6px; }
  .chart-wrap { margin-top: 20px; position: relative; }
</style>
<script src="lib/utils.js"></script>
</head>
<body>
<div class="title" id="title"></div>
<div class="subtitle" id="subtitle"></div>
<div class="chart-wrap">
  <svg id="canvas"></svg>
</div>
<script>
(function() {
  var svg = document.getElementById('canvas');
  var SANS = "-apple-system, system-ui, 'PingFang SC', sans-serif";

'''

tail = '</script>\n</body>\n</html>\n'

L1 = '''
  document.getElementById('title').textContent = '线性提交历史';
  document.getElementById('subtitle').textContent = 'L1 简单 · 1 分支 · 4 提交';
  var branches = ['main'];

  var commits = [
    { id: 'c1', message: 'Initial commit', branch: 'main' },
    { id: 'c2', message: 'Add README', branch: 'main', parent: 'c1' },
    { id: 'c3', message: 'Setup project', branch: 'main', parent: 'c2' },
    { id: 'c4', message: 'First feature', branch: 'main', parent: 'c3' }
  ];
'''

L2 = '''
  document.getElementById('title').textContent = '功能分支工作流';
  document.getElementById('subtitle').textContent = 'L2 中等 · 2 分支 · 6 提交 · 1 合并';
  var branches = ['main', 'feature/login'];

  var commits = [
    { id: 'c1', message: 'Initial commit', branch: 'main' },
    { id: 'c2', message: 'Setup CI', branch: 'main', parent: 'c1' },
    { id: 'c3', message: 'Add login page', branch: 'feature/login', parent: 'c2' },
    { id: 'c4', message: 'Add validation', branch: 'feature/login', parent: 'c3' },
    { id: 'c5', message: 'Update docs', branch: 'main', parent: 'c2' },
    { id: 'c6', message: 'Merge login', branch: 'main', parent: ['c5', 'c4'], merge: true }
  ];
'''

L3 = '''
  document.getElementById('title').textContent = 'Git 分支工作流';
  document.getElementById('subtitle').textContent = 'L3 复杂 · 3 分支 · 10 提交 · 2 合并';
  var branches = ['main', 'develop', 'feature/auth'];

  var commits = [
    { id: 'c1', message: 'Initial commit', branch: 'main' },
    { id: 'c2', message: 'Setup CI/CD', branch: 'main', parent: 'c1' },
    { id: 'c3', message: 'Create develop', branch: 'develop', parent: 'c2' },
    { id: 'c4', message: 'Add auth module', branch: 'feature/auth', parent: 'c3' },
    { id: 'c5', message: 'Implement JWT', branch: 'feature/auth', parent: 'c4' },
    { id: 'c6', message: 'Add middleware', branch: 'develop', parent: 'c3' },
    { id: 'c7', message: 'Auth tests', branch: 'feature/auth', parent: 'c5' },
    { id: 'c8', message: 'Merge auth', branch: 'develop', parent: ['c6', 'c7'], merge: true },
    { id: 'c9', message: 'Release prep', branch: 'develop', parent: 'c8' },
    { id: 'c10', message: 'v1.0.0', branch: 'main', parent: ['c2', 'c9'], merge: true }
  ];
'''

L4 = '''
  document.getElementById('title').textContent = '复杂分支拓扑';
  document.getElementById('subtitle').textContent = 'L4 超级复杂 · 5 分支 · 18 提交 · 4 合并';
  var branches = ['main', 'develop', 'feature/auth', 'feature/payment', 'hotfix/security'];

  var commits = [
    { id: 'c1', message: 'Initial commit', branch: 'main' },
    { id: 'c2', message: 'Setup CI/CD', branch: 'main', parent: 'c1' },
    { id: 'c3', message: 'Create develop', branch: 'develop', parent: 'c2' },
    { id: 'c4', message: 'Add auth module', branch: 'feature/auth', parent: 'c3' },
    { id: 'c5', message: 'Add payment SDK', branch: 'feature/payment', parent: 'c3' },
    { id: 'c6', message: 'Implement JWT', branch: 'feature/auth', parent: 'c4' },
    { id: 'c7', message: 'Payment gateway', branch: 'feature/payment', parent: 'c5' },
    { id: 'c8', message: 'Add middleware', branch: 'develop', parent: 'c3' },
    { id: 'c9', message: 'Auth tests', branch: 'feature/auth', parent: 'c6' },
    { id: 'c10', message: 'Merge auth', branch: 'develop', parent: ['c8', 'c9'], merge: true },
    { id: 'c11', message: 'Refund logic', branch: 'feature/payment', parent: 'c7' },
    { id: 'c12', message: 'Payment tests', branch: 'feature/payment', parent: 'c11' },
    { id: 'c13', message: 'Merge payment', branch: 'develop', parent: ['c10', 'c12'], merge: true },
    { id: 'c14', message: 'Fix XSS vuln', branch: 'hotfix/security', parent: 'c2' },
    { id: 'c15', message: 'Add CSP headers', branch: 'hotfix/security', parent: 'c14' },
    { id: 'c16', message: 'Hotfix merged', branch: 'main', parent: ['c2', 'c15'], merge: true },
    { id: 'c17', message: 'Release prep', branch: 'develop', parent: 'c13' },
    { id: 'c18', message: 'v2.0.0', branch: 'main', parent: ['c16', 'c17'], merge: true }
  ];
'''

test_data = {'L1': L1, 'L2': L2, 'L3': L3, 'L4': L4}

for level, data in test_data.items():
    content = header + data + '\n' + engine + tail
    filename = f'git-graph-{level}.html'
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
