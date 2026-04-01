"""生成 er L1-L4 测试 HTML 文件"""
import re
import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / 'docs' / 'assets' / 'diagram' / 'tests' / 'html'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 确保 lib 目录可用
if not os.path.exists('lib'):
    os.symlink('../templates/html/lib', 'lib')

# 读取模板
with open('../templates/html/er.html', 'r') as f:
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

# L1: 简单（3 表，2 关系）
L1 = '''
  var title = '博客系统 ER 图';
  var subtitle = 'L1 简单 · 3 表 · 2 关系';

  var tables = [
    { id: 'users', label: '用户表 users', type: 'core', fields: [
      { name: 'id', dtype: 'INT', pk: true },
      { name: 'username', dtype: 'VARCHAR(50)' },
      { name: 'email', dtype: 'VARCHAR(100)' }
    ]},
    { id: 'posts', label: '文章表 posts', type: 'core', fields: [
      { name: 'id', dtype: 'INT', pk: true },
      { name: 'user_id', dtype: 'INT', fk: true },
      { name: 'title', dtype: 'VARCHAR(200)' },
      { name: 'content', dtype: 'TEXT' }
    ]},
    { id: 'comments', label: '评论表 comments', type: 'normal', fields: [
      { name: 'id', dtype: 'INT', pk: true },
      { name: 'post_id', dtype: 'INT', fk: true },
      { name: 'content', dtype: 'TEXT' }
    ]}
  ];

  var relations = [
    { from: 'users', to: 'posts', label: '1 : N' },
    { from: 'posts', to: 'comments', label: '1 : N' }
  ];
'''

# L2: 中等（6 表，5 关系）— 模板默认数据
L2 = '''
  var title = '电商数据库 ER 图';
  var subtitle = 'L2 中等 · 6 表 · 5 关系';

  var tables = [
    { id: 'users', label: '用户表 users', type: 'core', fields: [
      { name: 'id', dtype: 'INT', pk: true },
      { name: 'username', dtype: 'VARCHAR(50)' },
      { name: 'email', dtype: 'VARCHAR(100)' },
      { name: 'phone', dtype: 'VARCHAR(20)' },
      { name: 'status', dtype: 'ENUM' },
      { name: 'created_at', dtype: 'TIMESTAMP' }
    ]},
    { id: 'orders', label: '订单表 orders', type: 'core', fields: [
      { name: 'id', dtype: 'INT', pk: true },
      { name: 'user_id', dtype: 'INT', fk: true },
      { name: 'total_amount', dtype: 'DECIMAL' },
      { name: 'status', dtype: 'ENUM' },
      { name: 'created_at', dtype: 'TIMESTAMP' }
    ]},
    { id: 'products', label: '商品表 products', type: 'normal', fields: [
      { name: 'id', dtype: 'INT', pk: true },
      { name: 'name', dtype: 'VARCHAR(200)' },
      { name: 'price', dtype: 'DECIMAL' },
      { name: 'stock', dtype: 'INT' },
      { name: 'category_id', dtype: 'INT', fk: true }
    ]},
    { id: 'categories', label: '分类表 categories', type: 'junction', fields: [
      { name: 'id', dtype: 'INT', pk: true },
      { name: 'name', dtype: 'VARCHAR(100)' },
      { name: 'parent_id', dtype: 'INT' }
    ]},
    { id: 'order_items', label: '订单明细 order_items', type: 'junction', fields: [
      { name: 'id', dtype: 'INT', pk: true },
      { name: 'order_id', dtype: 'INT', fk: true },
      { name: 'product_id', dtype: 'INT', fk: true },
      { name: 'quantity', dtype: 'INT' },
      { name: 'price', dtype: 'DECIMAL' }
    ]},
    { id: 'payments', label: '支付记录 payments', type: 'junction', fields: [
      { name: 'id', dtype: 'INT', pk: true },
      { name: 'order_id', dtype: 'INT', fk: true },
      { name: 'amount', dtype: 'DECIMAL' },
      { name: 'method', dtype: 'ENUM' },
      { name: 'status', dtype: 'ENUM' },
      { name: 'paid_at', dtype: 'TIMESTAMP' }
    ]}
  ];

  var relations = [
    { from: 'users', to: 'orders', label: '1 : N' },
    { from: 'orders', to: 'order_items', label: '1 : N' },
    { from: 'products', to: 'order_items', label: '1 : N' },
    { from: 'categories', to: 'products', label: '1 : N' },
    { from: 'orders', to: 'payments', label: '1 : N' }
  ];
'''

# L3: 复杂（10 表，12 关系）
L3 = '''
  var title = '电商平台完整 ER 图';
  var subtitle = 'L3 复杂 · 10 表 · 12 关系';

  var tables = [
    { id: 'users', label: '用户表 users', type: 'core', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'username', dtype: 'VARCHAR(50)' },
      { name: 'email', dtype: 'VARCHAR(100)' },
      { name: 'phone', dtype: 'VARCHAR(20)' },
      { name: 'role', dtype: 'ENUM' },
      { name: 'created_at', dtype: 'TIMESTAMP' }
    ]},
    { id: 'orders', label: '订单表 orders', type: 'core', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'user_id', dtype: 'BIGINT', fk: true },
      { name: 'address_id', dtype: 'BIGINT', fk: true },
      { name: 'total_amount', dtype: 'DECIMAL' },
      { name: 'status', dtype: 'ENUM' },
      { name: 'created_at', dtype: 'TIMESTAMP' }
    ]},
    { id: 'products', label: '商品表 products', type: 'core', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'name', dtype: 'VARCHAR(200)' },
      { name: 'price', dtype: 'DECIMAL' },
      { name: 'stock', dtype: 'INT' },
      { name: 'category_id', dtype: 'BIGINT', fk: true },
      { name: 'shop_id', dtype: 'BIGINT', fk: true }
    ]},
    { id: 'categories', label: '分类表 categories', type: 'junction', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'name', dtype: 'VARCHAR(100)' },
      { name: 'parent_id', dtype: 'BIGINT' },
      { name: 'level', dtype: 'INT' }
    ]},
    { id: 'order_items', label: '订单明细 order_items', type: 'junction', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'order_id', dtype: 'BIGINT', fk: true },
      { name: 'product_id', dtype: 'BIGINT', fk: true },
      { name: 'quantity', dtype: 'INT' },
      { name: 'price', dtype: 'DECIMAL' }
    ]},
    { id: 'payments', label: '支付记录 payments', type: 'normal', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'order_id', dtype: 'BIGINT', fk: true },
      { name: 'amount', dtype: 'DECIMAL' },
      { name: 'method', dtype: 'ENUM' },
      { name: 'status', dtype: 'ENUM' },
      { name: 'paid_at', dtype: 'TIMESTAMP' }
    ]},
    { id: 'addresses', label: '地址表 addresses', type: 'normal', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'user_id', dtype: 'BIGINT', fk: true },
      { name: 'province', dtype: 'VARCHAR(50)' },
      { name: 'city', dtype: 'VARCHAR(50)' },
      { name: 'detail', dtype: 'VARCHAR(200)' }
    ]},
    { id: 'shops', label: '店铺表 shops', type: 'normal', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'owner_id', dtype: 'BIGINT', fk: true },
      { name: 'name', dtype: 'VARCHAR(100)' },
      { name: 'rating', dtype: 'DECIMAL' }
    ]},
    { id: 'reviews', label: '评价表 reviews', type: 'junction', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'user_id', dtype: 'BIGINT', fk: true },
      { name: 'product_id', dtype: 'BIGINT', fk: true },
      { name: 'rating', dtype: 'INT' },
      { name: 'content', dtype: 'TEXT' }
    ]},
    { id: 'coupons', label: '优惠券 coupons', type: 'junction', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'user_id', dtype: 'BIGINT', fk: true },
      { name: 'order_id', dtype: 'BIGINT', fk: true },
      { name: 'discount', dtype: 'DECIMAL' },
      { name: 'status', dtype: 'ENUM' }
    ]}
  ];

  var relations = [
    { from: 'users', to: 'orders', label: '1 : N' },
    { from: 'users', to: 'addresses', label: '1 : N' },
    { from: 'users', to: 'shops', label: '1 : 1' },
    { from: 'users', to: 'reviews', label: '1 : N' },
    { from: 'users', to: 'coupons', label: '1 : N' },
    { from: 'orders', to: 'order_items', label: '1 : N' },
    { from: 'orders', to: 'payments', label: '1 : N' },
    { from: 'orders', to: 'addresses', label: 'N : 1' },
    { from: 'products', to: 'order_items', label: '1 : N' },
    { from: 'products', to: 'reviews', label: '1 : N' },
    { from: 'categories', to: 'products', label: '1 : N' },
    { from: 'shops', to: 'products', label: '1 : N' }
  ];
'''

# L4: 超级复杂（15 表，20 关系）
L4 = '''
  var title = '全业务领域 ER 图';
  var subtitle = 'L4 超级复杂 · 15 表 · 20 关系';

  var tables = [
    { id: 'users', label: '用户 users', type: 'core', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'username', dtype: 'VARCHAR(50)' },
      { name: 'email', dtype: 'VARCHAR(100)' },
      { name: 'phone', dtype: 'VARCHAR(20)' },
      { name: 'role', dtype: 'ENUM' }
    ]},
    { id: 'orders', label: '订单 orders', type: 'core', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'user_id', dtype: 'BIGINT', fk: true },
      { name: 'address_id', dtype: 'BIGINT', fk: true },
      { name: 'coupon_id', dtype: 'BIGINT', fk: true },
      { name: 'total', dtype: 'DECIMAL' },
      { name: 'status', dtype: 'ENUM' }
    ]},
    { id: 'products', label: '商品 products', type: 'core', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'name', dtype: 'VARCHAR(200)' },
      { name: 'price', dtype: 'DECIMAL' },
      { name: 'stock', dtype: 'INT' },
      { name: 'category_id', dtype: 'BIGINT', fk: true },
      { name: 'shop_id', dtype: 'BIGINT', fk: true }
    ]},
    { id: 'categories', label: '分类 categories', type: 'normal', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'name', dtype: 'VARCHAR(100)' },
      { name: 'parent_id', dtype: 'BIGINT' }
    ]},
    { id: 'order_items', label: '订单项 order_items', type: 'junction', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'order_id', dtype: 'BIGINT', fk: true },
      { name: 'product_id', dtype: 'BIGINT', fk: true },
      { name: 'quantity', dtype: 'INT' },
      { name: 'price', dtype: 'DECIMAL' }
    ]},
    { id: 'payments', label: '支付 payments', type: 'normal', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'order_id', dtype: 'BIGINT', fk: true },
      { name: 'amount', dtype: 'DECIMAL' },
      { name: 'method', dtype: 'ENUM' },
      { name: 'status', dtype: 'ENUM' }
    ]},
    { id: 'addresses', label: '地址 addresses', type: 'normal', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'user_id', dtype: 'BIGINT', fk: true },
      { name: 'province', dtype: 'VARCHAR(50)' },
      { name: 'city', dtype: 'VARCHAR(50)' },
      { name: 'detail', dtype: 'TEXT' }
    ]},
    { id: 'shops', label: '店铺 shops', type: 'normal', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'owner_id', dtype: 'BIGINT', fk: true },
      { name: 'name', dtype: 'VARCHAR(100)' },
      { name: 'rating', dtype: 'DECIMAL' }
    ]},
    { id: 'reviews', label: '评价 reviews', type: 'junction', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'user_id', dtype: 'BIGINT', fk: true },
      { name: 'product_id', dtype: 'BIGINT', fk: true },
      { name: 'rating', dtype: 'INT' },
      { name: 'content', dtype: 'TEXT' }
    ]},
    { id: 'coupons', label: '优惠券 coupons', type: 'junction', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'user_id', dtype: 'BIGINT', fk: true },
      { name: 'discount', dtype: 'DECIMAL' },
      { name: 'min_amount', dtype: 'DECIMAL' },
      { name: 'status', dtype: 'ENUM' }
    ]},
    { id: 'shipping', label: '物流 shipping', type: 'normal', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'order_id', dtype: 'BIGINT', fk: true },
      { name: 'carrier', dtype: 'VARCHAR(50)' },
      { name: 'tracking_no', dtype: 'VARCHAR(50)' },
      { name: 'status', dtype: 'ENUM' }
    ]},
    { id: 'refunds', label: '退款 refunds', type: 'junction', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'order_id', dtype: 'BIGINT', fk: true },
      { name: 'payment_id', dtype: 'BIGINT', fk: true },
      { name: 'amount', dtype: 'DECIMAL' },
      { name: 'reason', dtype: 'TEXT' }
    ]},
    { id: 'cart_items', label: '购物车 cart_items', type: 'junction', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'user_id', dtype: 'BIGINT', fk: true },
      { name: 'product_id', dtype: 'BIGINT', fk: true },
      { name: 'quantity', dtype: 'INT' }
    ]},
    { id: 'favorites', label: '收藏 favorites', type: 'junction', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'user_id', dtype: 'BIGINT', fk: true },
      { name: 'product_id', dtype: 'BIGINT', fk: true }
    ]},
    { id: 'notifications', label: '通知 notifications', type: 'junction', fields: [
      { name: 'id', dtype: 'BIGINT', pk: true },
      { name: 'user_id', dtype: 'BIGINT', fk: true },
      { name: 'type', dtype: 'ENUM' },
      { name: 'content', dtype: 'TEXT' },
      { name: 'is_read', dtype: 'BOOLEAN' }
    ]}
  ];

  var relations = [
    { from: 'users', to: 'orders', label: '1 : N' },
    { from: 'users', to: 'addresses', label: '1 : N' },
    { from: 'users', to: 'shops', label: '1 : 1' },
    { from: 'users', to: 'reviews', label: '1 : N' },
    { from: 'users', to: 'coupons', label: '1 : N' },
    { from: 'users', to: 'cart_items', label: '1 : N' },
    { from: 'users', to: 'favorites', label: '1 : N' },
    { from: 'users', to: 'notifications', label: '1 : N' },
    { from: 'orders', to: 'order_items', label: '1 : N' },
    { from: 'orders', to: 'payments', label: '1 : N' },
    { from: 'orders', to: 'shipping', label: '1 : 1' },
    { from: 'orders', to: 'refunds', label: '1 : N' },
    { from: 'orders', to: 'coupons', label: 'N : 1' },
    { from: 'addresses', to: 'orders', label: '1 : N' },
    { from: 'products', to: 'order_items', label: '1 : N' },
    { from: 'products', to: 'reviews', label: '1 : N' },
    { from: 'products', to: 'cart_items', label: '1 : N' },
    { from: 'products', to: 'favorites', label: '1 : N' },
    { from: 'categories', to: 'products', label: '1 : N' },
    { from: 'shops', to: 'products', label: '1 : N' }
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
    filename = f'er-{level}.html'
    with open(str(OUTPUT_DIR / filename), 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
