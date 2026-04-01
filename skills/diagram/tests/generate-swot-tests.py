"""生成 swot L1-L4 测试 HTML 文件"""
import re
import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / 'docs' / 'assets' / 'diagram' / 'tests' / 'html'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 读取模板
with open('../templates/html/swot.html', 'r') as f:
    template = f.read()

# SWOT 是纯 HTML/CSS，提取引擎部分（数据结束标记之后到 </script>）
engine_match = re.search(r'(// ===== 数据结束 =====\n.*)</script>', template, re.DOTALL)
engine = engine_match.group(1)

# 提取 HTML 头部（从开始到 <script> 标签后的数据定义之前）
head_match = re.search(r'(.*<script>\n)', template, re.DOTALL)
html_head = head_match.group(1)

# L1: 2 items per quadrant
L1 = '''// ===== 数据 =====
var data = {
  strengths: ['品牌知名度高', '核心技术领先'],
  weaknesses: ['成本偏高', '渠道单一'],
  opportunities: ['新市场拓展', '技术升级'],
  threats: ['价格战竞争', '政策变化']
};
'''

# L2: current default data (3 items each)
L2 = '''// ===== 数据 =====
var data = {
  strengths: ['技术团队强', '产品口碑好', '用户基数大'],
  weaknesses: ['资金有限', '市场覆盖不足', '运营团队小'],
  opportunities: ['新兴市场增长', 'AI 技术赋能', '政策支持'],
  threats: ['竞争加剧', '用户增长放缓', '监管趋严']
};
'''

# L3: 5 items per quadrant
L3 = '''// ===== 数据 =====
var data = {
  strengths: ['技术壁垒高', '团队经验丰富', '产品迭代快', '用户粘性强', '数据资产积累'],
  weaknesses: ['现金流紧张', '国际化能力弱', '售后体系不完善', '人才招聘困难', '品牌认知度低'],
  opportunities: ['出海东南亚市场', 'AI 降本增效', '产业数字化转型', '政策补贴红利', '跨界合作机会'],
  threats: ['大厂入局竞争', '用户隐私法规收紧', '技术路线变更风险', '宏观经济下行', '供应链不稳定']
};
'''

# L4: 8 items per quadrant, with longer text
L4 = '''// ===== 数据 =====
var data = {
  strengths: [
    '核心算法专利壁垒，技术领先同行 2 年',
    '月活用户突破 5000 万，日均使用时长 45 分钟',
    '团队 80% 来自一线大厂，技术功底扎实',
    '产品 NPS 评分 72，远超行业平均水平',
    '自建数据中台，数据处理能力行业领先',
    '已完成 C 轮融资，资金储备充足',
    '完善的 DevOps 体系，发布效率高',
    '深耕垂直领域 5 年，行业理解深刻'
  ],
  weaknesses: [
    '海外市场占比不足 5%，国际化进展缓慢',
    '客服团队仅 50 人，用户投诉响应时间长',
    '技术债务累积严重，重构成本高',
    '中层管理梯队断层，组织效率受限',
    '部分核心依赖单一供应商，存在断供风险',
    '移动端体验落后于竞品，适配机型不足',
    '内容审核机制不完善，合规风险存在',
    '员工流失率偏高，知识传承不足'
  ],
  opportunities: [
    '东南亚互联网渗透率快速增长，市场空间巨大',
    'AIGC 技术突破带来产品创新的全新可能',
    '行业监管趋严利好合规化运营的企业',
    '5G 普及推动视频和实时互动场景爆发',
    '企业数字化转型加速，B 端需求旺盛',
    '竞品 A 因融资失败退出市场，用户可迁移',
    '政府产业扶持基金开放申请，可降低研发成本',
    '碳中和政策推动绿色科技赛道快速增长'
  ],
  threats: [
    '头部大厂推出同类产品，获客成本持续上升',
    '数据隐私法规全球收紧，合规成本大幅增加',
    '经济下行周期广告主预算缩减，收入承压',
    '开源替代方案成熟度提升，技术护城河被削弱',
    '关键芯片供应受地缘政治影响，硬件成本波动',
    '用户注意力碎片化加剧，留存难度持续增大',
    'AI 生成内容监管政策不确定性高',
    '竞品 B 获得战略投资，加速市场扩张'
  ]
};
'''

test_data = {
    'L1': L1,
    'L2': L2,
    'L3': L3,
    'L4': L4
}

for level, data in test_data.items():
    content = html_head + data + engine + '</script>\n</body>\n</html>\n'
    filename = f'swot-{level}.html'
    with open(str(OUTPUT_DIR / filename), 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
