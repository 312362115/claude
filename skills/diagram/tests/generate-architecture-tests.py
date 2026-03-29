"""生成 architecture L1-L4 测试 HTML 文件"""
import re

# 读取模板
with open('../templates/html/architecture.html', 'r') as f:
    template = f.read()

# 提取引擎部分（从 theme 定义到文件末尾）
engine_match = re.search(r'(  // ========== 主题 ==========.*)</script>', template, re.DOTALL)
engine = engine_match.group(1)

# 公共 HTML 头
header = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, system-ui, 'PingFang SC', sans-serif;
    background: #fff;
    padding: 24px;
    display: inline-block;
  }
</style>
</head>
<body>
<svg id="canvas"></svg>

<script>
(function() {
  var NS = 'http://www.w3.org/2000/svg';
  var svg = document.getElementById('canvas');

'''

# L1: 简单（2 层，每层 2 节点）
L1 = '''
  var title = '前后端架构';
  var subtitle = 'L1 简单 · 2 层';

  var layers = [
    { label: '前端', nodes: [
      { label: 'Web App', desc: 'React' },
      { label: 'Admin', desc: 'Vue.js' }
    ]},
    { label: '后端', nodes: [
      { label: 'API Server', desc: 'Node.js' },
      { label: 'Database', desc: 'PostgreSQL' }
    ]}
  ];
'''

# L2: 中等（4 层）— 模板默认数据
L2 = '''
  var title = '电商平台 · 系统架构';
  var subtitle = 'L2 中等 · 4 层';

  var layers = [
    { label: '客户端层', nodes: [
      { label: 'Web App', desc: 'React SPA' },
      { label: 'Mobile App', desc: 'React Native' },
      { label: 'Admin Panel', desc: 'Vue.js' }
    ]},
    { label: 'API 网关层', nodes: [
      { label: 'Nginx', desc: '负载均衡' },
      { label: 'API Gateway', desc: '鉴权 + 路由' }
    ]},
    { label: '服务层', nodes: [
      { label: '用户服务', desc: 'Go' },
      { label: '订单服务', desc: 'Java' },
      { label: '支付服务', desc: 'Java' },
      { label: '商品服务', desc: 'Go' }
    ]},
    { label: '数据层', nodes: [
      { label: 'MySQL', desc: '主从集群' },
      { label: 'Redis', desc: '缓存集群' },
      { label: 'Elasticsearch', desc: '搜索引擎' }
    ]}
  ];
'''

# L3: 复杂（6 层，节点数量不等）
L3 = '''
  var title = '云原生微服务架构';
  var subtitle = 'L3 复杂 · 6 层';

  var layers = [
    { label: '接入层', nodes: [
      { label: 'Web', desc: 'React' },
      { label: 'iOS', desc: 'Swift' },
      { label: 'Android', desc: 'Kotlin' },
      { label: '小程序', desc: 'WeChat' }
    ]},
    { label: '网关层', nodes: [
      { label: 'CDN', desc: '静态资源' },
      { label: 'WAF', desc: '安全防护' },
      { label: 'Kong', desc: 'API 网关' }
    ]},
    { label: '业务服务', nodes: [
      { label: '用户中心', desc: 'Go' },
      { label: '商品中心', desc: 'Java' },
      { label: '交易中心', desc: 'Java' },
      { label: '营销中心', desc: 'Python' },
      { label: '物流中心', desc: 'Go' }
    ]},
    { label: '中间件', nodes: [
      { label: 'Kafka', desc: '消息队列' },
      { label: 'Sentinel', desc: '流控熔断' },
      { label: 'Nacos', desc: '服务发现' }
    ]},
    { label: '数据层', nodes: [
      { label: 'MySQL', desc: '分库分表' },
      { label: 'Redis', desc: '集群模式' },
      { label: 'ES', desc: '全文搜索' },
      { label: 'MongoDB', desc: '文档存储' }
    ]},
    { label: '基础设施', nodes: [
      { label: 'K8s', desc: '容器编排' },
      { label: 'Prometheus', desc: '监控告警' },
      { label: 'ELK', desc: '日志平台' }
    ]}
  ];
'''

# L4: 超级复杂（8 层，最多 5 节点）
L4 = '''
  var title = '企业级全栈技术架构';
  var subtitle = 'L4 超级复杂 · 8 层';

  var layers = [
    { label: '终端', nodes: [
      { label: 'PC Web', desc: 'React' },
      { label: 'H5', desc: 'Vue' },
      { label: 'iOS', desc: 'Swift' },
      { label: 'Android', desc: 'Kotlin' },
      { label: '小程序', desc: 'Taro' }
    ]},
    { label: 'CDN/边缘', nodes: [
      { label: 'CloudFlare', desc: 'CDN' },
      { label: 'WAF', desc: '防火墙' }
    ]},
    { label: '网关', nodes: [
      { label: 'Nginx', desc: '负载均衡' },
      { label: 'Kong', desc: 'API 网关' },
      { label: 'OAuth2', desc: '统一鉴权' }
    ]},
    { label: 'BFF', nodes: [
      { label: 'Web BFF', desc: 'Node.js' },
      { label: 'App BFF', desc: 'Node.js' },
      { label: 'Admin BFF', desc: 'Go' }
    ]},
    { label: '核心服务', nodes: [
      { label: '用户服务', desc: 'Go' },
      { label: '订单服务', desc: 'Java' },
      { label: '支付服务', desc: 'Java' },
      { label: '商品服务', desc: 'Go' },
      { label: '风控服务', desc: 'Python' }
    ]},
    { label: '中间件', nodes: [
      { label: 'Kafka', desc: '事件总线' },
      { label: 'gRPC', desc: '服务通信' },
      { label: 'Sentinel', desc: '限流熔断' },
      { label: 'Nacos', desc: '注册中心' }
    ]},
    { label: '数据层', nodes: [
      { label: 'TiDB', desc: '分布式 SQL' },
      { label: 'Redis', desc: '缓存集群' },
      { label: 'ES', desc: '搜索引擎' },
      { label: 'MinIO', desc: '对象存储' },
      { label: 'ClickHouse', desc: 'OLAP' }
    ]},
    { label: '基础设施', nodes: [
      { label: 'K8s', desc: '容器平台' },
      { label: 'Prometheus', desc: '监控' },
      { label: 'Jaeger', desc: '链路追踪' },
      { label: 'ArgoCD', desc: 'GitOps' }
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
    content = header + data + '\n' + engine + '</script>\n</body>\n</html>\n'
    filename = f'architecture-{level}.html'
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
