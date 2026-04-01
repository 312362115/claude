from pathlib import Path
"""生成 swimlane L1-L4 测试 HTML 文件"""
import re

OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / 'docs' / 'assets' / 'diagram' / 'tests' / 'html'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 读取模板
with open('../templates/html/swimlane.html', 'r') as f:
    template = f.read()

# 提取引擎部分（从 theme 定义到文件末尾）
engine_match = re.search(r'(  // ========== 主题 ==========.*)</script>', template, re.DOTALL)
engine = engine_match.group(1)

# 公共 HTML 头
header = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="lib/base.css">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, system-ui, 'PingFang SC', sans-serif;
    background: #ffffff;
    padding: 24px;
    display: inline-block;
  }
</style>
</head>
<body>
<svg id="canvas"></svg>

<script src="lib/utils.js"></script>
<script>
(function() {
  var NS = 'http://www.w3.org/2000/svg';
  var svg = document.getElementById('canvas');

'''

# L1: 简单（2 泳道，4 步，无决策）
L1 = '''
  var title = '简单审批流程';
  var subtitle = 'L1 简单 · 2 泳道 · 4 步';

  var lanes = [
    { id: 'applicant', label: '申请人' },
    { id: 'approver', label: '审批人' }
  ];

  var steps = [
    { id: 's1', label: '提交申请', lane: 'applicant', type: 'start' },
    { id: 's2', label: '审核材料', lane: 'approver', type: 'process' },
    { id: 's3', label: '批准通过', lane: 'approver', type: 'success' },
    { id: 'end', label: '完成', lane: 'applicant', type: 'end' }
  ];

  var sideNodes = [];
'''

# L2: 中等（4 泳道，9 步，1 决策）— 模板默认数据
L2 = '''
  var title = '用户注册流程';
  var subtitle = 'L2 中等 · 4 泳道 · 9 步 · 1 决策';

  var lanes = [
    { id: 'user', label: '用户' },
    { id: 'frontend', label: '前端' },
    { id: 'backend', label: '后端' },
    { id: 'db', label: '数据库' }
  ];

  var steps = [
    { id: 's1', label: '提交表单', lane: 'user', type: 'start' },
    { id: 's2', label: '表单校验', lane: 'frontend', type: 'process' },
    { id: 'd1', label: '校验通过?', lane: 'frontend', type: 'decision', no: 'e1' },
    { id: 's3', label: '调用 API', lane: 'frontend', type: 'process' },
    { id: 's4', label: '业务处理', lane: 'backend', type: 'process' },
    { id: 's5', label: '写入数据', lane: 'db', type: 'datastore' },
    { id: 's6', label: '返回结果', lane: 'backend', type: 'process' },
    { id: 's7', label: '显示成功', lane: 'frontend', type: 'success' },
    { id: 'end', label: '完成', lane: 'user', type: 'end' }
  ];

  var sideNodes = [
    { id: 'e1', label: '显示错误', type: 'error', lane: 'frontend' }
  ];
'''

# L3: 复杂（4 泳道，12 步，2 决策 + 侧节点）
L3 = '''
  var title = '订单处理流程';
  var subtitle = 'L3 复杂 · 4 泳道 · 12 步 · 2 决策';

  var lanes = [
    { id: 'customer', label: '客户' },
    { id: 'frontend', label: '前端' },
    { id: 'order_svc', label: '订单服务' },
    { id: 'pay_svc', label: '支付服务' }
  ];

  var steps = [
    { id: 's1', label: '选购商品', lane: 'customer', type: 'start' },
    { id: 's2', label: '加入购物车', lane: 'frontend', type: 'process' },
    { id: 's3', label: '提交订单', lane: 'frontend', type: 'highlight' },
    { id: 'd1', label: '库存充足?', lane: 'order_svc', type: 'decision', no: 'e1' },
    { id: 's4', label: '创建订单', lane: 'order_svc', type: 'process' },
    { id: 's5', label: '锁定库存', lane: 'order_svc', type: 'datastore' },
    { id: 's6', label: '发起支付', lane: 'pay_svc', type: 'process' },
    { id: 'd2', label: '支付成功?', lane: 'pay_svc', type: 'decision', no: 'e2' },
    { id: 's7', label: '更新状态', lane: 'order_svc', type: 'process' },
    { id: 's8', label: '发送通知', lane: 'order_svc', type: 'process' },
    { id: 's9', label: '显示结果', lane: 'frontend', type: 'success' },
    { id: 'end', label: '完成', lane: 'customer', type: 'end' }
  ];

  var sideNodes = [
    { id: 'e1', label: '库存不足', type: 'error', lane: 'order_svc' },
    { id: 'e2', label: '支付失败', type: 'error', lane: 'pay_svc' }
  ];
'''

# L4: 超级复杂（5 泳道，15 步，3 决策）
L4 = '''
  var title = '电商退货退款流程';
  var subtitle = 'L4 超级复杂 · 5 泳道 · 15 步 · 3 决策';

  var lanes = [
    { id: 'customer', label: '客户' },
    { id: 'cs', label: '客服' },
    { id: 'warehouse', label: '仓库' },
    { id: 'finance', label: '财务' },
    { id: 'system', label: '系统' }
  ];

  var steps = [
    { id: 's1', label: '申请退货', lane: 'customer', type: 'start' },
    { id: 's2', label: '提交工单', lane: 'system', type: 'process' },
    { id: 'd1', label: '审核通过?', lane: 'cs', type: 'decision', no: 'e1' },
    { id: 's3', label: '生成退货单', lane: 'system', type: 'process' },
    { id: 's4', label: '寄回商品', lane: 'customer', type: 'process' },
    { id: 's5', label: '签收入库', lane: 'warehouse', type: 'datastore' },
    { id: 'd2', label: '商品完好?', lane: 'warehouse', type: 'decision', no: 'e2' },
    { id: 's6', label: '确认退货', lane: 'warehouse', type: 'success' },
    { id: 's7', label: '发起退款', lane: 'finance', type: 'highlight' },
    { id: 's8', label: '调用支付渠道', lane: 'system', type: 'process' },
    { id: 'd3', label: '退款成功?', lane: 'system', type: 'decision', no: 'e3' },
    { id: 's9', label: '更新订单状态', lane: 'system', type: 'process' },
    { id: 's10', label: '发送通知', lane: 'system', type: 'process' },
    { id: 's11', label: '确认到账', lane: 'customer', type: 'success' },
    { id: 'end', label: '完成', lane: 'customer', type: 'end' }
  ];

  var sideNodes = [
    { id: 'e1', label: '审核拒绝', type: 'error', lane: 'cs' },
    { id: 'e2', label: '商品损坏', type: 'error', lane: 'warehouse' },
    { id: 'e3', label: '退款异常', type: 'error', lane: 'system' }
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
    filename = f'swimlane-{level}.html'
    with open(str(OUTPUT_DIR / filename), 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
