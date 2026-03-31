"""生成 state L1-L4 测试 HTML 文件"""
import re
import os

# 确保 lib 软链接存在
if not os.path.exists('lib'):
    os.symlink('../templates/html/lib', 'lib')

# 读取模板
with open('../templates/html/state.html', 'r') as f:
    template = f.read()

# 提取引擎部分（从工具函数到文件末尾）
engine_match = re.search(r'(  // ========== 工具函数 ==========.*)</script>', template, re.DOTALL)
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

# L3: 10 states, 15 transitions, includes self-loop
L3 = '''
  // ========== 数据定义 ==========
  var title = '工单处理状态机';
  var subtitle = 'L3 复杂 · 10 状态 · 15 转换 · 含自循环';

  var states = [
    { id: 'start', label: '●', type: 'start' },
    { id: 'created', label: '已创建', type: 'state' },
    { id: 'assigned', label: '已分配', type: 'state' },
    { id: 'inprogress', label: '处理中', type: 'state' },
    { id: 'blocked', label: '已阻塞', type: 'state' },
    { id: 'review', label: '待审核', type: 'state' },
    { id: 'rejected', label: '已驳回', type: 'state' },
    { id: 'resolved', label: '已解决', type: 'state' },
    { id: 'closed', label: '已关闭', type: 'state' },
    { id: 'end', label: '◎', type: 'end' }
  ];

  var transitions = [
    { from: 'start', to: 'created', label: '提交工单' },
    { from: 'created', to: 'assigned', label: '分配处理人' },
    { from: 'assigned', to: 'inprogress', label: '开始处理' },
    { from: 'inprogress', to: 'inprogress', label: '更新进度' },
    { from: 'inprogress', to: 'blocked', label: '遇到阻塞' },
    { from: 'blocked', to: 'inprogress', label: '阻塞解除' },
    { from: 'inprogress', to: 'review', label: '提交审核' },
    { from: 'review', to: 'rejected', label: '审核不通过' },
    { from: 'review', to: 'resolved', label: '审核通过' },
    { from: 'rejected', to: 'inprogress', label: '重新处理' },
    { from: 'resolved', to: 'closed', label: '确认关闭' },
    { from: 'created', to: 'closed', label: '重复关闭' },
    { from: 'assigned', to: 'closed', label: '无需处理' },
    { from: 'blocked', to: 'closed', label: '无法解决' },
    { from: 'closed', to: 'end', label: '归档' }
  ];
'''

# L4: 14 states, 22 transitions, multiple paths to end
L4 = '''
  // ========== 数据定义 ==========
  var title = '电商退款全链路状态机';
  var subtitle = 'L4 超级复杂 · 14 状态 · 22 转换';

  var states = [
    { id: 'start', label: '●', type: 'start' },
    { id: 'submitted', label: '已提交', type: 'state' },
    { id: 'cs_review', label: '客服审核', type: 'state' },
    { id: 'merchant_review', label: '商家审核', type: 'state' },
    { id: 'return_shipping', label: '退货中', type: 'state' },
    { id: 'warehouse_check', label: '仓库验收', type: 'state' },
    { id: 'finance_review', label: '财务审批', type: 'state' },
    { id: 'refunding', label: '退款中', type: 'state' },
    { id: 'partial_refund', label: '部分退款', type: 'state' },
    { id: 'refunded', label: '已退款', type: 'state' },
    { id: 'rejected', label: '已拒绝', type: 'state' },
    { id: 'escalated', label: '已升级', type: 'state' },
    { id: 'cancelled', label: '已撤销', type: 'state' },
    { id: 'end', label: '◎', type: 'end' }
  ];

  var transitions = [
    { from: 'start', to: 'submitted', label: '发起退款' },
    { from: 'submitted', to: 'cs_review', label: '自动分配' },
    { from: 'submitted', to: 'cancelled', label: '用户撤销' },
    { from: 'cs_review', to: 'merchant_review', label: '转商家处理' },
    { from: 'cs_review', to: 'finance_review', label: '直接退款' },
    { from: 'cs_review', to: 'rejected', label: '不符合条件' },
    { from: 'merchant_review', to: 'return_shipping', label: '同意退货' },
    { from: 'merchant_review', to: 'rejected', label: '拒绝退款' },
    { from: 'merchant_review', to: 'finance_review', label: '仅退款' },
    { from: 'return_shipping', to: 'warehouse_check', label: '签收退货' },
    { from: 'return_shipping', to: 'cancelled', label: '超时未寄' },
    { from: 'warehouse_check', to: 'finance_review', label: '验收通过' },
    { from: 'warehouse_check', to: 'rejected', label: '验收不通过' },
    { from: 'finance_review', to: 'refunding', label: '审批通过' },
    { from: 'finance_review', to: 'partial_refund', label: '部分退款' },
    { from: 'finance_review', to: 'rejected', label: '审批拒绝' },
    { from: 'refunding', to: 'refunded', label: '到账成功' },
    { from: 'partial_refund', to: 'refunded', label: '到账成功' },
    { from: 'rejected', to: 'escalated', label: '用户申诉' },
    { from: 'escalated', to: 'cs_review', label: '重新审核' },
    { from: 'refunded', to: 'end', label: '完成' },
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
