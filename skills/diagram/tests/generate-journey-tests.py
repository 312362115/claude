"""生成 journey L1-L4 测试 HTML 文件"""
import re
import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / 'docs' / 'assets' / 'diagram' / 'tests-html'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 读取模板
with open('../templates/html/journey.html', 'r') as f:
    template = f.read()

# 提取引擎部分（数据结束标记之后到 </script>）
engine_match = re.search(r'(// ===== 数据结束 =====\n.*)</script>', template, re.DOTALL)
engine = engine_match.group(1)

# 提取 HTML 头部（从开始到 <script> 标签后）
head_match = re.search(r'(.*<script>\n)', template, re.DOTALL)
html_head = head_match.group(1)

# L1: 2 phases, 2 steps each
L1 = '''// ===== 数据 =====
var phases = [
  { label: '注册', steps: [
    { label: '填写信息', score: 3 },
    { label: '邮箱验证', score: 4 }
  ]},
  { label: '上手', steps: [
    { label: '引导教程', score: 5 },
    { label: '创建首个项目', score: 4 }
  ]}
];
'''

# L2: current default data (4 phases)
L2 = '''// ===== 数据 =====
var phases = [
  { label: '发现', steps: [
    { label: '看到广告', score: 3 },
    { label: '搜索产品', score: 4 }
  ]},
  { label: '购买', steps: [
    { label: '浏览商品', score: 4 },
    { label: '加入购物车', score: 3 },
    { label: '下单支付', score: 2 }
  ]},
  { label: '使用', steps: [
    { label: '收到商品', score: 5 },
    { label: '使用体验', score: 4 }
  ]},
  { label: '售后', steps: [
    { label: '联系客服', score: 2 },
    { label: '退换货', score: 1 }
  ]}
];
'''

# L3: 5 phases, 3-4 steps each
L3 = '''// ===== 数据 =====
var phases = [
  { label: '认知', steps: [
    { label: '社交媒体广告', score: 3 },
    { label: '朋友推荐', score: 5 },
    { label: '应用商店搜索', score: 4 }
  ]},
  { label: '注册', steps: [
    { label: '下载 App', score: 4 },
    { label: '填写注册信息', score: 2 },
    { label: '实名认证', score: 1 },
    { label: '设置偏好', score: 3 }
  ]},
  { label: '首次体验', steps: [
    { label: '新手引导', score: 4 },
    { label: '浏览推荐内容', score: 5 },
    { label: '完成首单', score: 3 }
  ]},
  { label: '持续使用', steps: [
    { label: '日常浏览', score: 4 },
    { label: '参与社区互动', score: 5 },
    { label: '使用会员权益', score: 4 },
    { label: '收到推送通知', score: 2 }
  ]},
  { label: '推荐传播', steps: [
    { label: '分享给朋友', score: 5 },
    { label: '撰写评价', score: 3 },
    { label: '参与拉新活动', score: 4 }
  ]}
];
'''

# L4: 6 phases, 4-5 steps each
L4 = '''// ===== 数据 =====
var phases = [
  { label: '需求萌发', steps: [
    { label: '工作中遇到效率瓶颈', score: 2 },
    { label: '同事推荐工具', score: 4 },
    { label: '搜索解决方案', score: 3 },
    { label: '阅读产品评测', score: 4 }
  ]},
  { label: '评估对比', steps: [
    { label: '访问官网了解功能', score: 4 },
    { label: '查看定价方案', score: 3 },
    { label: '与竞品功能对比', score: 3 },
    { label: '申请免费试用', score: 5 },
    { label: '咨询销售顾问', score: 2 }
  ]},
  { label: '采购', steps: [
    { label: '内部审批流程', score: 1 },
    { label: '与销售沟通折扣', score: 3 },
    { label: '签署合同', score: 2 },
    { label: '完成付款', score: 4 }
  ]},
  { label: '部署上线', steps: [
    { label: '技术对接集成', score: 3 },
    { label: '数据迁移', score: 1 },
    { label: '配置工作流', score: 2 },
    { label: '团队培训', score: 4 },
    { label: '灰度发布验证', score: 3 }
  ]},
  { label: '日常使用', steps: [
    { label: '团队日常协作', score: 5 },
    { label: '自定义工作流', score: 4 },
    { label: '使用数据分析看板', score: 5 },
    { label: '提交功能建议', score: 3 }
  ]},
  { label: '续费与拓展', steps: [
    { label: '评估使用效果', score: 4 },
    { label: '续费谈判', score: 2 },
    { label: '推广到其他部门', score: 5 },
    { label: '成为标杆客户', score: 5 },
    { label: '参与用户社区', score: 4 }
  ]}
];
'''

test_data = {
    'L1': L1,
    'L2': L2,
    'L3': L3,
    'L4': L4
}

for level, data in test_data.items():
    content = html_head + data + engine + '</script>\n</body>\n</html>\n'
    filename = f'journey-{level}.html'
    with open(str(OUTPUT_DIR / filename), 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
