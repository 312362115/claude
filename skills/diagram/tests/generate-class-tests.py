"""生成 class L1-L4 测试 HTML 文件"""
import re
import os

# 确保 lib 目录可用
if not os.path.exists('lib'):
    os.symlink('../templates/html/lib', 'lib')

# 读取模板
with open('../templates/html/class.html', 'r') as f:
    template = f.read()

# 提取引擎部分（从 theme 定义到文件末尾）
engine_match = re.search(r'(  // ========== 主题 ==========.*)</script>', template, re.DOTALL)
engine = engine_match.group(1)

# 公共 HTML 头（包含 ELKjs）
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

'''

# L1: 简单（3 类，2 关系，无枚举）
L1 = '''
  var title = '简单博客类图';
  var subtitle = 'L1 简单 · 3 类 · 2 关系';

  var classes = [
    { id: 'User', label: 'User', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'username', dtype: 'String' },
        { vis: '-', name: 'email', dtype: 'String' }
      ],
      methods: [
        { vis: '+', name: 'login()', dtype: 'bool' },
        { vis: '+', name: 'getPosts()', dtype: 'List' }
      ]
    },
    { id: 'Post', label: 'Post', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'title', dtype: 'String' },
        { vis: '-', name: 'content', dtype: 'String' }
      ],
      methods: [
        { vis: '+', name: 'publish()', dtype: 'bool' }
      ]
    },
    { id: 'Comment', label: 'Comment', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'content', dtype: 'String' }
      ],
      methods: [
        { vis: '+', name: 'create()', dtype: 'bool' }
      ]
    }
  ];

  var relations = [
    { from: 'User', to: 'Post', type: 'association', label: '发布' },
    { from: 'Post', to: 'Comment', type: 'composition', label: '包含' }
  ];
'''

# L2: 中等（6 类，3 枚举）— 模板默认数据
L2 = '''
  var title = '电商平台类图';
  var subtitle = 'L2 中等 · 6 类 · 3 枚举';

  var classes = [
    { id: 'User', label: 'User', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'username', dtype: 'String' },
        { vis: '-', name: 'email', dtype: 'String' },
        { vis: '-', name: 'phone', dtype: 'String' },
        { vis: '-', name: 'passwordHash', dtype: 'String' },
        { vis: '-', name: 'role', dtype: 'UserRole' }
      ],
      methods: [
        { vis: '+', name: 'register()', dtype: 'bool' },
        { vis: '+', name: 'login(pwd)', dtype: 'Token' },
        { vis: '+', name: 'updateProfile()', dtype: 'bool' },
        { vis: '+', name: 'getOrders()', dtype: 'List' }
      ]
    },
    { id: 'Order', label: 'Order', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'orderNo', dtype: 'String' },
        { vis: '-', name: 'status', dtype: 'OrderStatus' },
        { vis: '-', name: 'totalAmount', dtype: 'Decimal' },
        { vis: '-', name: 'payAmount', dtype: 'Decimal' },
        { vis: '-', name: 'createdAt', dtype: 'DateTime' }
      ],
      methods: [
        { vis: '+', name: 'create(items)', dtype: 'Order' },
        { vis: '+', name: 'cancel()', dtype: 'bool' },
        { vis: '+', name: 'pay(payment)', dtype: 'bool' },
        { vis: '+', name: 'calcTotal()', dtype: 'Decimal' }
      ]
    },
    { id: 'Payment', label: 'Payment', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'paymentNo', dtype: 'String' },
        { vis: '-', name: 'method', dtype: 'PayMethod' },
        { vis: '-', name: 'amount', dtype: 'Decimal' }
      ],
      methods: [
        { vis: '+', name: 'execute()', dtype: 'bool' },
        { vis: '+', name: 'refund(amt)', dtype: 'bool' }
      ]
    },
    { id: 'OrderItem', label: 'OrderItem', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'quantity', dtype: 'Integer' },
        { vis: '-', name: 'unitPrice', dtype: 'Decimal' },
        { vis: '-', name: 'subtotal', dtype: 'Decimal' }
      ],
      methods: [
        { vis: '+', name: 'getSubtotal()', dtype: 'Decimal' }
      ]
    },
    { id: 'Product', label: 'Product', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'name', dtype: 'String' },
        { vis: '-', name: 'price', dtype: 'Decimal' },
        { vis: '-', name: 'stock', dtype: 'Integer' }
      ],
      methods: [
        { vis: '+', name: 'updateStock(d)', dtype: 'bool' },
        { vis: '+', name: 'isAvailable()', dtype: 'bool' }
      ]
    },
    { id: 'Category', label: 'Category', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'name', dtype: 'String' },
        { vis: '-', name: 'parent', dtype: 'Category' }
      ],
      methods: [
        { vis: '+', name: 'getProducts()', dtype: 'List' },
        { vis: '+', name: 'getChildren()', dtype: 'List' }
      ]
    },
    { id: 'UserRole', label: 'UserRole', type: 'enum', values: ['CUSTOMER', 'ADMIN', 'MERCHANT'] },
    { id: 'OrderStatus', label: 'OrderStatus', type: 'enum', values: ['PENDING', 'PAID', 'SHIPPING', 'DELIVERED', 'CANCELLED'] },
    { id: 'PayMethod', label: 'PayMethod', type: 'enum', values: ['ALIPAY', 'WECHAT_PAY', 'CREDIT_CARD'] }
  ];

  var relations = [
    { from: 'User', to: 'Order', type: 'association', label: '下单' },
    { from: 'Order', to: 'OrderItem', type: 'composition', label: '包含' },
    { from: 'OrderItem', to: 'Product', type: 'association', label: '关联' },
    { from: 'Product', to: 'Category', type: 'association', label: '分类' },
    { from: 'Order', to: 'Payment', type: 'association', label: '支付' },
    { from: 'User', to: 'UserRole', type: 'dependency' },
    { from: 'Order', to: 'OrderStatus', type: 'dependency' },
    { from: 'Payment', to: 'PayMethod', type: 'dependency' }
  ];
'''

# L3: 复杂（9 类，2 枚举，10 关系，含继承）
L3 = '''
  var title = '物流管理系统类图';
  var subtitle = 'L3 复杂 · 9 类 · 2 枚举 · 10 关系';

  var classes = [
    { id: 'Vehicle', label: 'Vehicle', type: 'abstract',
      fields: [
        { vis: '#', name: 'id', dtype: 'Long' },
        { vis: '#', name: 'plateNo', dtype: 'String' },
        { vis: '#', name: 'capacity', dtype: 'Double' }
      ],
      methods: [
        { vis: '+', name: 'getLoad()', dtype: 'Double' },
        { vis: '+', name: 'isAvailable()', dtype: 'bool' }
      ]
    },
    { id: 'Truck', label: 'Truck', type: 'class',
      fields: [
        { vis: '-', name: 'axleCount', dtype: 'Integer' },
        { vis: '-', name: 'maxWeight', dtype: 'Double' }
      ],
      methods: [
        { vis: '+', name: 'loadCargo(c)', dtype: 'bool' }
      ]
    },
    { id: 'Van', label: 'Van', type: 'class',
      fields: [
        { vis: '-', name: 'volume', dtype: 'Double' }
      ],
      methods: [
        { vis: '+', name: 'loadPackage(p)', dtype: 'bool' }
      ]
    },
    { id: 'Driver', label: 'Driver', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'name', dtype: 'String' },
        { vis: '-', name: 'license', dtype: 'String' },
        { vis: '-', name: 'phone', dtype: 'String' }
      ],
      methods: [
        { vis: '+', name: 'assignRoute(r)', dtype: 'bool' },
        { vis: '+', name: 'reportStatus()', dtype: 'Status' }
      ]
    },
    { id: 'Route', label: 'Route', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'origin', dtype: 'String' },
        { vis: '-', name: 'destination', dtype: 'String' },
        { vis: '-', name: 'distance', dtype: 'Double' }
      ],
      methods: [
        { vis: '+', name: 'estimateTime()', dtype: 'Duration' },
        { vis: '+', name: 'getWaypoints()', dtype: 'List' }
      ]
    },
    { id: 'Shipment', label: 'Shipment', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'trackingNo', dtype: 'String' },
        { vis: '-', name: 'weight', dtype: 'Double' },
        { vis: '-', name: 'status', dtype: 'ShipStatus' }
      ],
      methods: [
        { vis: '+', name: 'track()', dtype: 'Location' },
        { vis: '+', name: 'updateStatus(s)', dtype: 'bool' }
      ]
    },
    { id: 'Warehouse', label: 'Warehouse', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'name', dtype: 'String' },
        { vis: '-', name: 'address', dtype: 'String' }
      ],
      methods: [
        { vis: '+', name: 'checkCapacity()', dtype: 'Double' },
        { vis: '+', name: 'receive(s)', dtype: 'bool' }
      ]
    },
    { id: 'Customer', label: 'Customer', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'name', dtype: 'String' },
        { vis: '-', name: 'address', dtype: 'String' }
      ],
      methods: [
        { vis: '+', name: 'placeOrder()', dtype: 'Shipment' }
      ]
    },
    { id: 'Waypoint', label: 'Waypoint', type: 'class',
      fields: [
        { vis: '-', name: 'lat', dtype: 'Double' },
        { vis: '-', name: 'lng', dtype: 'Double' },
        { vis: '-', name: 'arrivalTime', dtype: 'DateTime' }
      ],
      methods: []
    },
    { id: 'ShipStatus', label: 'ShipStatus', type: 'enum', values: ['CREATED', 'PICKED_UP', 'IN_TRANSIT', 'DELIVERED'] },
    { id: 'VehicleType', label: 'VehicleType', type: 'enum', values: ['TRUCK', 'VAN', 'MOTORCYCLE'] }
  ];

  var relations = [
    { from: 'Truck', to: 'Vehicle', type: 'inheritance' },
    { from: 'Van', to: 'Vehicle', type: 'inheritance' },
    { from: 'Driver', to: 'Vehicle', type: 'association', label: '驾驶' },
    { from: 'Driver', to: 'Route', type: 'association', label: '执行' },
    { from: 'Route', to: 'Waypoint', type: 'composition', label: '包含' },
    { from: 'Route', to: 'Shipment', type: 'association', label: '运输' },
    { from: 'Customer', to: 'Shipment', type: 'association', label: '下单' },
    { from: 'Warehouse', to: 'Shipment', type: 'association', label: '中转' },
    { from: 'Shipment', to: 'ShipStatus', type: 'dependency' },
    { from: 'Vehicle', to: 'VehicleType', type: 'dependency' }
  ];
'''

# L4: 超级复杂（12 类，4 枚举，15 关系）
L4 = '''
  var title = '在线教育平台类图';
  var subtitle = 'L4 超级复杂 · 12 类 · 4 枚举 · 15 关系';

  var classes = [
    { id: 'Person', label: 'Person', type: 'abstract',
      fields: [
        { vis: '#', name: 'id', dtype: 'Long' },
        { vis: '#', name: 'name', dtype: 'String' },
        { vis: '#', name: 'email', dtype: 'String' }
      ],
      methods: [
        { vis: '+', name: 'getProfile()', dtype: 'Profile' }
      ]
    },
    { id: 'Student', label: 'Student', type: 'class',
      fields: [
        { vis: '-', name: 'grade', dtype: 'String' },
        { vis: '-', name: 'enrollDate', dtype: 'Date' }
      ],
      methods: [
        { vis: '+', name: 'enroll(c)', dtype: 'bool' },
        { vis: '+', name: 'submitHomework(h)', dtype: 'bool' },
        { vis: '+', name: 'getCourses()', dtype: 'List' }
      ]
    },
    { id: 'Teacher', label: 'Teacher', type: 'class',
      fields: [
        { vis: '-', name: 'title', dtype: 'String' },
        { vis: '-', name: 'department', dtype: 'String' }
      ],
      methods: [
        { vis: '+', name: 'createCourse()', dtype: 'Course' },
        { vis: '+', name: 'gradeHomework(h)', dtype: 'Score' }
      ]
    },
    { id: 'Course', label: 'Course', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'title', dtype: 'String' },
        { vis: '-', name: 'desc', dtype: 'String' },
        { vis: '-', name: 'status', dtype: 'CourseStatus' },
        { vis: '-', name: 'price', dtype: 'Decimal' }
      ],
      methods: [
        { vis: '+', name: 'publish()', dtype: 'bool' },
        { vis: '+', name: 'getChapters()', dtype: 'List' },
        { vis: '+', name: 'getStudents()', dtype: 'List' }
      ]
    },
    { id: 'Chapter', label: 'Chapter', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'title', dtype: 'String' },
        { vis: '-', name: 'order', dtype: 'Integer' },
        { vis: '-', name: 'duration', dtype: 'Integer' }
      ],
      methods: [
        { vis: '+', name: 'getVideos()', dtype: 'List' }
      ]
    },
    { id: 'Video', label: 'Video', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'url', dtype: 'String' },
        { vis: '-', name: 'duration', dtype: 'Integer' }
      ],
      methods: [
        { vis: '+', name: 'play()', dtype: 'void' }
      ]
    },
    { id: 'Homework', label: 'Homework', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'title', dtype: 'String' },
        { vis: '-', name: 'deadline', dtype: 'DateTime' },
        { vis: '-', name: 'type', dtype: 'HwType' }
      ],
      methods: [
        { vis: '+', name: 'submit(file)', dtype: 'bool' },
        { vis: '+', name: 'getScore()', dtype: 'Score' }
      ]
    },
    { id: 'Score', label: 'Score', type: 'class',
      fields: [
        { vis: '-', name: 'value', dtype: 'Integer' },
        { vis: '-', name: 'comment', dtype: 'String' },
        { vis: '-', name: 'gradedAt', dtype: 'DateTime' }
      ],
      methods: []
    },
    { id: 'Enrollment', label: 'Enrollment', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'enrollAt', dtype: 'DateTime' },
        { vis: '-', name: 'progress', dtype: 'Double' },
        { vis: '-', name: 'status', dtype: 'EnrollStatus' }
      ],
      methods: [
        { vis: '+', name: 'updateProgress(p)', dtype: 'void' }
      ]
    },
    { id: 'IPayable', label: 'IPayable', type: 'interface',
      fields: [],
      methods: [
        { vis: '+', name: 'pay(amount)', dtype: 'bool' },
        { vis: '+', name: 'refund()', dtype: 'bool' }
      ]
    },
    { id: 'Certificate', label: 'Certificate', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'issuedAt', dtype: 'Date' },
        { vis: '-', name: 'code', dtype: 'String' }
      ],
      methods: [
        { vis: '+', name: 'verify()', dtype: 'bool' }
      ]
    },
    { id: 'Discussion', label: 'Discussion', type: 'class',
      fields: [
        { vis: '-', name: 'id', dtype: 'Long' },
        { vis: '-', name: 'content', dtype: 'String' },
        { vis: '-', name: 'createdAt', dtype: 'DateTime' }
      ],
      methods: [
        { vis: '+', name: 'reply(msg)', dtype: 'Discussion' }
      ]
    },
    { id: 'CourseStatus', label: 'CourseStatus', type: 'enum', values: ['DRAFT', 'PUBLISHED', 'ARCHIVED'] },
    { id: 'EnrollStatus', label: 'EnrollStatus', type: 'enum', values: ['ACTIVE', 'COMPLETED', 'DROPPED'] },
    { id: 'HwType', label: 'HwType', type: 'enum', values: ['QUIZ', 'ESSAY', 'PROJECT', 'CODE'] },
    { id: 'Role', label: 'Role', type: 'enum', values: ['STUDENT', 'TEACHER', 'ADMIN'] }
  ];

  var relations = [
    { from: 'Student', to: 'Person', type: 'inheritance' },
    { from: 'Teacher', to: 'Person', type: 'inheritance' },
    { from: 'Course', to: 'IPayable', type: 'realization' },
    { from: 'Teacher', to: 'Course', type: 'association', label: '创建' },
    { from: 'Student', to: 'Enrollment', type: 'association', label: '选课' },
    { from: 'Enrollment', to: 'Course', type: 'association', label: '课程' },
    { from: 'Course', to: 'Chapter', type: 'composition', label: '包含' },
    { from: 'Chapter', to: 'Video', type: 'composition', label: '包含' },
    { from: 'Course', to: 'Homework', type: 'composition', label: '布置' },
    { from: 'Homework', to: 'Score', type: 'association', label: '评分' },
    { from: 'Enrollment', to: 'Certificate', type: 'association', label: '颁发' },
    { from: 'Course', to: 'Discussion', type: 'association', label: '讨论' },
    { from: 'Course', to: 'CourseStatus', type: 'dependency' },
    { from: 'Enrollment', to: 'EnrollStatus', type: 'dependency' },
    { from: 'Homework', to: 'HwType', type: 'dependency' },
    { from: 'Person', to: 'Role', type: 'dependency' }
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
    filename = f'class-{level}.html'
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
