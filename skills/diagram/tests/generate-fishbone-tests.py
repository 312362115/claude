"""生成 fishbone L1-L4 测试 HTML 文件"""
import re
import os

# 读取模板
with open('../templates/html/fishbone.html', 'r') as f:
    template = f.read()

# 提取引擎部分（数据结束标记之后到 </script>）
engine_match = re.search(r'(// ===== 数据结束 =====\n.*)</script>', template, re.DOTALL)
engine = engine_match.group(1)

# 提取 HTML 头部（从开始到 <script> 标签后）
head_match = re.search(r'(.*<script>\n)', template, re.DOTALL)
html_head = head_match.group(1)

# L1: 3 categories, 2 items each
L1 = '''// ===== 数据 =====
var problem = '项目延期';
var causes = [
  { category: '人员', items: ['人手不足', '经验不够'] },
  { category: '流程', items: ['需求变更频繁', '审批流程长'] },
  { category: '技术', items: ['技术选型失误', '系统不稳定'] }
];
'''

# L2: current default data (6 categories)
L2 = '''// ===== 数据 =====
var problem = '用户留存率下降';
var causes = [
  { category: '产品', items: ['功能复杂', '性能慢', 'Bug 多'] },
  { category: '运营', items: ['活动少', '推送不精准'] },
  { category: '技术', items: ['加载慢', '兼容性差', '崩溃率高'] },
  { category: '市场', items: ['竞品强', '获客成本高'] },
  { category: '人员', items: ['团队不足', '经验欠缺'] },
  { category: '流程', items: ['迭代慢', '需求不清'] }
];
'''

# L3: 6 categories, 4-5 items each
L3 = '''// ===== 数据 =====
var problem = '系统可用性不达标';
var causes = [
  { category: '架构', items: ['单点故障多', '缺少降级方案', '容量规划不足', '服务耦合严重'] },
  { category: '运维', items: ['监控覆盖不全', '告警规则粗糙', '变更流程不规范', '容灾演练不足', '文档缺失'] },
  { category: '开发', items: ['代码质量差', '异常处理不完善', '缺少超时重试', '日志规范缺失'] },
  { category: '测试', items: ['压测覆盖不足', '故障注入测试少', '回归用例不全', '环境不一致', '数据不真实'] },
  { category: '基础设施', items: ['机房带宽瓶颈', '数据库主从延迟', '缓存命中率低', 'CDN 节点不足'] },
  { category: '组织', items: ['On-Call 机制不健全', '故障复盘不到位', '跨团队协作慢', 'SLA 定义模糊'] }
];
'''

# L4: 8 categories, 5-6 items each, long text
L4 = '''// ===== 数据 =====
var problem = '电商大促转化率持续走低';
var causes = [
  { category: '产品体验', items: ['商品详情页加载超过 3 秒', '购物车交互逻辑混乱', '搜索结果相关性差', '推荐算法效果不佳', '移动端适配问题多'] },
  { category: '价格策略', items: ['优惠券规则过于复杂', '凑单逻辑不清晰', '价格标注不透明', '竞品价格更低', '满减门槛设置不合理', '价格保护机制缺失'] },
  { category: '供应链', items: ['热门商品频繁缺货', '发货时效无法保证', '包装破损投诉增多', '退换货流程繁琐', '物流信息更新延迟'] },
  { category: '营销', items: ['广告投放 ROI 下降', '活动预热期不足', '触达渠道单一', '用户分层不够精细', '短信推送打开率极低', '社交裂变效果递减'] },
  { category: '技术', items: ['高峰期系统频繁降级', '支付成功率波动大', '库存扣减不准确', '订单状态同步延迟', '数据统计口径混乱'] },
  { category: '客服', items: ['客服响应时间过长', '机器人识别率低', '投诉处理流程僵化', '售后政策不统一', '客服培训不到位', '工单流转效率低'] },
  { category: '用户信任', items: ['虚假促销舆情发酵', '评价体系可信度下降', '隐私泄露事件影响', '售后承诺难以兑现', '品牌口碑下滑'] },
  { category: '竞争环境', items: ['竞品补贴力度加大', '直播电商分流严重', '社区团购抢占份额', '海外平台跨境竞争', '新兴渠道涌现分散用户'] }
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
    filename = f'fishbone-{level}.html'
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
