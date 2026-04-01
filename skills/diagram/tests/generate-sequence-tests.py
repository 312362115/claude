from pathlib import Path
"""生成 sequence L1-L4 测试 HTML 文件"""
import re

OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / 'docs' / 'assets' / 'diagram' / 'tests-html'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 读取模板
with open('../templates/html/sequence.html', 'r') as f:
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

# L1: 简单（3 参与者，5 消息，无 fragment）
L1 = '''
  var title = '用户查询接口时序图';
  var subtitle = 'L1 简单 · 3 参与者 · 5 消息';

  var participants = [
    { id: 'client', label: '客户端', type: 'actor' },
    { id: 'server', label: '服务端', type: 'service' },
    { id: 'db', label: '数据库', type: 'database' }
  ];

  var messages = [
    { from: 'client', to: 'server', label: 'GET /api/users',  type: 'sync' },
    { from: 'server', to: 'db',     label: 'SELECT * FROM users', type: 'sync' },
    { from: 'db',     to: 'server', label: '返回用户列表',       type: 'return' },
    { from: 'server', to: 'server', label: '序列化 JSON',        type: 'self' },
    { from: 'server', to: 'client', label: '200 OK + JSON',      type: 'return' }
  ];
'''

# L2: 中等（6 参与者，alt fragment）— 模板默认数据
L2 = '''
  var title = 'API 登录鉴权时序图';
  var subtitle = 'L2 中等 · 6 参与者 · alt fragment';

  var participants = [
    { id: 'user', label: '用户', type: 'actor' },
    { id: 'fe', label: '前端', type: 'service' },
    { id: 'gw', label: 'API Gateway', type: 'service' },
    { id: 'auth', label: 'Auth 服务', type: 'service' },
    { id: 'mysql', label: 'MySQL', type: 'database' },
    { id: 'redis', label: 'Redis', type: 'database' }
  ];

  var messages = [
    { from: 'user', to: 'fe',    label: '输入账号密码',          type: 'sync' },
    { from: 'fe',   to: 'gw',    label: 'POST /login',          type: 'sync' },
    { from: 'gw',   to: 'auth',  label: '转发请求',              type: 'sync' },
    { from: 'auth', to: 'mysql', label: '查询用户',              type: 'sync' },
    { from: 'mysql',to: 'auth',  label: '返回用户信息',          type: 'return' },
    { from: 'auth', to: 'auth',  label: '验证密码 + 签发 Token', type: 'self' },
    { type: 'fragment', kind: 'alt', condition: 'Token 有效',
      messages: [
        { from: 'auth', to: 'redis', label: '存储 Session',     type: 'sync' },
        { from: 'redis',to: 'auth',  label: 'OK',               type: 'return' }
      ],
      elseCondition: 'Token 无效',
      elseMessages: [
        { from: 'auth', to: 'gw',    label: '401 Unauthorized', type: 'return' }
      ]
    },
    { from: 'auth', to: 'gw',    label: '返回 Token',            type: 'return' },
    { from: 'gw',   to: 'fe',    label: '200 OK + Token',        type: 'return' },
    { from: 'fe',   to: 'user',  label: '登录成功',              type: 'return' }
  ];
'''

# L3: 复杂（8 参与者，20 消息，loop + alt fragments）
L3 = '''
  var title = '订单支付全链路时序图';
  var subtitle = 'L3 复杂 · 8 参与者 · 20 消息 · loop + alt';

  var participants = [
    { id: 'user', label: '用户', type: 'actor' },
    { id: 'app', label: 'App', type: 'service' },
    { id: 'gw', label: 'Gateway', type: 'service' },
    { id: 'order', label: '订单服务', type: 'service' },
    { id: 'inv', label: '库存服务', type: 'service' },
    { id: 'pay', label: '支付服务', type: 'service' },
    { id: 'mysql', label: 'MySQL', type: 'database' },
    { id: 'mq', label: 'MQ', type: 'database' }
  ];

  var messages = [
    { from: 'user', to: 'app',   label: '点击下单',          type: 'sync' },
    { from: 'app',  to: 'gw',    label: 'POST /order',       type: 'sync' },
    { from: 'gw',   to: 'order', label: '创建订单请求',      type: 'sync' },
    { from: 'order',to: 'order', label: '校验订单参数',      type: 'self' },
    { type: 'fragment', kind: 'loop', condition: '遍历商品列表',
      messages: [
        { from: 'order', to: 'inv',   label: '检查库存',       type: 'sync' },
        { from: 'inv',   to: 'mysql', label: '查询库存表',     type: 'sync' },
        { from: 'mysql', to: 'inv',   label: '返回库存数量',   type: 'return' },
        { from: 'inv',   to: 'order', label: '库存充足',       type: 'return' }
      ]
    },
    { from: 'order', to: 'mysql', label: '写入订单记录',     type: 'sync' },
    { from: 'mysql', to: 'order', label: 'OK',               type: 'return' },
    { from: 'order', to: 'gw',    label: '返回订单号',       type: 'return' },
    { from: 'gw',    to: 'app',   label: '跳转支付页',       type: 'return' },
    { from: 'user',  to: 'app',   label: '确认支付',         type: 'sync' },
    { from: 'app',   to: 'pay',   label: '发起支付',         type: 'sync' },
    { from: 'pay',   to: 'pay',   label: '调用第三方支付',   type: 'self' },
    { type: 'fragment', kind: 'alt', condition: '支付成功',
      messages: [
        { from: 'pay',   to: 'order', label: '支付成功回调', type: 'sync' },
        { from: 'order', to: 'mq',    label: '发送订单完成事件', type: 'sync' },
        { from: 'order', to: 'pay',   label: 'ACK',          type: 'return' }
      ],
      elseCondition: '支付失败',
      elseMessages: [
        { from: 'pay', to: 'order',   label: '支付失败通知', type: 'sync' },
        { from: 'order', to: 'inv',   label: '释放库存',     type: 'sync' },
        { from: 'inv',   to: 'order', label: 'OK',           type: 'return' }
      ]
    },
    { from: 'pay',  to: 'app',    label: '返回支付结果',     type: 'return' },
    { from: 'app',  to: 'user',   label: '显示支付结果',     type: 'return' }
  ];
'''

# L4: 超级复杂（10 参与者，30 消息，嵌套 fragments）
L4 = '''
  var title = '微服务下单全链路时序图';
  var subtitle = 'L4 超级复杂 · 10 参与者 · 30 消息 · 嵌套 fragment';

  var participants = [
    { id: 'user', label: '用户', type: 'actor' },
    { id: 'web', label: 'Web', type: 'service' },
    { id: 'gw', label: 'Gateway', type: 'service' },
    { id: 'auth', label: '鉴权服务', type: 'service' },
    { id: 'order', label: '订单服务', type: 'service' },
    { id: 'inv', label: '库存服务', type: 'service' },
    { id: 'pay', label: '支付服务', type: 'service' },
    { id: 'notify', label: '通知服务', type: 'service' },
    { id: 'mysql', label: 'MySQL', type: 'database' },
    { id: 'redis', label: 'Redis', type: 'database' }
  ];

  var messages = [
    { from: 'user', to: 'web',    label: '点击下单',            type: 'sync' },
    { from: 'web',  to: 'gw',     label: 'POST /api/order',     type: 'sync' },
    { from: 'gw',   to: 'auth',   label: '校验 Token',          type: 'sync' },
    { from: 'auth', to: 'redis',  label: '查询 Session',        type: 'sync' },
    { from: 'redis',to: 'auth',   label: '返回用户信息',        type: 'return' },
    { type: 'fragment', kind: 'alt', condition: '鉴权通过',
      messages: [
        { from: 'auth', to: 'gw',    label: '鉴权成功',         type: 'return' },
        { from: 'gw',   to: 'order', label: '转发创建订单',     type: 'sync' },
        { from: 'order',to: 'order', label: '参数校验',         type: 'self' },
        { type: 'fragment', kind: 'loop', condition: '遍历购物车商品',
          messages: [
            { from: 'order', to: 'inv',   label: '锁定库存',     type: 'sync' },
            { from: 'inv',   to: 'mysql', label: 'UPDATE stock', type: 'sync' },
            { from: 'mysql', to: 'inv',   label: 'OK',           type: 'return' },
            { from: 'inv',   to: 'order', label: '锁定成功',     type: 'return' }
          ]
        },
        { from: 'order', to: 'mysql', label: 'INSERT order',    type: 'sync' },
        { from: 'mysql', to: 'order', label: '订单 ID',         type: 'return' },
        { from: 'order', to: 'pay',   label: '发起支付请求',    type: 'sync' },
        { from: 'pay',   to: 'pay',   label: '调用支付宝 API',  type: 'self' },
        { type: 'fragment', kind: 'alt', condition: '支付成功',
          messages: [
            { from: 'pay',    to: 'order',  label: '支付成功',    type: 'return' },
            { from: 'order',  to: 'mysql',  label: '更新订单状态', type: 'sync' },
            { from: 'mysql',  to: 'order',  label: 'OK',          type: 'return' },
            { from: 'order',  to: 'notify', label: '发送通知',    type: 'sync' },
            { from: 'notify', to: 'notify', label: '推送短信+站内信', type: 'self' },
            { from: 'notify', to: 'order',  label: '通知完成',    type: 'return' }
          ],
          elseCondition: '支付失败',
          elseMessages: [
            { from: 'pay',   to: 'order',  label: '支付失败',     type: 'return' },
            { from: 'order', to: 'inv',    label: '释放库存',     type: 'sync' },
            { from: 'inv',   to: 'order',  label: '释放完成',     type: 'return' }
          ]
        },
        { from: 'order', to: 'gw',    label: '返回订单结果',    type: 'return' }
      ],
      elseCondition: '鉴权失败',
      elseMessages: [
        { from: 'auth',  to: 'gw',    label: '401 Unauthorized', type: 'return' }
      ]
    },
    { from: 'gw',  to: 'web',     label: '返回响应',            type: 'return' },
    { from: 'web', to: 'user',    label: '显示结果页',          type: 'return' }
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
    filename = f'sequence-{level}.html'
    with open(str(OUTPUT_DIR / filename), 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
