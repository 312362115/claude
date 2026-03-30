"""生成 c4 L1-L4 测试 HTML 文件"""

# 读取模板
with open('../templates/html/c4.html', 'r') as f:
    template = f.read()

# C4 模板的 HTML head 部分（到 <script> 标签）
head_end = template.index('<script>', template.index('<script src="lib/utils.js">') + 1)
head = template[:head_end + len('<script>')]

tail = '</script>\n</body>\n</html>\n'

# 提取模板中 IIFE 内的完整脚本（从 (function() 到 })();）
iife_start = template.index('(function() {')
iife_end = template.index('})();') + len('})();')
original_script = template[iife_start:iife_end]


def make_c4_script(title, subtitle, persons, frontend_nodes, backend_nodes, data_nodes, externals,
                   arrow_labels=None):
    """生成完整的 C4 IIFE 脚本"""
    if arrow_labels is None:
        arrow_labels = ['HTTPS', 'REST / gRPC', 'JDBC / TCP', 'HTTPS']

    # 生成 persons JS 数组
    persons_js = '[\n'
    for p in persons:
        persons_js += f"    {{ id: '{p['id']}', name: '{p['name']}', desc: '{p['desc']}' }},\n"
    persons_js += '  ]'

    # 生成 frontendNodes JS 数组
    frontend_js = '[\n'
    for n in frontend_nodes:
        frontend_js += f"    {{ name: '{n['name']}', tech: '{n['tech']}', desc: '{n['desc']}' }},\n"
    frontend_js += '  ]'

    # 生成 backendNodes JS 数组
    backend_js = '[\n'
    for n in backend_nodes:
        backend_js += f"    {{ name: '{n['name']}', tech: '{n['tech']}', desc: '{n['desc']}' }},\n"
    backend_js += '  ]'

    # 生成 dataNodes JS 数组
    data_js = '[\n'
    for n in data_nodes:
        data_js += f"    {{ name: '{n['name']}', tech: '{n['tech']}', desc: '{n['desc']}' }},\n"
    data_js += '  ]'

    # 生成 externals JS 数组
    externals_js = '[\n'
    for n in externals:
        externals_js += f"    {{ name: '{n['name']}', tag: '{n['tag']}' }},\n"
    externals_js += '  ]'

    return f'''(function() {{
  // ===== 配置 =====
  var FONT = "-apple-system, system-ui, 'PingFang SC', sans-serif";
  var PAD = 40;           // 画布边距
  var ROW_GAP = 50;       // 层间距（箭头空间）
  var NODE_GAP = 16;      // 节点间距
  var LAYER_PAD_X = 20;   // 层容器内边距
  var LAYER_PAD_Y = 32;   // 层容器上方内边距（给标签留空）
  var LAYER_PAD_B = 16;   // 层容器底部内边距

  // 节点尺寸
  var PERSON_W = 100, PERSON_H = 80;
  var CONTAINER_W = 150, CONTAINER_H = 70;
  var EXTERNAL_W = 130, EXTERNAL_H = 50;

  // 颜色
  var COLOR = {{
    person: '#3B82F6',
    frontend: '#667eea',
    backend: '#43e97b',
    data: '#4facfe',
    arrow: '#94A3B8',
    title: '#1a1a2e',
    subtitle: '#64748B',
    layerLabel: '#475569',
    externalBorder: '#94A3B8'
  }};

  // ===== 数据 =====
  var persons = {persons_js};

  var frontendNodes = {frontend_js};

  var backendNodes = {backend_js};

  var dataNodes = {data_js};

  var externals = {externals_js};

  // ===== 布局计算 =====
  function rowWidth(count, nodeW) {{
    return count * nodeW + (count - 1) * NODE_GAP;
  }}

  // 找出最宽的行，确定画布宽度
  var layerContentWidths = [
    rowWidth(persons.length, PERSON_W),
    rowWidth(frontendNodes.length, CONTAINER_W),
    rowWidth(backendNodes.length, CONTAINER_W),
    rowWidth(dataNodes.length, CONTAINER_W),
    rowWidth(externals.length, EXTERNAL_W)
  ];

  // 层容器需要额外的内边距
  var layerBoxWidths = [
    layerContentWidths[0],  // persons 无层容器
    layerContentWidths[1] + LAYER_PAD_X * 2,
    layerContentWidths[2] + LAYER_PAD_X * 2,
    layerContentWidths[3] + LAYER_PAD_X * 2,
    layerContentWidths[4]   // externals 无层容器
  ];

  var maxLayerW = Math.max.apply(null, layerBoxWidths);
  var canvasW = maxLayerW + PAD * 2;

  // Y 坐标布局
  var titleY = 30;
  var subtitleY = titleY + 22;
  var startY = subtitleY + 36;

  // Row 0: Persons
  var personsY = startY;
  var personsRowH = PERSON_H;

  // Row 1: Frontend layer
  var frontendLayerY = personsY + personsRowH + ROW_GAP;
  var frontendLayerH = LAYER_PAD_Y + CONTAINER_H + LAYER_PAD_B;

  // Row 2: Backend layer
  var backendLayerY = frontendLayerY + frontendLayerH + ROW_GAP;
  var backendLayerH = LAYER_PAD_Y + CONTAINER_H + LAYER_PAD_B;

  // Row 3: Data layer
  var dataLayerY = backendLayerY + backendLayerH + ROW_GAP;
  var dataLayerH = LAYER_PAD_Y + CONTAINER_H + LAYER_PAD_B;

  // Row 4: External
  var externalY = dataLayerY + dataLayerH + ROW_GAP;
  var externalRowH = EXTERNAL_H;

  var canvasH = externalY + externalRowH + PAD;
  var cx = canvasW / 2; // 中心 x

  // ===== SVG 构建辅助 =====
  var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  svg.setAttribute('width', canvasW);
  svg.setAttribute('height', canvasH);
  svg.setAttribute('viewBox', '0 0 ' + canvasW + ' ' + canvasH);
  svg.style.display = 'block';

  function el(tag, attrs) {{
    var e = document.createElementNS('http://www.w3.org/2000/svg', tag);
    for (var key in attrs || {{}}) {{
      if (attrs.hasOwnProperty(key)) e.setAttribute(key, attrs[key]);
    }}
    return e;
  }}

  function text(str, x, y, attrs) {{
    var t = el('text', Object.assign({{
      x: x, y: y,
      'font-family': FONT,
      'text-anchor': 'middle',
      'dominant-baseline': 'middle'
    }}, attrs || {{}}));
    t.textContent = str;
    return t;
  }}

  // ===== Defs: arrow marker =====
  var defs = el('defs');
  var marker = el('marker', {{
    id: 'arrowhead',
    markerWidth: '8', markerHeight: '6',
    refX: '8', refY: '3',
    orient: 'auto'
  }});
  marker.appendChild(el('path', {{ d: 'M0,0 L8,3 L0,6 Z', fill: COLOR.arrow }}));
  defs.appendChild(marker);
  svg.appendChild(defs);

  // ===== Group 1: Lines (drawn first, behind everything) =====
  var linesGroup = el('g', {{ id: 'lines' }});
  svg.appendChild(linesGroup);

  // ===== Group 2: Nodes (drawn on top) =====
  var nodesGroup = el('g', {{ id: 'nodes' }});
  svg.appendChild(nodesGroup);

  // ===== Title =====
  nodesGroup.appendChild(text('{title}', cx, titleY, {{
    'font-size': '22', 'font-weight': 'bold', fill: COLOR.title
  }}));
  nodesGroup.appendChild(text('{subtitle}', cx, subtitleY, {{
    'font-size': '13', fill: COLOR.subtitle
  }}));

  // ===== 绘制人物节点 =====
  function drawPerson(node, px, py) {{
    var g = el('g');
    // 圆角矩形背景
    g.appendChild(el('rect', {{
      x: px, y: py, width: PERSON_W, height: PERSON_H,
      rx: '10', ry: '10', fill: COLOR.person
    }}));
    // 人物图标：头（圆）+ 身体（梯形简化为圆角矩形）
    var iconCx = px + PERSON_W / 2;
    var iconCy = py + 22;
    g.appendChild(el('circle', {{
      cx: iconCx, cy: iconCy, r: '8', fill: 'none', stroke: '#fff', 'stroke-width': '1.5'
    }}));
    g.appendChild(el('path', {{
      d: 'M' + (iconCx - 12) + ',' + (iconCy + 18) +
         ' Q' + (iconCx - 12) + ',' + (iconCy + 10) + ' ' + iconCx + ',' + (iconCy + 10) +
         ' Q' + (iconCx + 12) + ',' + (iconCy + 10) + ' ' + (iconCx + 12) + ',' + (iconCy + 18),
      fill: 'none', stroke: '#fff', 'stroke-width': '1.5'
    }}));
    // 名称
    g.appendChild(text(node.name, px + PERSON_W / 2, py + PERSON_H - 12, {{
      'font-size': '12', 'font-weight': '600', fill: '#fff'
    }}));
    nodesGroup.appendChild(g);
  }}

  var personsTotalW = rowWidth(persons.length, PERSON_W);
  var personsStartX = cx - personsTotalW / 2;
  persons.forEach(function(p, i) {{
    var px = personsStartX + i * (PERSON_W + NODE_GAP);
    drawPerson(p, px, personsY);
  }});

  // ===== 绘制层容器背景 =====
  function drawLayerBg(layerY, layerH, fillColor, label, contentW) {{
    var layerW = contentW + LAYER_PAD_X * 2;
    var lx = cx - layerW / 2;
    var g = el('g');
    g.appendChild(el('rect', {{
      x: lx, y: layerY, width: layerW, height: layerH,
      rx: '12', ry: '12',
      fill: fillColor, 'fill-opacity': '0.06',
      stroke: fillColor, 'stroke-opacity': '0.2', 'stroke-width': '1'
    }}));
    g.appendChild(text(label, lx + 12, layerY + 14, {{
      'font-size': '11', 'font-weight': '600', fill: COLOR.layerLabel,
      'text-anchor': 'start', 'dominant-baseline': 'middle',
      'letter-spacing': '0.5'
    }}));
    nodesGroup.appendChild(g);
    return {{ x: lx, w: layerW }};
  }}

  // ===== 绘制容器节点 =====
  function drawContainer(node, px, py, fillColor) {{
    var g = el('g');
    g.appendChild(el('rect', {{
      x: px, y: py, width: CONTAINER_W, height: CONTAINER_H,
      rx: '8', ry: '8', fill: fillColor
    }}));
    g.appendChild(text(node.name, px + CONTAINER_W / 2, py + 18, {{
      'font-size': '13', 'font-weight': 'bold', fill: '#fff'
    }}));
    g.appendChild(text(node.tech, px + CONTAINER_W / 2, py + 35, {{
      'font-size': '11', 'font-style': 'italic', fill: '#fff', 'fill-opacity': '0.85'
    }}));
    g.appendChild(text(node.desc, px + CONTAINER_W / 2, py + 52, {{
      'font-size': '10', fill: '#fff', 'fill-opacity': '0.75'
    }}));
    nodesGroup.appendChild(g);
  }}

  // Frontend layer
  var fContentW = rowWidth(frontendNodes.length, CONTAINER_W);
  drawLayerBg(frontendLayerY, frontendLayerH, COLOR.frontend, 'Frontend', fContentW);
  var fStartX = cx - fContentW / 2;
  frontendNodes.forEach(function(n, i) {{
    drawContainer(n, fStartX + i * (CONTAINER_W + NODE_GAP), frontendLayerY + LAYER_PAD_Y, COLOR.frontend);
  }});

  // Backend layer
  var bContentW = rowWidth(backendNodes.length, CONTAINER_W);
  drawLayerBg(backendLayerY, backendLayerH, COLOR.backend, 'Backend Services', bContentW);
  var bStartX = cx - bContentW / 2;
  backendNodes.forEach(function(n, i) {{
    drawContainer(n, bStartX + i * (CONTAINER_W + NODE_GAP), backendLayerY + LAYER_PAD_Y, COLOR.backend);
  }});

  // Data layer
  var dContentW = rowWidth(dataNodes.length, CONTAINER_W);
  drawLayerBg(dataLayerY, dataLayerH, COLOR.data, 'Data Stores', dContentW);
  var dStartX = cx - dContentW / 2;
  dataNodes.forEach(function(n, i) {{
    drawContainer(n, dStartX + i * (CONTAINER_W + NODE_GAP), dataLayerY + LAYER_PAD_Y, COLOR.data);
  }});

  // ===== 绘制外部系统 =====
  function drawExternal(node, px, py) {{
    var g = el('g');
    g.appendChild(el('rect', {{
      x: px, y: py, width: EXTERNAL_W, height: EXTERNAL_H,
      rx: '8', ry: '8',
      fill: 'none', stroke: COLOR.externalBorder,
      'stroke-width': '1.5', 'stroke-dasharray': '6 3'
    }}));
    g.appendChild(text(node.name, px + EXTERNAL_W / 2, py + 19, {{
      'font-size': '13', 'font-weight': '600', fill: '#475569'
    }}));
    g.appendChild(text('[' + node.tag + ']', px + EXTERNAL_W / 2, py + 36, {{
      'font-size': '10', fill: COLOR.externalBorder
    }}));
    nodesGroup.appendChild(g);
  }}

  var eTotalW = rowWidth(externals.length, EXTERNAL_W);
  var eStartX = cx - eTotalW / 2;
  externals.forEach(function(n, i) {{
    drawExternal(n, eStartX + i * (EXTERNAL_W + NODE_GAP), externalY);
  }});

  // ===== 绘制 4 条层间箭头 =====
  function drawArrow(y1, y2, label) {{
    // 直线从中心向下
    var line = el('line', {{
      x1: cx, y1: y1, x2: cx, y2: y2,
      stroke: COLOR.arrow, 'stroke-width': '1.5',
      'marker-end': 'url(#arrowhead)'
    }});
    linesGroup.appendChild(line);

    // 标签
    if (label) {{
      var midY = (y1 + y2) / 2;
      // 白色背景让标签不被线挡住
      var labelEl = text(label, cx, midY, {{
        'font-size': '11', fill: COLOR.subtitle,
        'font-weight': '500'
      }});
      // 先算标签宽度，用一个白色矩形做背景
      var bgRect = el('rect', {{
        x: cx - 30, y: midY - 9,
        width: 60, height: 18,
        rx: '4', ry: '4', fill: '#ffffff'
      }});
      linesGroup.appendChild(bgRect);
      linesGroup.appendChild(labelEl);
    }}
  }}

  // Arrow 1: Persons → Frontend
  drawArrow(
    personsY + PERSON_H,
    frontendLayerY,
    '{arrow_labels[0]}'
  );

  // Arrow 2: Frontend → Backend
  drawArrow(
    frontendLayerY + frontendLayerH,
    backendLayerY,
    '{arrow_labels[1]}'
  );

  // Arrow 3: Backend → Data
  drawArrow(
    backendLayerY + backendLayerH,
    dataLayerY,
    '{arrow_labels[2]}'
  );

  // Arrow 4: Backend → External
  drawArrow(
    dataLayerY + dataLayerH,
    externalY,
    '{arrow_labels[3]}'
  );

  // ===== 挂载 =====
  document.body.appendChild(svg);
}})();'''


# ===== L1: 1 person, 2 frontend, 2 backend, 1 data, 1 external =====
L1 = make_c4_script(
    title='博客系统 · C4 容器图',
    subtitle='Container Diagram — 简单博客系统架构',
    persons=[
        {'id': 'user', 'name': '用户', 'desc': '阅读和发布文章'},
    ],
    frontend_nodes=[
        {'name': '博客前端', 'tech': 'React', 'desc': '文章展示与编辑'},
        {'name': '管理后台', 'tech': 'Vue 3', 'desc': '内容管理'},
    ],
    backend_nodes=[
        {'name': 'API服务', 'tech': 'Node.js, Express', 'desc': 'RESTful API'},
        {'name': '认证服务', 'tech': 'Node.js', 'desc': '登录注册'},
    ],
    data_nodes=[
        {'name': 'PostgreSQL', 'tech': 'PG 15', 'desc': '文章与用户数据'},
    ],
    externals=[
        {'name': 'CDN', 'tag': 'External Service'},
    ],
    arrow_labels=['HTTPS', 'REST API', 'SQL', 'HTTPS'],
)

# ===== L2: default template data =====
L2 = make_c4_script(
    title='电商平台 · C4 容器图',
    subtitle='Container Diagram — 展示系统内部容器及其交互关系',
    persons=[
        {'id': 'customer', 'name': '顾客', 'desc': '浏览商品、下单购买'},
        {'id': 'admin', 'name': '管理员', 'desc': '管理商品、处理订单'},
    ],
    frontend_nodes=[
        {'name': 'Web商城', 'tech': 'React, Next.js', 'desc': 'PC/H5 购物页面'},
        {'name': '移动端App', 'tech': 'React Native', 'desc': 'iOS/Android 客户端'},
        {'name': '管理后台', 'tech': 'Vue 3, Vite', 'desc': '商品管理、订单管理'},
    ],
    backend_nodes=[
        {'name': 'API网关', 'tech': 'Kong', 'desc': '路由、限流、鉴权'},
        {'name': '用户服务', 'tech': 'Java, Spring Boot', 'desc': '注册登录、用户信息'},
        {'name': '商品服务', 'tech': 'Java, Spring Boot', 'desc': '商品CRUD、库存'},
        {'name': '订单服务', 'tech': 'Java, Spring Boot', 'desc': '订单创建、状态流转'},
        {'name': '支付服务', 'tech': 'Go, Gin', 'desc': '支付对接、退款处理'},
        {'name': '通知服务', 'tech': 'Node.js', 'desc': '短信、邮件、推送'},
    ],
    data_nodes=[
        {'name': 'MySQL', 'tech': 'MySQL 8.0', 'desc': '核心业务数据'},
        {'name': 'Redis', 'tech': 'Redis 7', 'desc': '会话缓存、热点数据'},
        {'name': 'RocketMQ', 'tech': 'RocketMQ 5', 'desc': '异步消息解耦'},
        {'name': 'Elasticsearch', 'tech': 'ES 8', 'desc': '商品全文搜索'},
    ],
    externals=[
        {'name': '第三方支付', 'tag': 'External System'},
        {'name': '物流系统', 'tag': 'External System'},
        {'name': '短信平台', 'tag': 'External System'},
    ],
)

# ===== L3: 3 persons, 4 frontend, 7 backend, 5 data, 4 externals =====
L3 = make_c4_script(
    title='在线教育平台 · C4 容器图',
    subtitle='Container Diagram — 展示在线教育系统的容器及交互关系',
    persons=[
        {'id': 'student', 'name': '学生', 'desc': '选课学习、提交作业'},
        {'id': 'teacher', 'name': '教师', 'desc': '发布课程、批改作业'},
        {'id': 'admin', 'name': '运营管理员', 'desc': '平台运营、数据分析'},
    ],
    frontend_nodes=[
        {'name': '学生Web端', 'tech': 'React, Next.js', 'desc': '课程学习、考试'},
        {'name': '学生App', 'tech': 'Flutter', 'desc': '移动端学习'},
        {'name': '教师工作台', 'tech': 'Vue 3, Vite', 'desc': '课程管理、成绩'},
        {'name': '运营后台', 'tech': 'React, Ant Design', 'desc': '运营分析、配置'},
    ],
    backend_nodes=[
        {'name': 'API网关', 'tech': 'Kong', 'desc': '路由分发、限流'},
        {'name': '用户服务', 'tech': 'Java, Spring Boot', 'desc': '注册登录、角色管理'},
        {'name': '课程服务', 'tech': 'Java, Spring Boot', 'desc': '课程CRUD、目录'},
        {'name': '学习服务', 'tech': 'Go, Gin', 'desc': '进度追踪、学习记录'},
        {'name': '考试服务', 'tech': 'Java, Spring Boot', 'desc': '出题组卷、自动阅卷'},
        {'name': '支付服务', 'tech': 'Go, Gin', 'desc': '课程购买、退款'},
        {'name': '通知服务', 'tech': 'Node.js', 'desc': '上课提醒、成绩通知'},
    ],
    data_nodes=[
        {'name': 'MySQL', 'tech': 'MySQL 8.0', 'desc': '用户与课程数据'},
        {'name': 'Redis', 'tech': 'Redis 7', 'desc': '缓存、排行榜'},
        {'name': 'MongoDB', 'tech': 'MongoDB 7', 'desc': '学习记录、日志'},
        {'name': 'MinIO', 'tech': 'MinIO', 'desc': '视频与课件存储'},
        {'name': 'Elasticsearch', 'tech': 'ES 8', 'desc': '课程搜索'},
    ],
    externals=[
        {'name': '第三方支付', 'tag': 'External System'},
        {'name': '直播CDN', 'tag': 'External Service'},
        {'name': '短信平台', 'tag': 'External Service'},
        {'name': 'AI批改引擎', 'tag': 'External System'},
    ],
    arrow_labels=['HTTPS', 'REST / gRPC', 'JDBC / TCP', 'HTTPS'],
)

# ===== L4: 3 persons, 5 frontend, 8 backend, 6 data, 5 externals =====
L4 = make_c4_script(
    title='金融交易平台 · C4 容器图',
    subtitle='Container Diagram — 展示金融交易系统全架构容器及交互',
    persons=[
        {'id': 'trader', 'name': '交易员', 'desc': '下单交易、查看行情'},
        {'id': 'risk', 'name': '风控人员', 'desc': '风险监控、审批'},
        {'id': 'admin', 'name': '系统管理员', 'desc': '系统配置、权限管理'},
    ],
    frontend_nodes=[
        {'name': '交易终端', 'tech': 'Electron, React', 'desc': '专业交易界面'},
        {'name': 'Web交易', 'tech': 'React, Next.js', 'desc': '网页版交易'},
        {'name': '移动交易', 'tech': 'React Native', 'desc': 'APP下单交易'},
        {'name': '风控大屏', 'tech': 'Vue 3, ECharts', 'desc': '实时风险监控'},
        {'name': '管理后台', 'tech': 'React, Ant Design', 'desc': '系统运维管理'},
    ],
    backend_nodes=[
        {'name': 'API网关', 'tech': 'Kong, Lua', 'desc': '路由、鉴权、限流'},
        {'name': '行情服务', 'tech': 'C++, Boost', 'desc': '实时行情推送'},
        {'name': '撮合引擎', 'tech': 'C++', 'desc': '订单撮合、成交'},
        {'name': '订单服务', 'tech': 'Java, Spring Boot', 'desc': '委托管理、状态'},
        {'name': '风控服务', 'tech': 'Go, Gin', 'desc': '实时风控、规则引擎'},
        {'name': '清算服务', 'tech': 'Java, Spring Boot', 'desc': '日终清算、对账'},
        {'name': '用户服务', 'tech': 'Java, Spring Boot', 'desc': '账户、KYC认证'},
        {'name': '通知服务', 'tech': 'Node.js', 'desc': '成交推送、风险告警'},
    ],
    data_nodes=[
        {'name': 'TiDB', 'tech': 'TiDB 7', 'desc': '核心交易数据'},
        {'name': 'Redis Cluster', 'tech': 'Redis 7', 'desc': '行情缓存、会话'},
        {'name': 'Kafka', 'tech': 'Kafka 3.6', 'desc': '交易事件流'},
        {'name': 'ClickHouse', 'tech': 'ClickHouse', 'desc': '交易分析、报表'},
        {'name': 'MongoDB', 'tech': 'MongoDB 7', 'desc': '操作日志、审计'},
        {'name': 'MinIO', 'tech': 'MinIO', 'desc': '对账文件、报告'},
    ],
    externals=[
        {'name': '交易所接口', 'tag': 'External System'},
        {'name': '银行系统', 'tag': 'External System'},
        {'name': '征信平台', 'tag': 'External System'},
        {'name': '监管报送', 'tag': 'External System'},
        {'name': '短信/邮件', 'tag': 'External Service'},
    ],
    arrow_labels=['WebSocket / HTTPS', 'REST / gRPC / FIX', 'JDBC / TCP', 'HTTPS / FIX'],
)

test_data = {'L1': L1, 'L2': L2, 'L3': L3, 'L4': L4}

for level, script in test_data.items():
    content = head + '\n' + script + '\n' + tail
    filename = f'c4-{level}.html'
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Generated {filename}')
