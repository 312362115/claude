"""生成 state L1-L4 测试 HTML 文件"""
import re
import os

# 确保 lib 软链接存在
if not os.path.exists('lib'):
    os.symlink('../templates/html/lib', 'lib')

# 读取模板
with open('../templates/html/state.html', 'r') as f:
    template = f.read()

# 提取引擎部分（从常量到文件末尾）
engine_match = re.search(r'(  // ========== 常量 ==========.*)</script>', template, re.DOTALL)
engine = engine_match.group(1)

# 公共 HTML 头（含 ELKjs）
header = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, system-ui, 'PingFang SC', sans-serif;
    background: #ffffff;
    padding: 24px;
    display: inline-block;
  }
</style>
<script src="lib/elk.bundled.js"></script>
<script src="lib/utils.js"></script>
</head>
<body>
<svg id="canvas"></svg>

<script>
(function() {
  var NS = 'http://www.w3.org/2000/svg';
  var svg = document.getElementById('canvas');
  var SANS = "-apple-system, system-ui, 'PingFang SC', sans-serif";

'''

# L1: 4 states, 3 transitions (simple linear: start->A->B->end)
L1 = '''
  // ========== 数据定义 ==========
  var title = '简单审批流';
  var subtitle = 'L1 简单 · 4 状态 · 3 转换';

  var states = [
    { id: 'start', label: '●', type: 'start' },
    { id: 'draft', label: '草稿', type: 'state' },
    { id: 'approved', label: '已通过', type: 'state' },
    { id: 'end', label: '◎', type: 'end' }
  ];

  var transitions = [
    { from: 'start', to: 'draft', label: '创建' },
    { from: 'draft', to: 'approved', label: '审批通过' },
    { from: 'approved', to: 'end', label: '归档' }
  ];
'''

# L2: 8 states, 10 transitions (current default data)
L2 = '''
  // ========== 数据定义 ==========
  var title = '订单状态机';
  var subtitle = 'L2 中等 · 8 状态 · 10 转换';

  var states = [
    { id: 'start', label: '●', type: 'start' },
    { id: 'pending', label: '待支付', type: 'state' },
    { id: 'paid', label: '已支付', type: 'state' },
    { id: 'shipping', label: '配送中', type: 'state' },
    { id: 'delivered', label: '已签收', type: 'state' },
    { id: 'cancelled', label: '已取消', type: 'state' },
    { id: 'refunded', label: '已退款', type: 'state' },
    { id: 'end', label: '◎', type: 'end' }
  ];

  var transitions = [
    { from: 'start', to: 'pending', label: '创建订单' },
    { from: 'pending', to: 'paid', label: '支付成功' },
    { from: 'pending', to: 'cancelled', label: '超时取消' },
    { from: 'paid', to: 'shipping', label: '发货' },
    { from: 'paid', to: 'refunded', label: '申请退款' },
    { from: 'shipping', to: 'delivered', label: '签收' },
    { from: 'delivered', to: 'refunded', label: '退货退款' },
    { from: 'delivered', to: 'end', label: '完成' },
    { from: 'cancelled', to: 'end', label: '关闭' },
    { from: 'refunded', to: 'end', label: '关闭' }
  ];
'''

# L3: composite state + choice pseudo-state
L3 = '''
  // ========== 数据定义 ==========
  var title = 'TCP 连接状态机';
  var subtitle = 'L3 复杂 · composite 复合状态 + choice 伪状态';

  var states = [
    { id: 'start', label: '●', type: 'start' },
    { id: 'established', label: '已建立连接', type: 'composite', children: [
      { id: 'idle', label: '空闲', type: 'state' },
      { id: 'sending', label: '发送中', type: 'state' },
      { id: 'receiving', label: '接收中', type: 'state' }
    ]},
    { id: 'c1', label: '', type: 'choice' },
    { id: 'closing', label: '关闭中', type: 'state' },
    { id: 'error', label: '连接异常', type: 'state' },
    { id: 'end', label: '◎', type: 'end' }
  ];

  var transitions = [
    { from: 'start', to: 'established', label: '三次握手' },
    { from: 'idle', to: 'sending', label: '发送请求' },
    { from: 'sending', to: 'receiving', label: '等待响应' },
    { from: 'receiving', to: 'idle', label: '处理完成' },
    { from: 'established', to: 'c1', label: '断开' },
    { from: 'c1', to: 'closing', label: '[正常关闭]' },
    { from: 'c1', to: 'error', label: '[超时/异常]' },
    { from: 'closing', to: 'end', label: '四次挥手' },
    { from: 'error', to: 'end', label: '强制断开' }
  ];
'''

# L4: composite + choice + fork/join
L4 = '''
  // ========== 数据定义 ==========
  var title = '订单全链路状态机';
  var subtitle = 'L4 超级复杂 · composite + choice + fork/join';

  var states = [
    { id: 'start', label: '●', type: 'start' },
    { id: 'created', label: '已创建', type: 'state' },
    { id: 'c1', label: '', type: 'choice' },
    { id: 'payment', label: '支付处理', type: 'composite', children: [
      { id: 'validating', label: '验证中', type: 'state' },
      { id: 'charging', label: '扣款中', type: 'state' },
      { id: 'confirmed', label: '已确认', type: 'state' }
    ]},
    { id: 'fork1', label: '', type: 'fork' },
    { id: 'packing', label: '打包中', type: 'state' },
    { id: 'notifying', label: '通知中', type: 'state' },
    { id: 'join1', label: '', type: 'join' },
    { id: 'shipping', label: '配送中', type: 'state' },
    { id: 'delivered', label: '已签收', type: 'state' },
    { id: 'cancelled', label: '已取消', type: 'state' },
    { id: 'end', label: '◎', type: 'end' }
  ];

  var transitions = [
    { from: 'start', to: 'created', label: '下单' },
    { from: 'created', to: 'c1', label: '提交' },
    { from: 'c1', to: 'payment', label: '[在线支付]' },
    { from: 'c1', to: 'cancelled', label: '[取消订单]' },
    { from: 'validating', to: 'charging', label: '验证通过' },
    { from: 'charging', to: 'confirmed', label: '扣款成功' },
    { from: 'payment', to: 'fork1', label: '支付完成' },
    { from: 'fork1', to: 'packing', label: '仓库' },
    { from: 'fork1', to: 'notifying', label: '通知' },
    { from: 'packing', to: 'join1' },
    { from: 'notifying', to: 'join1' },
    { from: 'join1', to: 'shipping', label: '发货' },
    { from: 'shipping', to: 'delivered', label: '签收' },
    { from: 'delivered', to: 'end', label: '完成' },
    { from: 'cancelled', to: 'end', label: '关闭' }
  ];
'''

test_data = {
    'L1': L1,
    'L2': L2,
    'L3': L3,
    'L4': L4
}

for level, data in test_data.items():
    content = header + data + '\n' + engine + '</script>\n</body>\n</html>\n'
    filename = f'state-{level}.html'
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
