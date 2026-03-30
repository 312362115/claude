"""生成 mindmap L1-L4 测试 HTML 文件"""

# 读取模板
with open('../templates/html/mindmap.html', 'r') as f:
    template = f.read()

# 提取 <script> 前的 HTML 头部（含 <script> 标签）
head_end = template.index('<script>', template.index('<script src="lib/utils.js">') + 1)
head = template[:head_end + len('<script>')]

tail = '</script>\n</body>\n</html>\n'

# --- 提取引擎部分：从 var CX 开始到 IIFE 结束 ---
# 用于 L1/L2（只替换数据，引擎不变）
engine_start = template.index('  var CX = 700, CY = 480;')
engine_end = template.index('})();') + len('})();')
engine_code = template[engine_start:engine_end]

# L1: 最小化 — 1 右分支(2 subs, 2 leaves each), 1 左分支(1 sub, 2 leaves)
L1_data = '''
(function() {
  var svg = document.getElementById('canvas');

  var colors = ['#667eea', '#f5576c', '#43e97b', '#4facfe', '#fa8231'];
  var tints = ['rgba(102,126,234,0.08)', 'rgba(245,87,108,0.08)', 'rgba(67,233,123,0.08)', 'rgba(79,172,254,0.08)', 'rgba(250,130,49,0.08)'];

  var rightBranches = [
    { name: '前端框架', color: 0, subs: [
      { name: 'React生态', leaves: ['Next.js', 'Remix'] },
      { name: 'Vue生态', leaves: ['Nuxt', 'Vite'] }
    ]}
  ];

  var leftBranches = [
    { name: '后端语言', color: 3, subs: [
      { name: '静态类型', leaves: ['Go', 'Rust'] }
    ]}
  ];

'''

# L2: 默认模板数据（3 right, 2 left），直接复用
L2_data = '''
(function() {
  var svg = document.getElementById('canvas');

  var colors = ['#667eea', '#f5576c', '#43e97b', '#4facfe', '#fa8231'];
  var tints = ['rgba(102,126,234,0.08)', 'rgba(245,87,108,0.08)', 'rgba(67,233,123,0.08)', 'rgba(79,172,254,0.08)', 'rgba(250,130,49,0.08)'];

  // 右侧 3 个分支，左侧 2 个分支
  var rightBranches = [
    { name: '服务拆分', color: 0, subs: [
      { name: '拆分原则', leaves: ['单一职责', '业务边界清晰', '数据独立性'] },
      { name: '拆分策略', leaves: ['按业务域', '按团队组织', '绞杀者模式'] },
      { name: '典型服务', leaves: ['用户', '订单', '商品', '支付'] }
    ]},
    { name: '通信机制', color: 1, subs: [
      { name: '同步通信', leaves: ['REST', 'gRPC', 'GraphQL'] },
      { name: '异步通信', leaves: ['MQ', 'Event Bus', '发布订阅'] },
      { name: '服务发现', leaves: ['Nacos', 'DNS', '客户端负载'] }
    ]},
    { name: '数据管理', color: 2, subs: [
      { name: '数据库策略', leaves: ['独立DB', '读写分离', '分库分表'] },
      { name: '数据一致性', leaves: ['Saga', 'TCC', '最终一致'] },
      { name: '缓存策略', leaves: ['本地', 'Redis', '多级'] }
    ]}
  ];

  var leftBranches = [
    { name: '部署运维', color: 3, subs: [
      { name: '容器化', leaves: ['Docker', 'K8s', 'Helm'] },
      { name: 'CI/CD', leaves: ['GitLab CI', '蓝绿', '金丝雀'] },
      { name: '可观测性', leaves: ['ELK', 'Prometheus', 'Jaeger'] }
    ]},
    { name: '安全治理', color: 4, subs: [
      { name: '认证鉴权', leaves: ['OAuth2', 'JWT', 'RBAC'] },
      { name: '流量治理', leaves: ['限流熔断', '降级', '灰度'] },
      { name: 'API网关', leaves: ['路由', '协议转换', '安全'] }
    ]}
  ];

'''

# L3: 3 right, 3 left，更多 subs 和 leaves（full script，调整 CY）
L3_script = '''
(function() {
  var svg = document.getElementById('canvas');

  var colors = ['#667eea', '#f5576c', '#43e97b', '#4facfe', '#fa8231', '#a855f7'];
  var tints = ['rgba(102,126,234,0.08)', 'rgba(245,87,108,0.08)', 'rgba(67,233,123,0.08)', 'rgba(79,172,254,0.08)', 'rgba(250,130,49,0.08)', 'rgba(168,85,247,0.08)'];

  var rightBranches = [
    { name: '需求分析', color: 0, subs: [
      { name: '用户调研', leaves: ['问卷调查', '用户访谈', '竞品分析', '数据埋点'] },
      { name: '需求梳理', leaves: ['用户故事', '优先级矩阵', '需求文档', 'PRD评审'] },
      { name: '原型设计', leaves: ['低保真', '高保真', '交互说明', '设计走查'] }
    ]},
    { name: '技术架构', color: 1, subs: [
      { name: '前端技术', leaves: ['React', 'Vue', 'SSR', '微前端'] },
      { name: '后端技术', leaves: ['Spring Boot', 'Go Gin', 'Node.js', 'gRPC'] },
      { name: '中间件', leaves: ['Redis', 'Kafka', 'Elasticsearch', 'Nginx'] },
      { name: '数据层', leaves: ['MySQL', 'PostgreSQL', 'MongoDB', 'ClickHouse'] }
    ]},
    { name: '质量保障', color: 2, subs: [
      { name: '测试策略', leaves: ['单元测试', '集成测试', 'E2E测试', '性能测试'] },
      { name: '代码质量', leaves: ['Code Review', 'SonarQube', 'ESLint', '覆盖率'] },
      { name: 'CI/CD', leaves: ['Jenkins', 'GitHub Actions', '蓝绿发布', '灰度'] }
    ]}
  ];

  var leftBranches = [
    { name: '团队协作', color: 3, subs: [
      { name: '项目管理', leaves: ['Scrum', 'Kanban', 'OKR', '周报复盘'] },
      { name: '文档规范', leaves: ['Confluence', 'Notion', 'API文档', '架构图'] },
      { name: '沟通工具', leaves: ['飞书', 'Slack', 'GitLab', 'Figma'] }
    ]},
    { name: '运维监控', color: 4, subs: [
      { name: '基础设施', leaves: ['K8s集群', 'Docker', 'Terraform', 'Ansible'] },
      { name: '监控告警', leaves: ['Prometheus', 'Grafana', 'PagerDuty', '自定义'] },
      { name: '日志分析', leaves: ['ELK', 'Loki', '链路追踪', '错误聚合'] }
    ]},
    { name: '安全合规', color: 5, subs: [
      { name: '应用安全', leaves: ['OAuth2', 'WAF', 'XSS防护', 'CSRF防护'] },
      { name: '数据安全', leaves: ['加密存储', '脱敏', '审计日志', 'GDPR'] },
      { name: '运营安全', leaves: ['权限管理', '操作审计', '灾备', '演练'] }
    ]}
  ];

  var CX = 700, CY = 540;

  function textW(str, size) {
    var w = 0;
    for (var i = 0; i < str.length; i++) w += str.charCodeAt(i) > 127 ? size : size * 0.6;
    return w;
  }

  var LEAF_H = 22;
  var SUB_GAP = 10;
  var BRANCH_GAP = 28;

  function layoutSide(branches, dir) {
    var branchX = CX + dir * 160;
    var subX = CX + dir * 340;
    var leafX = CX + dir * 530;

    var layouts = [];
    var totalH = 0;
    branches.forEach(function(branch, bi) {
      var subLayouts = [];
      var branchH = 0;
      branch.subs.forEach(function(sub, si) {
        var subH = sub.leaves.length * LEAF_H;
        subLayouts.push({ name: sub.name, leaves: sub.leaves, h: subH, localY: branchH });
        branchH += subH + (si < branch.subs.length - 1 ? SUB_GAP : 0);
      });
      layouts.push({ name: branch.name, ci: branch.color, subs: subLayouts, h: branchH });
      totalH += branchH + (bi < branches.length - 1 ? BRANCH_GAP : 0);
    });

    var startY;
    if (layouts.length % 2 === 1) {
      var midIdx = Math.floor(layouts.length / 2);
      var aboveH = 0;
      for (var i = 0; i < midIdx; i++) aboveH += layouts[i].h + BRANCH_GAP;
      startY = CY - aboveH - layouts[midIdx].h / 2;
    } else {
      startY = CY - totalH / 2;
    }

    var curY = startY;
    layouts.forEach(function(bl, bi) {
      bl.y = curY;
      bl.centerY = curY + bl.h / 2;
      bl.subs.forEach(function(sl) {
        sl.y = curY + sl.localY;
        sl.centerY = curY + sl.localY + sl.h / 2;
      });
      curY += bl.h + BRANCH_GAP;
    });

    return { layouts: layouts, branchX: branchX, subX: subX, leafX: leafX, dir: dir };
  }

  var rightSide = layoutSide(rightBranches, 1);
  var leftSide = layoutSide(leftBranches, -1);
  var allSides = [rightSide, leftSide];

  var defs = el('defs', {});
  var filter = el('filter', { id: 'shadow', x: '-10%', y: '-10%', width: '120%', height: '130%' });
  filter.appendChild(el('feDropShadow', { dx: 0, dy: 2, stdDeviation: 3, 'flood-color': 'rgba(0,0,0,0.06)' }));
  defs.appendChild(filter);
  svg.appendChild(defs);

  function addCurve(x1, y1, x2, y2, color, opacity, width) {
    var cpx = (x1 + x2) / 2;
    svg.appendChild(el('path', {
      d: 'M' + x1 + ',' + y1 + ' C' + cpx + ',' + y1 + ' ' + cpx + ',' + y2 + ' ' + x2 + ',' + y2,
      stroke: color, 'stroke-width': width || 2, fill: 'none', opacity: opacity || 0.4
    }));
  }

  var titleEl = el('text', { x: CX, y: 36, 'text-anchor': 'middle', 'font-size': 22, 'font-weight': 700, fill: '#1a1a2e' });
  titleEl.textContent = '思维导图 — 软件研发全景';
  svg.appendChild(titleEl);

  allSides.forEach(function(side) {
    var dir = side.dir;
    side.layouts.forEach(function(bl) {
      var ci = bl.ci;
      var color = colors[ci];
      var rootEdge = CX + dir * 80;
      addCurve(rootEdge, CY, side.branchX + dir * (textW(bl.name, 14) / 2 + 14) * (-1), bl.centerY, color, 0.35, 2.5);

      var bw = textW(bl.name, 14) + 28;
      var bEdge = side.branchX + dir * bw / 2;
      bl.subs.forEach(function(sl) {
        var sw = textW(sl.name, 12) + 20;
        addCurve(bEdge, bl.centerY, side.subX - dir * sw / 2, sl.centerY, color, 0.3, 1.5);
      });

      bl.subs.forEach(function(sl) {
        var sw = textW(sl.name, 12) + 20;
        var sEdge = side.subX + dir * sw / 2;
        sl.leaves.forEach(function(leaf, li) {
          var ly = sl.y + li * LEAF_H + LEAF_H / 2;
          addCurve(sEdge, sl.centerY, side.leafX - dir * 4, ly, color, 0.2, 1);
        });
      });
    });
  });

  var rootLabel = '软件研发全景';
  var rootW = textW(rootLabel, 16) + 36;
  svg.appendChild(el('rect', {
    x: CX - rootW / 2, y: CY - 24, width: rootW, height: 48,
    rx: 16, fill: '#1a1a2e', filter: 'url(#shadow)'
  }));
  var rtxt = el('text', { x: CX, y: CY + 1, 'text-anchor': 'middle', 'dominant-baseline': 'central', 'font-size': 16, 'font-weight': 700, fill: '#fff' });
  rtxt.textContent = rootLabel;
  svg.appendChild(rtxt);

  allSides.forEach(function(side) {
    var dir = side.dir;
    side.layouts.forEach(function(bl) {
      var ci = bl.ci;
      var color = colors[ci];
      var tint = tints[ci];

      var bw = textW(bl.name, 14) + 28;
      svg.appendChild(el('rect', {
        x: side.branchX - bw / 2, y: bl.centerY - 16, width: bw, height: 32,
        rx: 10, fill: color, filter: 'url(#shadow)'
      }));
      var btxt = el('text', { x: side.branchX, y: bl.centerY + 1, 'text-anchor': 'middle', 'dominant-baseline': 'central', 'font-size': 13, 'font-weight': 600, fill: '#fff' });
      btxt.textContent = bl.name;
      svg.appendChild(btxt);

      bl.subs.forEach(function(sl) {
        var sw = textW(sl.name, 12) + 20;
        svg.appendChild(el('rect', {
          x: side.subX - sw / 2, y: sl.centerY - 13, width: sw, height: 26,
          rx: 6, fill: tint, stroke: color, 'stroke-width': 1, 'stroke-opacity': 0.3
        }));
        var stxt = el('text', { x: side.subX, y: sl.centerY + 1, 'text-anchor': 'middle', 'dominant-baseline': 'central', 'font-size': 12, 'font-weight': 600, fill: color });
        stxt.textContent = sl.name;
        svg.appendChild(stxt);

        sl.leaves.forEach(function(leaf, li) {
          var ly = sl.y + li * LEAF_H + LEAF_H / 2;
          svg.appendChild(el('circle', { cx: side.leafX, cy: ly, r: 3, fill: color, opacity: 0.5 }));
          var anchor = dir > 0 ? 'start' : 'end';
          var offset = dir * 8;
          var ltxt = el('text', { x: side.leafX + offset, y: ly + 1, 'text-anchor': anchor, 'dominant-baseline': 'central', 'font-size': 11, fill: '#64748b' });
          ltxt.textContent = leaf;
          svg.appendChild(ltxt);
        });
      });
    });
  });
})();
'''

# L4: 4 right, 3 left，4 subs/branch, 5 leaves/sub（full script，大幅增高画布）
L4_script = '''
(function() {
  var svg = document.getElementById('canvas');

  var colors = ['#667eea', '#f5576c', '#43e97b', '#4facfe', '#fa8231', '#a855f7', '#ec4899'];
  var tints = ['rgba(102,126,234,0.08)', 'rgba(245,87,108,0.08)', 'rgba(67,233,123,0.08)', 'rgba(79,172,254,0.08)', 'rgba(250,130,49,0.08)', 'rgba(168,85,247,0.08)', 'rgba(236,72,153,0.08)'];

  var rightBranches = [
    { name: '产品设计', color: 0, subs: [
      { name: '用户研究', leaves: ['问卷设计', '深度访谈', '可用性测试', '数据分析', 'A/B实验'] },
      { name: '交互设计', leaves: ['信息架构', '任务流程', '线框图', '原型制作', '动效设计'] },
      { name: '视觉设计', leaves: ['设计系统', '配色方案', '图标库', '响应式', '暗黑模式'] },
      { name: '产品策略', leaves: ['路线图', '竞品分析', '商业模型', '指标体系', 'GTM策略'] }
    ]},
    { name: '前端工程', color: 1, subs: [
      { name: '框架选型', leaves: ['React 18', 'Vue 3', 'Svelte', 'Solid.js', 'Qwik'] },
      { name: '构建工具', leaves: ['Vite', 'Turbopack', 'Rspack', 'esbuild', 'SWC'] },
      { name: '状态管理', leaves: ['Zustand', 'Jotai', 'Redux TK', 'Pinia', 'XState'] },
      { name: '测试工具', leaves: ['Vitest', 'Playwright', 'Storybook', 'Cypress', 'MSW'] }
    ]},
    { name: '后端服务', color: 2, subs: [
      { name: '语言运行时', leaves: ['Go 1.22', 'Java 21', 'Node 20', 'Rust', 'Python'] },
      { name: 'Web框架', leaves: ['Gin', 'Spring Boot', 'Fastify', 'Axum', 'FastAPI'] },
      { name: '数据存储', leaves: ['PostgreSQL', 'MySQL 8', 'MongoDB 7', 'Redis 7', 'TiDB'] },
      { name: '消息队列', leaves: ['Kafka', 'RocketMQ', 'Pulsar', 'NATS', 'RabbitMQ'] }
    ]},
    { name: 'AI/ML', color: 6, subs: [
      { name: '大模型', leaves: ['GPT-4', 'Claude', 'Gemini', 'Llama 3', 'Mistral'] },
      { name: '训练框架', leaves: ['PyTorch', 'JAX', 'TensorFlow', 'DeepSpeed', 'Megatron'] },
      { name: '推理部署', leaves: ['vLLM', 'TensorRT', 'ONNX', 'Triton', 'TGI'] },
      { name: '应用场景', leaves: ['RAG', 'Agent', '代码生成', '图像生成', '语音合成'] }
    ]}
  ];

  var leftBranches = [
    { name: '平台工程', color: 3, subs: [
      { name: '容器编排', leaves: ['Kubernetes', 'Docker', 'Helm', 'Kustomize', 'Istio'] },
      { name: 'CI/CD', leaves: ['GitHub Actions', 'ArgoCD', 'Tekton', 'Jenkins', 'Flux'] },
      { name: 'IaC', leaves: ['Terraform', 'Pulumi', 'Ansible', 'Crossplane', 'CDK'] },
      { name: '开发者平台', leaves: ['Backstage', 'Port', '内部门户', '自助工具', 'CLI'] }
    ]},
    { name: '可观测性', color: 4, subs: [
      { name: '指标监控', leaves: ['Prometheus', 'Grafana', 'Datadog', 'VictoriaMetrics', 'Thanos'] },
      { name: '日志管理', leaves: ['Loki', 'Elasticsearch', 'Fluentd', 'Vector', 'ClickHouse'] },
      { name: '链路追踪', leaves: ['Jaeger', 'Tempo', 'Zipkin', 'SkyWalking', 'OpenTelemetry'] },
      { name: '告警运维', leaves: ['PagerDuty', 'OpsGenie', 'Alertmanager', 'Incident.io', 'Rootly'] }
    ]},
    { name: '安全治理', color: 5, subs: [
      { name: '应用安全', leaves: ['OAuth 2.1', 'OIDC', 'mTLS', 'WAF', 'SAST/DAST'] },
      { name: '数据合规', leaves: ['GDPR', '等保2.0', '数据脱敏', '加密存储', '审计日志'] },
      { name: '供应链安全', leaves: ['SBOM', 'Sigstore', 'Trivy', 'Snyk', 'Dependabot'] },
      { name: '零信任', leaves: ['BeyondCorp', 'SPIFFE', '最小权限', '持续验证', '微隔离'] }
    ]}
  ];

  var CX = 800, CY = 940;

  function textW(str, size) {
    var w = 0;
    for (var i = 0; i < str.length; i++) w += str.charCodeAt(i) > 127 ? size : size * 0.6;
    return w;
  }

  var LEAF_H = 20;
  var SUB_GAP = 8;
  var BRANCH_GAP = 24;

  function layoutSide(branches, dir) {
    var branchX = CX + dir * 160;
    var subX = CX + dir * 340;
    var leafX = CX + dir * 500;

    var layouts = [];
    var totalH = 0;
    branches.forEach(function(branch, bi) {
      var subLayouts = [];
      var branchH = 0;
      branch.subs.forEach(function(sub, si) {
        var subH = sub.leaves.length * LEAF_H;
        subLayouts.push({ name: sub.name, leaves: sub.leaves, h: subH, localY: branchH });
        branchH += subH + (si < branch.subs.length - 1 ? SUB_GAP : 0);
      });
      layouts.push({ name: branch.name, ci: branch.color, subs: subLayouts, h: branchH });
      totalH += branchH + (bi < branches.length - 1 ? BRANCH_GAP : 0);
    });

    var startY;
    if (layouts.length % 2 === 1) {
      var midIdx = Math.floor(layouts.length / 2);
      var aboveH = 0;
      for (var i = 0; i < midIdx; i++) aboveH += layouts[i].h + BRANCH_GAP;
      startY = CY - aboveH - layouts[midIdx].h / 2;
    } else {
      startY = CY - totalH / 2;
    }

    var curY = startY;
    layouts.forEach(function(bl, bi) {
      bl.y = curY;
      bl.centerY = curY + bl.h / 2;
      bl.subs.forEach(function(sl) {
        sl.y = curY + sl.localY;
        sl.centerY = curY + sl.localY + sl.h / 2;
      });
      curY += bl.h + BRANCH_GAP;
    });

    return { layouts: layouts, branchX: branchX, subX: subX, leafX: leafX, dir: dir };
  }

  var rightSide = layoutSide(rightBranches, 1);
  var leftSide = layoutSide(leftBranches, -1);
  var allSides = [rightSide, leftSide];

  var defs = el('defs', {});
  var filter = el('filter', { id: 'shadow', x: '-10%', y: '-10%', width: '120%', height: '130%' });
  filter.appendChild(el('feDropShadow', { dx: 0, dy: 2, stdDeviation: 3, 'flood-color': 'rgba(0,0,0,0.06)' }));
  defs.appendChild(filter);
  svg.appendChild(defs);

  function addCurve(x1, y1, x2, y2, color, opacity, width) {
    var cpx = (x1 + x2) / 2;
    svg.appendChild(el('path', {
      d: 'M' + x1 + ',' + y1 + ' C' + cpx + ',' + y1 + ' ' + cpx + ',' + y2 + ' ' + x2 + ',' + y2,
      stroke: color, 'stroke-width': width || 2, fill: 'none', opacity: opacity || 0.4
    }));
  }

  var titleEl = el('text', { x: CX, y: 36, 'text-anchor': 'middle', 'font-size': 22, 'font-weight': 700, fill: '#1a1a2e' });
  titleEl.textContent = '思维导图 — 技术团队能力全景';
  svg.appendChild(titleEl);

  allSides.forEach(function(side) {
    var dir = side.dir;
    side.layouts.forEach(function(bl) {
      var ci = bl.ci;
      var color = colors[ci];
      var rootEdge = CX + dir * 80;
      addCurve(rootEdge, CY, side.branchX + dir * (textW(bl.name, 14) / 2 + 14) * (-1), bl.centerY, color, 0.35, 2.5);

      var bw = textW(bl.name, 14) + 28;
      var bEdge = side.branchX + dir * bw / 2;
      bl.subs.forEach(function(sl) {
        var sw = textW(sl.name, 12) + 20;
        addCurve(bEdge, bl.centerY, side.subX - dir * sw / 2, sl.centerY, color, 0.3, 1.5);
      });

      bl.subs.forEach(function(sl) {
        var sw = textW(sl.name, 12) + 20;
        var sEdge = side.subX + dir * sw / 2;
        sl.leaves.forEach(function(leaf, li) {
          var ly = sl.y + li * LEAF_H + LEAF_H / 2;
          addCurve(sEdge, sl.centerY, side.leafX - dir * 4, ly, color, 0.2, 1);
        });
      });
    });
  });

  var rootLabel = '技术团队能力全景';
  var rootW = textW(rootLabel, 16) + 36;
  svg.appendChild(el('rect', {
    x: CX - rootW / 2, y: CY - 24, width: rootW, height: 48,
    rx: 16, fill: '#1a1a2e', filter: 'url(#shadow)'
  }));
  var rtxt = el('text', { x: CX, y: CY + 1, 'text-anchor': 'middle', 'dominant-baseline': 'central', 'font-size': 16, 'font-weight': 700, fill: '#fff' });
  rtxt.textContent = rootLabel;
  svg.appendChild(rtxt);

  allSides.forEach(function(side) {
    var dir = side.dir;
    side.layouts.forEach(function(bl) {
      var ci = bl.ci;
      var color = colors[ci];
      var tint = tints[ci];

      var bw = textW(bl.name, 14) + 28;
      svg.appendChild(el('rect', {
        x: side.branchX - bw / 2, y: bl.centerY - 16, width: bw, height: 32,
        rx: 10, fill: color, filter: 'url(#shadow)'
      }));
      var btxt = el('text', { x: side.branchX, y: bl.centerY + 1, 'text-anchor': 'middle', 'dominant-baseline': 'central', 'font-size': 13, 'font-weight': 600, fill: '#fff' });
      btxt.textContent = bl.name;
      svg.appendChild(btxt);

      bl.subs.forEach(function(sl) {
        var sw = textW(sl.name, 12) + 20;
        svg.appendChild(el('rect', {
          x: side.subX - sw / 2, y: sl.centerY - 13, width: sw, height: 26,
          rx: 6, fill: tint, stroke: color, 'stroke-width': 1, 'stroke-opacity': 0.3
        }));
        var stxt = el('text', { x: side.subX, y: sl.centerY + 1, 'text-anchor': 'middle', 'dominant-baseline': 'central', 'font-size': 12, 'font-weight': 600, fill: color });
        stxt.textContent = sl.name;
        svg.appendChild(stxt);

        sl.leaves.forEach(function(leaf, li) {
          var ly = sl.y + li * LEAF_H + LEAF_H / 2;
          svg.appendChild(el('circle', { cx: side.leafX, cy: ly, r: 3, fill: color, opacity: 0.5 }));
          var anchor = dir > 0 ? 'start' : 'end';
          var offset = dir * 8;
          var ltxt = el('text', { x: side.leafX + offset, y: ly + 1, 'text-anchor': anchor, 'dominant-baseline': 'central', 'font-size': 11, fill: '#64748b' });
          ltxt.textContent = leaf;
          svg.appendChild(ltxt);
        });
      });
    });
  });
})();
'''

# L1/L2 用数据+引擎拼接，L3/L4 用 full script
# 但为保持一致性，全部用 full script approach

# L1 也需要 full script（引擎需要改 rootLabel 和 title）
L1_script = L1_data + '''  var CX = 700, CY = 480;

  function textW(str, size) {
    var w = 0;
    for (var i = 0; i < str.length; i++) w += str.charCodeAt(i) > 127 ? size : size * 0.6;
    return w;
  }

  var LEAF_H = 22;
  var SUB_GAP = 10;
  var BRANCH_GAP = 28;

  function layoutSide(branches, dir) {
    var branchX = CX + dir * 160;
    var subX = CX + dir * 340;
    var leafX = CX + dir * 530;

    var layouts = [];
    var totalH = 0;
    branches.forEach(function(branch, bi) {
      var subLayouts = [];
      var branchH = 0;
      branch.subs.forEach(function(sub, si) {
        var subH = sub.leaves.length * LEAF_H;
        subLayouts.push({ name: sub.name, leaves: sub.leaves, h: subH, localY: branchH });
        branchH += subH + (si < branch.subs.length - 1 ? SUB_GAP : 0);
      });
      layouts.push({ name: branch.name, ci: branch.color, subs: subLayouts, h: branchH });
      totalH += branchH + (bi < branches.length - 1 ? BRANCH_GAP : 0);
    });

    var startY;
    if (layouts.length % 2 === 1) {
      var midIdx = Math.floor(layouts.length / 2);
      var aboveH = 0;
      for (var i = 0; i < midIdx; i++) aboveH += layouts[i].h + BRANCH_GAP;
      startY = CY - aboveH - layouts[midIdx].h / 2;
    } else {
      startY = CY - totalH / 2;
    }

    var curY = startY;
    layouts.forEach(function(bl, bi) {
      bl.y = curY;
      bl.centerY = curY + bl.h / 2;
      bl.subs.forEach(function(sl) {
        sl.y = curY + sl.localY;
        sl.centerY = curY + sl.localY + sl.h / 2;
      });
      curY += bl.h + BRANCH_GAP;
    });

    return { layouts: layouts, branchX: branchX, subX: subX, leafX: leafX, dir: dir };
  }

  var rightSide = layoutSide(rightBranches, 1);
  var leftSide = layoutSide(leftBranches, -1);
  var allSides = [rightSide, leftSide];

  var defs = el('defs', {});
  var filter = el('filter', { id: 'shadow', x: '-10%', y: '-10%', width: '120%', height: '130%' });
  filter.appendChild(el('feDropShadow', { dx: 0, dy: 2, stdDeviation: 3, 'flood-color': 'rgba(0,0,0,0.06)' }));
  defs.appendChild(filter);
  svg.appendChild(defs);

  function addCurve(x1, y1, x2, y2, color, opacity, width) {
    var cpx = (x1 + x2) / 2;
    svg.appendChild(el('path', {
      d: 'M' + x1 + ',' + y1 + ' C' + cpx + ',' + y1 + ' ' + cpx + ',' + y2 + ' ' + x2 + ',' + y2,
      stroke: color, 'stroke-width': width || 2, fill: 'none', opacity: opacity || 0.4
    }));
  }

  var titleEl = el('text', { x: CX, y: 36, 'text-anchor': 'middle', 'font-size': 22, 'font-weight': 700, fill: '#1a1a2e' });
  titleEl.textContent = '思维导图 — 技术选型';
  svg.appendChild(titleEl);

  allSides.forEach(function(side) {
    var dir = side.dir;
    side.layouts.forEach(function(bl) {
      var ci = bl.ci;
      var color = colors[ci];
      var rootEdge = CX + dir * 80;
      addCurve(rootEdge, CY, side.branchX + dir * (textW(bl.name, 14) / 2 + 14) * (-1), bl.centerY, color, 0.35, 2.5);

      var bw = textW(bl.name, 14) + 28;
      var bEdge = side.branchX + dir * bw / 2;
      bl.subs.forEach(function(sl) {
        var sw = textW(sl.name, 12) + 20;
        addCurve(bEdge, bl.centerY, side.subX - dir * sw / 2, sl.centerY, color, 0.3, 1.5);
      });

      bl.subs.forEach(function(sl) {
        var sw = textW(sl.name, 12) + 20;
        var sEdge = side.subX + dir * sw / 2;
        sl.leaves.forEach(function(leaf, li) {
          var ly = sl.y + li * LEAF_H + LEAF_H / 2;
          addCurve(sEdge, sl.centerY, side.leafX - dir * 4, ly, color, 0.2, 1);
        });
      });
    });
  });

  var rootLabel = '技术选型';
  var rootW = textW(rootLabel, 16) + 36;
  svg.appendChild(el('rect', {
    x: CX - rootW / 2, y: CY - 24, width: rootW, height: 48,
    rx: 16, fill: '#1a1a2e', filter: 'url(#shadow)'
  }));
  var rtxt = el('text', { x: CX, y: CY + 1, 'text-anchor': 'middle', 'dominant-baseline': 'central', 'font-size': 16, 'font-weight': 700, fill: '#fff' });
  rtxt.textContent = rootLabel;
  svg.appendChild(rtxt);

  allSides.forEach(function(side) {
    var dir = side.dir;
    side.layouts.forEach(function(bl) {
      var ci = bl.ci;
      var color = colors[ci];
      var tint = tints[ci];

      var bw = textW(bl.name, 14) + 28;
      svg.appendChild(el('rect', {
        x: side.branchX - bw / 2, y: bl.centerY - 16, width: bw, height: 32,
        rx: 10, fill: color, filter: 'url(#shadow)'
      }));
      var btxt = el('text', { x: side.branchX, y: bl.centerY + 1, 'text-anchor': 'middle', 'dominant-baseline': 'central', 'font-size': 13, 'font-weight': 600, fill: '#fff' });
      btxt.textContent = bl.name;
      svg.appendChild(btxt);

      bl.subs.forEach(function(sl) {
        var sw = textW(sl.name, 12) + 20;
        svg.appendChild(el('rect', {
          x: side.subX - sw / 2, y: sl.centerY - 13, width: sw, height: 26,
          rx: 6, fill: tint, stroke: color, 'stroke-width': 1, 'stroke-opacity': 0.3
        }));
        var stxt = el('text', { x: side.subX, y: sl.centerY + 1, 'text-anchor': 'middle', 'dominant-baseline': 'central', 'font-size': 12, 'font-weight': 600, fill: color });
        stxt.textContent = sl.name;
        svg.appendChild(stxt);

        sl.leaves.forEach(function(leaf, li) {
          var ly = sl.y + li * LEAF_H + LEAF_H / 2;
          svg.appendChild(el('circle', { cx: side.leafX, cy: ly, r: 3, fill: color, opacity: 0.5 }));
          var anchor = dir > 0 ? 'start' : 'end';
          var offset = dir * 8;
          var ltxt = el('text', { x: side.leafX + offset, y: ly + 1, 'text-anchor': anchor, 'dominant-baseline': 'central', 'font-size': 11, fill: '#64748b' });
          ltxt.textContent = leaf;
          svg.appendChild(ltxt);
        });
      });
    });
  });
})();
'''

# L2 也用 full script 以保持模板数据完全一致
L2_script = L2_data + engine_code

# 不同 level 对应不同 HTML head（L3/L4 需调整 viewport 和 canvas 高度）
def make_head(width, height, title):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={width}, height={height}">
<title>思维导图 - {title}</title>
<link rel="stylesheet" href="lib/base.css">
</head>
<body style="width:{width}px;height:{height}px;display:inline-block;text-align:center;">
<svg id="canvas" width="{width}" height="{height}" viewBox="0 0 {width} {height}"></svg>

<script src="lib/utils.js"></script>
<script>
'''

test_data = {
    'L1': (make_head(1400, 960, '技术选型'), L1_script),
    'L2': (make_head(1400, 960, '微服务架构设计'), L2_script),
    'L3': (make_head(1400, 1100, '软件研发全景'), L3_script),
    'L4': (make_head(1600, 1880, '技术团队能力全景'), L4_script),
}

for level, (html_head, script) in test_data.items():
    content = html_head + script + '\n</script>\n</body>\n</html>\n'
    filename = f'mindmap-{level}.html'
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
