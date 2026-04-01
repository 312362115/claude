"""生成 kanban L1-L4 测试 HTML 文件"""
import re
import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / 'docs' / 'assets' / 'diagram' / 'tests-html'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not os.path.exists('lib'):
    os.symlink('../templates/html/lib', 'lib')

with open('../templates/html/kanban.html', 'r') as f:
    template = f.read()

# 提取引擎（从 配色 到文件末尾）
engine_match = re.search(r'(  // ========== 配色 ==========.*)</script>\n</body>\n</html>', template, re.DOTALL)
engine = engine_match.group(1)

header = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, system-ui, 'PingFang SC', sans-serif; background: #fff; display: flex; flex-direction: column; align-items: center; }
  .title { font-size: 22px; font-weight: 700; color: #1a1a2e; margin-top: 28px; }
  .subtitle { font-size: 14px; color: #888; margin-top: 6px; }
  .chart-wrap { margin-top: 20px; position: relative; }
</style>
<script src="lib/utils.js"></script>
</head>
<body>
<div class="title" id="title"></div>
<div class="subtitle" id="subtitle"></div>
<div class="chart-wrap">
  <svg id="canvas"></svg>
</div>
<script>
(function() {
  var svg = document.getElementById('canvas');
  var SANS = "-apple-system, system-ui, 'PingFang SC', sans-serif";

'''

tail = '</script>\n</body>\n</html>\n'

L1 = '''
  document.getElementById('title').textContent = '简单任务板';
  document.getElementById('subtitle').textContent = 'L1 简单 · 3 列 · 1-2 卡片';
  var columns = [
    { title: 'To Do', cards: [
      { title: '搭建项目脚手架', tag: 'task' },
      { title: '确认技术选型', tag: 'task' }
    ]},
    { title: 'In Progress', cards: [
      { title: '编写首页 UI', tag: 'feature' }
    ]},
    { title: 'Done', cards: [
      { title: '需求评审', tag: 'task' },
      { title: '创建代码仓库', tag: 'task' }
    ]}
  ];
'''

L2 = '''
  document.getElementById('title').textContent = 'Sprint Board';
  document.getElementById('subtitle').textContent = 'L2 中等 · 5 列 · 带标签和负责人';
  var columns = [
    { title: 'Backlog', cards: [
      { title: '用户注册流程优化', tag: 'feature' },
      { title: '邮件模板国际化', tag: 'feature' },
      { title: '性能基准测试', tag: 'task' }
    ]},
    { title: 'To Do', cards: [
      { title: '修复登录超时 #234', tag: 'bug' },
      { title: '添加 Redis 缓存层', tag: 'feature', assignee: '张三' }
    ]},
    { title: 'In Progress', cards: [
      { title: 'API 限流中间件', tag: 'feature', assignee: '李四' },
      { title: '修复支付回调 #256', tag: 'bug', assignee: '王五' }
    ]},
    { title: 'Review', cards: [
      { title: '日志规范化改造', tag: 'task', assignee: '张三' }
    ]},
    { title: 'Done', cards: [
      { title: '数据库索引优化', tag: 'task', assignee: '李四' },
      { title: '修复 XSS 漏洞 #201', tag: 'bug', assignee: '王五' },
      { title: 'OAuth2 接入', tag: 'feature', assignee: '张三' }
    ]}
  ];
'''

L3 = '''
  document.getElementById('title').textContent = '产品迭代看板';
  document.getElementById('subtitle').textContent = 'L3 复杂 · 6 列 · 4-5 卡片 · 混合标签';
  var columns = [
    { title: 'Icebox', cards: [
      { title: '暗色模式适配', tag: 'feature' },
      { title: '多语言支持（日语）', tag: 'feature' },
      { title: '无障碍访问优化', tag: 'task' },
      { title: '性能监控告警', tag: 'task' }
    ]},
    { title: 'Backlog', cards: [
      { title: '搜索结果排序优化', tag: 'feature', assignee: '张三' },
      { title: '修复图片上传失败 #312', tag: 'bug', assignee: '李四' },
      { title: '数据导出 CSV 格式', tag: 'feature' },
      { title: '单元测试覆盖率提升', tag: 'task' },
      { title: '修复分页显示错误 #318', tag: 'bug' }
    ]},
    { title: 'To Do', cards: [
      { title: '用户画像分析模块', tag: 'feature', assignee: '王五' },
      { title: '接口文档自动生成', tag: 'task', assignee: '张三' },
      { title: '修复内存泄漏 #325', tag: 'bug', assignee: '李四' },
      { title: 'WebSocket 推送服务', tag: 'feature' }
    ]},
    { title: 'In Progress', cards: [
      { title: '订单流程重构', tag: 'feature', assignee: '王五' },
      { title: '修复并发锁问题 #330', tag: 'bug', assignee: '李四' },
      { title: '权限系统 RBAC 改造', tag: 'feature', assignee: '张三' },
      { title: 'CI/CD 流水线优化', tag: 'task', assignee: '赵六' },
      { title: '修复缓存穿透 #335', tag: 'bug', assignee: '王五' }
    ]},
    { title: 'Review', cards: [
      { title: '消息队列接入', tag: 'feature', assignee: '张三' },
      { title: '数据库读写分离', tag: 'task', assignee: '李四' },
      { title: '修复时区问题 #340', tag: 'bug', assignee: '赵六' },
      { title: '日志采集 ELK 对接', tag: 'task', assignee: '王五' }
    ]},
    { title: 'Done', cards: [
      { title: '用户反馈系统', tag: 'feature', assignee: '张三' },
      { title: '修复 SQL 注入 #301', tag: 'bug', assignee: '李四' },
      { title: 'API 网关搭建', tag: 'task', assignee: '王五' },
      { title: '配置中心集成', tag: 'feature', assignee: '赵六' },
      { title: '修复文件下载 #305', tag: 'bug', assignee: '李四' }
    ]}
  ];
'''

L4 = '''
  document.getElementById('title').textContent = '大型项目全局看板';
  document.getElementById('subtitle').textContent = 'L4 超级复杂 · 7 列 · 5-8 卡片 · 全特性';
  var columns = [
    { title: 'Icebox', cards: [
      { title: 'GraphQL 迁移', tag: 'feature' },
      { title: '微前端架构评估', tag: 'task' },
      { title: 'AI 智能推荐引擎', tag: 'feature' },
      { title: '跨端统一 SDK', tag: 'feature' },
      { title: '自动化运维平台', tag: 'task' },
      { title: '多租户架构改造', tag: 'feature' }
    ]},
    { title: 'Backlog', cards: [
      { title: '全文搜索 ES 接入', tag: 'feature', assignee: '张三' },
      { title: '修复 OOM #401', tag: 'bug', assignee: '李四' },
      { title: '灰度发布系统', tag: 'feature', assignee: '王五' },
      { title: '接口幂等性改造', tag: 'task', assignee: '赵六' },
      { title: '修复死锁 #405', tag: 'bug', assignee: '李四' },
      { title: '分布式事务 Saga', tag: 'feature' },
      { title: '压测环境搭建', tag: 'task' }
    ]},
    { title: 'To Do', cards: [
      { title: '支付对账系统', tag: 'feature', assignee: '张三' },
      { title: '修复数据不一致 #410', tag: 'bug', assignee: '王五' },
      { title: '链路追踪 Jaeger', tag: 'task', assignee: '赵六' },
      { title: '文件存储 OSS 迁移', tag: 'feature', assignee: '李四' },
      { title: '修复慢查询 #415', tag: 'bug', assignee: '张三' },
      { title: '配置热更新', tag: 'task', assignee: '王五' },
      { title: '审计日志模块', tag: 'feature' },
      { title: '修复 CORS #418', tag: 'bug' }
    ]},
    { title: 'In Progress', cards: [
      { title: '实时数据大屏', tag: 'feature', assignee: '张三' },
      { title: '修复连接池泄漏 #420', tag: 'bug', assignee: '李四' },
      { title: '短信网关对接', tag: 'feature', assignee: '王五' },
      { title: '数据脱敏中间件', tag: 'task', assignee: '赵六' },
      { title: '修复重复提交 #425', tag: 'bug', assignee: '张三' },
      { title: '动态表单引擎', tag: 'feature', assignee: '李四' },
      { title: '服务熔断 Sentinel', tag: 'task', assignee: '王五' }
    ]},
    { title: 'Review', cards: [
      { title: '消息通知中心', tag: 'feature', assignee: '赵六' },
      { title: '修复权限绕过 #430', tag: 'bug', assignee: '张三' },
      { title: '数据迁移工具', tag: 'task', assignee: '李四' },
      { title: '定时任务调度', tag: 'feature', assignee: '王五' },
      { title: '修复并发超卖 #435', tag: 'bug', assignee: '赵六' }
    ]},
    { title: 'Testing', cards: [
      { title: '全链路压测', tag: 'task', assignee: '张三' },
      { title: '安全渗透测试', tag: 'task', assignee: '李四' },
      { title: '性能回归验证', tag: 'task', assignee: '王五' },
      { title: '修复边界条件 #440', tag: 'bug', assignee: '赵六' },
      { title: 'UAT 用户验收', tag: 'task', assignee: '张三' },
      { title: '修复兼容性 #442', tag: 'bug', assignee: '李四' }
    ]},
    { title: 'Done', cards: [
      { title: '统一认证中心', tag: 'feature', assignee: '张三' },
      { title: '修复 XSS #390', tag: 'bug', assignee: '李四' },
      { title: 'K8s 部署改造', tag: 'task', assignee: '王五' },
      { title: '数据备份恢复', tag: 'task', assignee: '赵六' },
      { title: '修复 CSRF #395', tag: 'bug', assignee: '张三' },
      { title: '监控告警体系', tag: 'feature', assignee: '李四' },
      { title: 'API 版本管理', tag: 'feature', assignee: '王五' },
      { title: '修复内存溢出 #398', tag: 'bug', assignee: '赵六' }
    ]}
  ];
'''

test_data = {'L1': L1, 'L2': L2, 'L3': L3, 'L4': L4}

for level, data in test_data.items():
    content = header + data + '\n' + engine + tail
    filename = f'kanban-{level}.html'
    with open(str(OUTPUT_DIR / filename), 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
