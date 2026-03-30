"""生成 decision-tree L1-L4 测试 HTML 文件"""

# 读取模板
with open('../templates/html/decision-tree.html', 'r') as f:
    template = f.read()

# 提取 HTML 头部（到第二个 <script> 标签）
first_script = template.index('<script src="lib/utils.js">')
second_script = template.index('<script>', first_script)
head = template[:second_script + len('<script>')]

tail = '</script>\n</body>\n</html>\n'

# 提取引擎部分：从 LEVEL_GAP 到 IIFE 结束
engine_start = template.index('  // --- 布局参数 ---')
engine_end = template.index('})();') + len('})();')
engine = template[engine_start:engine_end]

# L1: depth=2, 1 root with 2 leaf children
L1_data = '''
(function() {
  var svg = document.getElementById('canvas');

  // --- 数据定义 ---
  var tree = {
    id: 'root', label: '是否需要数据库？', type: 'root',
    children: [
      { id: 'r1', label: '文件存储', type: 'result', edgeLabel: 'No', edgeColor: '#F43F5E' },
      { id: 'r2', label: 'SQLite', type: 'result', edgeLabel: 'Yes', edgeColor: '#10B981' }
    ]
  };

'''

# L2: default template data (depth=3, ~13 nodes)
L2_data = '''
(function() {
  var svg = document.getElementById('canvas');

  // --- 数据定义 ---
  var tree = {
    id: 'root', label: '数据类型？', type: 'root',
    children: [
      { id: 'd1', label: '结构化数据', type: 'decision', edgeLabel: '表格/关系型',
        children: [
          { id: 'd1a', label: '读多写少？', type: 'decision',
            children: [
              { id: 'r1', label: 'Redis', type: 'result', edgeLabel: 'Yes', edgeColor: '#10B981' },
              { id: 'r2', label: 'MySQL', type: 'result', edgeLabel: 'No' }
            ]
          },
          { id: 'd1b', label: '需要事务？', type: 'decision',
            children: [
              { id: 'r3', label: 'PostgreSQL', type: 'result', edgeLabel: 'Yes', edgeColor: '#10B981' }
            ]
          }
        ]
      },
      { id: 'd2', label: '半结构化数据', type: 'decision', edgeLabel: 'JSON/文档',
        children: [
          { id: 'd2a', label: 'JSON 为主？', type: 'decision',
            children: [
              { id: 'r4', label: 'MongoDB', type: 'result', edgeLabel: 'Yes', edgeColor: '#10B981' }
            ]
          },
          { id: 'd2b', label: '数据量大？', type: 'decision',
            children: [
              { id: 'r5', label: 'Elasticsearch', type: 'result', edgeLabel: 'Yes', edgeColor: '#10B981' }
            ]
          }
        ]
      },
      { id: 'd3', label: '非结构化数据', type: 'decision', edgeLabel: '文件/二进制',
        children: [
          { id: 'r6', label: 'OSS/S3', type: 'external', edgeLabel: '小文件' },
          { id: 'r7', label: 'HDFS', type: 'external', edgeLabel: '大数据' }
        ]
      }
    ]
  };

'''

# L3: depth=4, wider tree
L3_data = '''
(function() {
  var svg = document.getElementById('canvas');

  // --- 数据定义 ---
  var tree = {
    id: 'root', label: '系统架构选型', type: 'root',
    children: [
      { id: 'd1', label: '单体还是微服务？', type: 'decision', edgeLabel: '规模评估',
        children: [
          { id: 'd1a', label: '团队 < 10人？', type: 'decision', edgeLabel: '单体优先',
            children: [
              { id: 'r1', label: 'Spring Boot 单体', type: 'result', edgeLabel: 'Yes', edgeColor: '#10B981' },
              { id: 'd1a2', label: '需要快速迭代？', type: 'decision', edgeLabel: 'No',
                children: [
                  { id: 'r2', label: '模块化单体', type: 'result', edgeLabel: 'Yes', edgeColor: '#10B981' },
                  { id: 'r3', label: '微服务架构', type: 'result', edgeLabel: 'No' }
                ]
              }
            ]
          },
          { id: 'd1b', label: '高并发场景？', type: 'decision', edgeLabel: '微服务优先',
            children: [
              { id: 'r4', label: 'K8s + 微服务', type: 'result', edgeLabel: 'Yes', edgeColor: '#10B981' },
              { id: 'r5', label: 'Serverless', type: 'result', edgeLabel: 'No' }
            ]
          }
        ]
      },
      { id: 'd2', label: '前端技术栈？', type: 'decision', edgeLabel: '前端选型',
        children: [
          { id: 'd2a', label: 'SEO 重要？', type: 'decision', edgeLabel: '渲染方式',
            children: [
              { id: 'r6', label: 'Next.js SSR', type: 'result', edgeLabel: 'Yes', edgeColor: '#10B981' },
              { id: 'r7', label: 'React SPA', type: 'result', edgeLabel: 'No' }
            ]
          },
          { id: 'd2b', label: '移动端优先？', type: 'decision', edgeLabel: '跨平台',
            children: [
              { id: 'r8', label: 'React Native', type: 'result', edgeLabel: 'Yes', edgeColor: '#10B981' },
              { id: 'r9', label: 'Flutter', type: 'external', edgeLabel: '高性能' }
            ]
          }
        ]
      },
      { id: 'd3', label: '数据层选型？', type: 'decision', edgeLabel: '存储选型',
        children: [
          { id: 'd3a', label: 'OLTP 为主？', type: 'decision',
            children: [
              { id: 'r10', label: 'PostgreSQL', type: 'result', edgeLabel: 'Yes', edgeColor: '#10B981' },
              { id: 'r11', label: 'ClickHouse', type: 'result', edgeLabel: 'OLAP' }
            ]
          },
          { id: 'r12', label: 'Redis 缓存层', type: 'external', edgeLabel: '缓存' }
        ]
      }
    ]
  };

'''

# L4: depth=4, very wide, many branches, long labels
L4_data = '''
(function() {
  var svg = document.getElementById('canvas');

  // --- 数据定义 ---
  var tree = {
    id: 'root', label: '技术方案决策', type: 'root',
    children: [
      { id: 'd1', label: '后端语言选型', type: 'decision', edgeLabel: '核心服务语言',
        children: [
          { id: 'd1a', label: '需要高并发？', type: 'decision', edgeLabel: '性能优先',
            children: [
              { id: 'd1a1', label: '团队有 Go 经验？', type: 'decision', edgeLabel: 'Yes',
                children: [
                  { id: 'r1', label: 'Go + Gin 框架', type: 'result', edgeLabel: 'Yes', edgeColor: '#10B981' },
                  { id: 'r2', label: 'Rust + Axum', type: 'result', edgeLabel: 'No' }
                ]
              },
              { id: 'r3', label: 'Java 虚拟线程', type: 'result', edgeLabel: 'No' }
            ]
          },
          { id: 'd1b', label: '快速原型验证？', type: 'decision', edgeLabel: '效率优先',
            children: [
              { id: 'r4', label: 'Python FastAPI', type: 'result', edgeLabel: 'AI/ML', edgeColor: '#10B981' },
              { id: 'r5', label: 'Node.js Fastify', type: 'result', edgeLabel: '全栈' },
              { id: 'r6', label: 'Ruby on Rails', type: 'result', edgeLabel: 'CRUD' }
            ]
          }
        ]
      },
      { id: 'd2', label: '消息队列选型', type: 'decision', edgeLabel: '异步通信',
        children: [
          { id: 'd2a', label: '需要顺序消费？', type: 'decision', edgeLabel: '消息顺序',
            children: [
              { id: 'r7', label: 'RocketMQ 顺序消息', type: 'result', edgeLabel: 'Yes', edgeColor: '#10B981' },
              { id: 'r8', label: 'Kafka 分区有序', type: 'result', edgeLabel: '分区级' }
            ]
          },
          { id: 'd2b', label: '延迟消息需求？', type: 'decision', edgeLabel: '特殊场景',
            children: [
              { id: 'r9', label: 'RabbitMQ 延迟插件', type: 'result', edgeLabel: 'Yes', edgeColor: '#10B981' },
              { id: 'r10', label: 'Pulsar', type: 'external', edgeLabel: '多租户' }
            ]
          }
        ]
      },
      { id: 'd3', label: '容器编排方案', type: 'decision', edgeLabel: '部署运维',
        children: [
          { id: 'd3a', label: '自建机房？', type: 'decision', edgeLabel: '基础设施',
            children: [
              { id: 'r11', label: 'K8s on Bare Metal', type: 'result', edgeLabel: 'Yes', edgeColor: '#10B981' },
              { id: 'd3a2', label: '多云需求？', type: 'decision', edgeLabel: 'No',
                children: [
                  { id: 'r12', label: 'Terraform + 多云 K8s', type: 'result', edgeLabel: 'Yes', edgeColor: '#10B981' },
                  { id: 'r13', label: 'AWS EKS / 阿里云 ACK', type: 'result', edgeLabel: '单云' }
                ]
              }
            ]
          },
          { id: 'r14', label: 'Serverless 函数计算', type: 'external', edgeLabel: '轻量级' }
        ]
      },
      { id: 'd4', label: '监控可观测性', type: 'decision', edgeLabel: '运维保障',
        children: [
          { id: 'd4a', label: '预算充足？', type: 'decision',
            children: [
              { id: 'r15', label: 'Datadog 全家桶', type: 'external', edgeLabel: 'SaaS' },
              { id: 'r16', label: 'Prometheus + Grafana', type: 'result', edgeLabel: '自建', edgeColor: '#10B981' }
            ]
          },
          { id: 'r17', label: 'OpenTelemetry 统一接入', type: 'result', edgeLabel: '标准化' }
        ]
      }
    ]
  };

'''

# 引擎部分（布局参数 → 绘制节点）从模板提取
# 标题在引擎中动态生成，需要在数据中包含 title 设置
# 但模板的标题是硬编码在引擎中的，我们需要用 full script approach

# 提取引擎代码（从布局参数到 IIFE 结束），然后在每个 level 中拼接不同标题
engine_before_title = engine[:engine.index("titleEl.textContent = '")]
engine_after_title_line = engine[engine.index("svg.appendChild(titleEl);"):]

titles = {
    'L1': '简单决策树',
    'L2': '数据库选型决策树',
    'L3': '系统架构选型决策树',
    'L4': '技术方案决策树',
}

test_data = {
    'L1': L1_data,
    'L2': L2_data,
    'L3': L3_data,
    'L4': L4_data,
}

for level, data in test_data.items():
    title = titles[level]
    full_engine = engine_before_title + "titleEl.textContent = '" + title + "';\n  " + engine_after_title_line
    content = head + '\n' + data + full_engine + '\n' + tail
    filename = f'decision-tree-{level}.html'
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
