from pathlib import Path
"""生成 flowchart L1-L6 测试 HTML 文件（L1-L4 线性模式，L5-L6 DAG 模式）"""
import re

OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / 'docs' / 'assets' / 'diagram' / 'tests' / 'html'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 读取模板
with open('../templates/html/flowchart.html', 'r') as f:
    template = f.read()

# 提取引擎部分（从 theme 定义到文件末尾）
engine_match = re.search(r'(  // ========== 主题 ==========.*)</script>', template, re.DOTALL)
engine = engine_match.group(1)

# 公共 HTML 头（线性模式）
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

# DAG 模式 HTML 头（包含 ELKjs）
header_dag = '''<!DOCTYPE html>
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
<script src="lib/elk.bundled.js"></script>
<script>
(function() {
  var NS = 'http://www.w3.org/2000/svg';
  var svg = document.getElementById('canvas');

'''

# L1: 简单（4 步，0 判断，无分组）
L1 = '''
  var title = '数据备份流程';
  var subtitle = 'L1 简单 · 4 步 · 0 判断';
  var groups = null;
  var steps = [
    { id: 'start', label: '触发备份', type: 'start' },
    { id: 's1', label: '导出数据库快照', type: 'highlight' },
    { id: 's2', label: '上传至 OSS', type: 'external' },
    { id: 'end', label: '备份完成', type: 'end' }
  ];
  var sideNodes = [];
'''

# L2: 中等（8 步，2 判断，3 分组）
L2 = '''
  var title = '订单处理流程';
  var subtitle = 'L2 中等 · 10 步 · 2 判断 · 3 分组';
  var groups = [
    { label: '用户端', steps: [
      { id: 'start', label: '用户提交订单', type: 'start' },
      { id: 's1', label: '订单参数校验', type: 'process' },
      { id: 'd1', label: '参数合法?', type: 'decision', no: 'e1' }
    ]},
    { label: '订单服务', steps: [
      { id: 's2', label: '库存检查', type: 'process' },
      { id: 'd2', label: '库存充足?', type: 'decision', no: 'e2' },
      { id: 's3', label: '创建订单记录', type: 'highlight' },
      { id: 's4', label: '写入订单数据库', type: 'datastore' }
    ]},
    { label: '通知服务', steps: [
      { id: 's5', label: '发送订单确认通知', type: 'process' },
      { id: 's6', label: '推送站内消息', type: 'process' },
      { id: 'end', label: '订单完成', type: 'end' }
    ]}
  ];
  var steps = null;
  var sideNodes = [
    { id: 'e1', label: '返回参数错误', type: 'error' },
    { id: 'e2', label: '退回库存不足', type: 'error' }
  ];
'''

# L3: 复杂（12 步，3 判断，无分组，含侧分支子流程）
L3 = '''
  var title = '用户注册与实名认证';
  var subtitle = 'L3 复杂 · 12 步 · 3 判断 · 含侧分支子流程';
  var groups = null;
  var steps = [
    { id: 'start', label: '用户点击注册', type: 'start' },
    { id: 's1', label: '填写基本信息', type: 'process' },
    { id: 's2', label: '发送验证码', type: 'process' },
    { id: 'd1', label: '验证码正确?', type: 'decision', no: 'e1' },
    { id: 's3', label: '创建用户账号', type: 'highlight' },
    { id: 's4', label: '写入用户数据库', type: 'datastore' },
    { id: 's5', label: '上传身份证照片', type: 'process' },
    { id: 'd2', label: 'OCR 识别成功?', type: 'decision', no: 'e2' },
    { id: 's6', label: '调用公安实名接口', type: 'external' },
    { id: 'd3', label: '实名验证通过?', type: 'decision', no: 'e3' },
    { id: 's7', label: '标记账号已实名', type: 'highlight' },
    { id: 'end', label: '注册完成', type: 'end' }
  ];
  var sideNodes = [
    { id: 'e1', label: '提示验证码错误', type: 'error' },
    { id: 'e2', label: '提示照片模糊', type: 'error',
      next: [
        { label: '记录失败日志', type: 'process' }
      ]
    },
    { id: 'e3', label: '实名失败', type: 'error',
      next: [
        { label: '进入人工审核', type: 'process' },
        { label: '通知安全团队', type: 'process' }
      ]
    }
  ];
'''

# L4: 超级复杂（15 步，4 判断，4 分组，含侧分支子流程）
L4 = '''
  var title = '电商订单全链路处理';
  var subtitle = 'L4 超级复杂 · 15 步 · 4 判断 · 4 分组';
  var groups = [
    { label: '用户端', steps: [
      { id: 'start', label: '用户点击下单', type: 'start' },
      { id: 's1', label: '前端表单校验', type: 'process' },
      { id: 'd1', label: '校验通过?', type: 'decision', no: 'e1' }
    ]},
    { label: '风控系统', steps: [
      { id: 's2', label: '调用风控接口', type: 'external' },
      { id: 'd2', label: '风控评分≥60?', type: 'decision', no: 'e2' }
    ]},
    { label: '订单服务', steps: [
      { id: 's3', label: '锁定库存', type: 'highlight' },
      { id: 's4', label: '写入订单表', type: 'datastore' },
      { id: 's5', label: '调用支付网关', type: 'external' },
      { id: 'd3', label: '支付成功?', type: 'decision', no: 'e3' },
      { id: 's6', label: '更新订单状态', type: 'process' }
    ]},
    { label: '物流与通知', steps: [
      { id: 's7', label: '推送物流中台', type: 'process' },
      { id: 's8', label: '生成电子发票', type: 'process' },
      { id: 'd4', label: '物流分配成功?', type: 'decision', no: 'e4' },
      { id: 's9', label: '发送确认短信', type: 'highlight' },
      { id: 'end', label: '订单完成', type: 'end' }
    ]}
  ];
  var steps = null;
  var sideNodes = [
    { id: 'e1', label: '提示校验错误', type: 'error' },
    { id: 'e2', label: '转人工审核', type: 'error',
      next: [{ label: '冻结账号', type: 'error' }]
    },
    { id: 'e3', label: '释放库存', type: 'process',
      next: [
        { label: '标记支付失败', type: 'error' },
        { label: '发送失败通知', type: 'process' }
      ]
    },
    { id: 'e4', label: '物流异常队列', type: 'error',
      next: [{ label: '触发运维告警', type: 'process' }]
    }
  ];
'''

# L5: DAG 简单（多根节点 + 汇聚，3 个独立入口）
L5 = '''
  var title = '多渠道获客转化';
  var subtitle = 'L5 DAG · 3 入口 · 汇聚 · 9 节点';
  var dagMode = true;
  var nodes = [
    { id: 'sem', label: 'SEM 投放', type: 'start' },
    { id: 'seo', label: 'SEO 自然流量', type: 'start' },
    { id: 'ref', label: '老客推荐', type: 'start' },
    { id: 'land', label: '落地页', type: 'process' },
    { id: 'reg', label: '注册转化', type: 'process' },
    { id: 'trial', label: '试用体验', type: 'process' },
    { id: 'pay', label: '付费转化', type: 'success' },
    { id: 'crm', label: 'CRM 客户池', type: 'datastore' },
    { id: 'churn', label: '流失召回', type: 'external' }
  ];
  var edges = [
    { from: 'sem', to: 'land', label: '广告点击' },
    { from: 'seo', to: 'land', label: '搜索进入' },
    { from: 'ref', to: 'reg', label: '邀请码' },
    { from: 'land', to: 'reg' },
    { from: 'reg', to: 'trial' },
    { from: 'trial', to: 'pay', label: '转化' },
    { from: 'trial', to: 'churn', label: '流失' },
    { from: 'pay', to: 'crm' },
    { from: 'churn', to: 'reg', label: '召回' }
  ];
  var steps = null;
  var groups = null;
  var sideNodes = [];
'''

# L6: DAG 复杂（多根 + 汇聚 + 多终点）
L6 = '''
  var title = '微服务请求链路';
  var subtitle = 'L6 DAG 复杂 · 多根 + 汇聚 + 12 节点';
  var dagMode = true;
  var nodes = [
    { id: 'web', label: 'Web 客户端', type: 'start' },
    { id: 'mobile', label: 'Mobile 客户端', type: 'start' },
    { id: 'gw', label: 'API Gateway', type: 'highlight' },
    { id: 'auth', label: '认证服务', type: 'process' },
    { id: 'user', label: '用户服务', type: 'process' },
    { id: 'order', label: '订单服务', type: 'process' },
    { id: 'pay', label: '支付服务', type: 'external' },
    { id: 'db_user', label: 'User DB', type: 'datastore' },
    { id: 'db_order', label: 'Order DB', type: 'datastore' },
    { id: 'cache', label: 'Redis 缓存', type: 'datastore' },
    { id: 'mq', label: '消息队列', type: 'process' },
    { id: 'notify', label: '通知服务', type: 'success' }
  ];
  var edges = [
    { from: 'web', to: 'gw' },
    { from: 'mobile', to: 'gw' },
    { from: 'gw', to: 'auth', label: '鉴权' },
    { from: 'auth', to: 'user' },
    { from: 'auth', to: 'order' },
    { from: 'user', to: 'db_user' },
    { from: 'user', to: 'cache', label: '缓存' },
    { from: 'order', to: 'db_order' },
    { from: 'order', to: 'pay', label: '支付' },
    { from: 'pay', to: 'mq', label: '回调' },
    { from: 'mq', to: 'notify' },
    { from: 'mq', to: 'order', label: '更新状态' }
  ];
  var steps = null;
  var groups = null;
  var sideNodes = [];
'''

# 线性模式测试
linear_tests = {
    'L1': L1,
    'L2': L2,
    'L3': L3,
    'L4': L4
}

# DAG 模式测试
dag_tests = {
    'L5': L5,
    'L6': L6
}

for level, data in linear_tests.items():
    content = header + data + '\n' + engine + '</script>\n</body>\n</html>\n'
    filename = f'flowchart-{level}.html'
    with open(str(OUTPUT_DIR / filename), 'w') as f:
        f.write(content)
    print(f'Generated {filename}')

for level, data in dag_tests.items():
    content = header_dag + data + '\n' + engine + '</script>\n</body>\n</html>\n'
    filename = f'flowchart-{level}.html'
    with open(str(OUTPUT_DIR / filename), 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
