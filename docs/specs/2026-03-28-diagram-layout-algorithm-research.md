# 图表布局算法调研报告

> 针对 6 种核心图表类型，调研业界专业工具使用的布局算法，推荐可在 ~50 行 vanilla JS 内实现的最简有效方案。

---

## 1. 流程图 (Flowchart)

### 1.1 专业工具使用的算法

| 工具 | 算法 | 说明 |
|------|------|------|
| **Graphviz (dot)** | Sugiyama 分层算法 | 4 阶段：环消除 → 层分配 → 交叉最小化 → 坐标赋值 |
| **Mermaid** | dagre（Sugiyama 变体） | 基于 dagre 库，本质是简化版 Sugiyama |
| **D2** | dagre / ELK / TALA | 默认 dagre，复杂图可切 ELK（也是 Sugiyama 系） |
| **draw.io** | mxHierarchicalLayout | 基于 mxGraph 的分层布局，Sugiyama 系 |
| **PlantUML** | Graphviz dot | 直接调用 Graphviz 引擎 |
| **Lucidchart** | 私有实现 | 类似 Sugiyama + 自动路由 |

**结论**：所有主流工具都使用 **Sugiyama 分层算法**（或其变体）来布局流程图。

### 1.2 Sugiyama 算法核心 4 步

```
Step 1: 环消除 (Cycle Removal)
  → 反转部分边使图变为 DAG（流程图通常已是 DAG，循环边特殊处理）

Step 2: 层分配 (Layer Assignment)
  → 拓扑排序后，将节点分配到不同层级
  → 长边（跨多层）插入虚拟节点使每条边只跨一层

Step 3: 交叉最小化 (Crossing Minimization)
  → 逐层扫描，用重心法 (barycenter) 调整同层节点顺序
  → 重心 = 相邻层已排序邻居位置的平均值
  → 多轮扫描（上→下 + 下→上）直到稳定

Step 4: 坐标赋值 (Coordinate Assignment)
  → 在层内按排序结果均匀分配 x 坐标
  → y 坐标由层级决定
  → 虚拟节点连成直线（减少弯折）
```

### 1.3 复杂分支/合并/循环的处理

- **分支（decision）**：判断节点的 true/false 分支分配到不同子树，各子树独立布局后并排放置
- **合并点（merge）**：多条路径汇入同一节点时，该节点层级 = max(所有前驱层级) + 1
- **循环（loop）**：反转回边使之变为 DAG → 布局完成后恢复回边方向 → 回边绘制为曲线绕行

### 1.4 推荐实现：简化 Sugiyama（~60 行 JS）

```javascript
// 简化版 Sugiyama：拓扑分层 + 重心排序
function layoutFlowchart(nodes, edges, opts) {
  var gapX = opts.gapX || 60, gapY = opts.gapY || 80;

  // Step 1: 拓扑排序分层（BFS，Kahn's algorithm）
  var inDeg = {}, adj = {}, layers = {};
  nodes.forEach(function(n) { inDeg[n.id] = 0; adj[n.id] = []; });
  edges.forEach(function(e) { inDeg[e.to]++; adj[e.from].push(e.to); });

  var queue = [], layer = 0;
  nodes.forEach(function(n) { if (inDeg[n.id] === 0) queue.push(n.id); });

  while (queue.length) {
    var next = [];
    queue.forEach(function(id) { layers[id] = layer; });
    queue.forEach(function(id) {
      adj[id].forEach(function(to) {
        if (--inDeg[to] === 0) next.push(to);
      });
    });
    queue = next;
    layer++;
  }

  // Step 2: 按层分组
  var byLayer = {};
  nodes.forEach(function(n) {
    var l = layers[n.id];
    if (!byLayer[l]) byLayer[l] = [];
    byLayer[l].push(n);
  });

  // Step 3: 重心排序（2 轮扫描）
  for (var pass = 0; pass < 2; pass++) {
    for (var l = 1; l < layer; l++) {
      byLayer[l].forEach(function(n) {
        var preds = edges.filter(function(e) { return e.to === n.id; })
          .map(function(e) { return nodes.find(function(x) { return x.id === e.from; }); });
        if (preds.length) {
          n._bary = preds.reduce(function(s, p) { return s + (p._order || 0); }, 0) / preds.length;
        }
      });
      byLayer[l].sort(function(a, b) { return (a._bary || 0) - (b._bary || 0); });
      byLayer[l].forEach(function(n, i) { n._order = i; });
    }
  }

  // Step 4: 坐标赋值
  var maxLayerW = 0;
  for (var l = 0; l < layer; l++) {
    var arr = byLayer[l] || [];
    if (arr.length > maxLayerW) maxLayerW = arr.length;
  }
  for (var l = 0; l < layer; l++) {
    var arr = byLayer[l] || [];
    var totalW = arr.reduce(function(s, n) { return s + n.w; }, 0) + (arr.length - 1) * gapX;
    var startX = -totalW / 2;
    arr.forEach(function(n) {
      n.x = startX;
      n.y = l * (n.h + gapY);
      startX += n.w + gapX;
    });
  }
}
```

### 1.5 关键参数

| 参数 | 典型值 | 说明 |
|------|--------|------|
| `gapX` | 40-80px | 同层节点间水平间距 |
| `gapY` | 60-100px | 层间垂直间距 |
| `nodeMinW` | 120px | 节点最小宽度 |
| `nodeMinH` | 40px | 节点最小高度 |
| `baryPasses` | 2-4 轮 | 重心排序扫描轮数（2 轮通常够用） |
| `direction` | `'TB'` | 布局方向（TB=上下，LR=左右） |

### 1.6 流程图专属规则

- 开始/结束节点用圆角矩形（radius: height/2）
- 判断节点用菱形，高度 = 宽度 * 0.7
- 判断节点的 true 分支默认向下，false 分支向右
- 回边（循环）绘制为向左绕行的曲线
- 并行分支居中对齐于父节点

---

## 2. 时序图 (Sequence Diagram)

### 2.1 专业工具使用的算法

| 工具 | 算法 | 说明 |
|------|------|------|
| **PlantUML** | 自研时序渲染器 | 基于消息列表顺序逐行绘制 |
| **Mermaid** | 顺序堆叠 + 间距计算 | 参与者等距排列，消息从上到下堆叠 |
| **D2** | 专用时序布局 | 参与者按出场顺序排列 |
| **draw.io** | 手动布局为主 | 提供时序图模板 |

**结论**：时序图不使用通用图布局算法，而是**专用的顺序堆叠渲染器**——本质上是一个表格化布局：水平轴是参与者，垂直轴是时间。

### 2.2 布局算法核心

时序图布局不是"图论算法"，而是"表格+堆叠"算法：

```
1. 参与者间距计算：
   → 基础间距 = max(所有消息文字宽度 + padding)
   → 自调用消息额外占宽（activation bar 宽度 + 回调箭头宽度）

2. 消息垂直堆叠：
   → 每条消息占固定行高（messageHeight）
   → 片段（fragment）额外增加 header 高度 + padding
   → 嵌套片段：当前缩进深度 * indentWidth

3. 激活条（activation bar）：
   → 维护一个栈：activate 时 push，deactivate 时 pop
   → 栈深度决定 activation bar 的 x 偏移（每层 offset 3-5px）
   → bar 起点 = activate 消息的 y，终点 = deactivate 消息的 y

4. 片段（fragment）嵌套：
   → 维护嵌套栈，每进入一个 fragment push
   → fragment 矩形：x = 最左参与者 - margin，
     w = 最右参与者 + margin，y = 起始消息 y，h = 结束消息 y - 起始 y
```

### 2.3 推荐实现：顺序堆叠法（~45 行 JS）

```javascript
function layoutSequence(participants, messages, opts) {
  var msgH = opts.msgHeight || 40;         // 消息行高
  var partGap = opts.partGap || 200;       // 参与者间距
  var actW = opts.activationWidth || 12;   // 激活条宽度
  var actOffset = opts.activationOffset || 5; // 嵌套偏移

  // 1. 参与者 x 坐标
  participants.forEach(function(p, i) { p.x = i * partGap; });

  // 2. 根据消息文字宽度调整间距
  messages.forEach(function(m) {
    var fromIdx = participants.findIndex(function(p) { return p.id === m.from; });
    var toIdx = participants.findIndex(function(p) { return p.id === m.to; });
    if (fromIdx >= 0 && toIdx >= 0 && fromIdx !== toIdx) {
      var needed = measureText(m.label, 13) + 40;
      var span = Math.abs(toIdx - fromIdx);
      var perSlot = needed / span;
      // 扩展间距（如果文字太长）
      if (perSlot > partGap) partGap = perSlot;
    }
  });
  // 重算 x
  participants.forEach(function(p, i) { p.x = i * partGap; });

  // 3. 消息 y 坐标 + 激活栈
  var y = 80; // 标题区高度
  var actStack = {}; // { participantId: [{ startY, depth }] }
  participants.forEach(function(p) { actStack[p.id] = []; });

  messages.forEach(function(m) {
    m.y = y;
    // 激活条管理
    if (m.activate) {
      var stack = actStack[m.to];
      stack.push({ startY: y, depth: stack.length });
    }
    if (m.deactivate) {
      var stack = actStack[m.from];
      var act = stack.pop();
      if (act) { act.endY = y; m._activation = act; }
    }
    y += msgH;
  });

  // 4. 生命线高度
  participants.forEach(function(p) { p.lifelineH = y + 40; });

  return { width: (participants.length - 1) * partGap + 100, height: y + 80 };
}
```

### 2.4 关键参数

| 参数 | 典型值 | 说明 |
|------|--------|------|
| `participantGap` | 160-220px | 参与者间距（取决于最长消息文字） |
| `messageHeight` | 35-45px | 每条消息占用的垂直高度 |
| `activationWidth` | 10-14px | 激活条宽度 |
| `activationOffset` | 3-5px | 嵌套激活条的 x 偏移 |
| `fragmentPadding` | 10-16px | 片段框内边距 |
| `headerHeight` | 24-30px | 片段头部标签高度 |
| `selfCallWidth` | 30-40px | 自调用消息的回弯宽度 |

### 2.5 时序图专属规则

- 参与者框固定在顶部，生命线（虚线）垂直向下延伸
- 同步消息用实线实心箭头，异步用实线开放箭头，返回用虚线
- 自调用消息：从生命线右侧伸出一个"回"字形，占 selfCallWidth 宽度
- 激活条嵌套时向右偏移 actOffset px，形成阶梯效果
- 片段（loop/alt/opt）绘制为虚线矩形，标签在左上角
- alt 片段内部用虚线分隔 [then] 和 [else] 区域
- 消息文字居中放置在箭头上方

---

## 3. 类图 (Class Diagram - UML)

### 3.1 专业工具使用的算法

| 工具 | 算法 | 说明 |
|------|------|------|
| **Graphviz (dot)** | Sugiyama 分层 | 继承关系决定层级，父类在上子类在下 |
| **PlantUML** | Graphviz dot | 继承边驱动的分层布局 |
| **D2** | dagre/ELK | 分层布局，容器用于 package 分组 |
| **draw.io** | mxHierarchicalLayout | 支持 package 容器的分层布局 |
| **Lucidchart** | 私有分层布局 | 继承树 + 关联关系布局 |
| **学术研究** | 正交布局 (orthogonal) | 最小化交叉 + 弯折 + 继承树方向一致 |

**结论**：类图使用**继承驱动的分层布局**——继承关系决定垂直层级（父上子下），关联/依赖关系尽量水平布局。学术界推崇正交布局风格（所有线段水平或垂直），但实现复杂度高。

### 3.2 布局策略

类图的核心挑战是**混合关系**：继承（决定层级）+ 关联/依赖（不决定层级，但影响邻近性）。

```
1. 继承树提取：
   → 找出所有继承 (extends/implements) 关系
   → 构建继承森林（可能有多棵树）
   → 每棵树独立做层分配

2. 层分配（继承驱动）：
   → 根类/接口 = layer 0
   → 直接子类 = layer 1
   → 同层的兄弟类水平排列

3. 关联关系处理：
   → 同层类尽量相邻放置（如果有关联关系）
   → 不同层的关联关系用折线连接

4. Package 分组：
   → 同 package 的类尽量聚拢
   → package 绘制为外框矩形
   → 层分配时 package 内部先布局，再整体参与外层布局
```

### 3.3 推荐实现：继承树分层 + 网格对齐（~50 行 JS）

```javascript
function layoutClassDiagram(classes, relations, opts) {
  var gapX = opts.gapX || 40, gapY = opts.gapY || 60;

  // 1. 提取继承关系建树
  var parent = {}, children = {};
  classes.forEach(function(c) { children[c.id] = []; });
  relations.forEach(function(r) {
    if (r.type === 'extends' || r.type === 'implements') {
      parent[r.from] = r.to;
      children[r.to].push(r.from);
    }
  });

  // 2. 找根节点（无父类的类）
  var roots = classes.filter(function(c) { return !parent[c.id]; });

  // 3. BFS 分层
  var layer = {};
  var queue = roots.map(function(c) { return c.id; });
  roots.forEach(function(c) { layer[c.id] = 0; });
  while (queue.length) {
    var next = [];
    queue.forEach(function(id) {
      (children[id] || []).forEach(function(cid) {
        layer[cid] = layer[id] + 1;
        next.push(cid);
      });
    });
    queue = next;
  }

  // 4. 无继承关系的独立类放最底层
  var maxLayer = 0;
  classes.forEach(function(c) {
    if (layer[c.id] === undefined) layer[c.id] = -1; // 标记
    if (layer[c.id] > maxLayer) maxLayer = layer[c.id];
  });
  classes.forEach(function(c) {
    if (layer[c.id] === -1) layer[c.id] = maxLayer + 1;
  });

  // 5. 按层分组 + 坐标赋值
  var byLayer = {};
  classes.forEach(function(c) {
    var l = layer[c.id];
    if (!byLayer[l]) byLayer[l] = [];
    byLayer[l].push(c);
  });

  Object.keys(byLayer).forEach(function(l) {
    var arr = byLayer[l];
    var totalW = arr.reduce(function(s, c) { return s + c.w; }, 0) + (arr.length - 1) * gapX;
    var startX = -totalW / 2;
    arr.forEach(function(c) {
      c.x = startX;
      c.y = Number(l) * (100 + gapY); // 类框高度约 100px
      startX += c.w + gapX;
    });
  });
}
```

### 3.4 关键参数

| 参数 | 典型值 | 说明 |
|------|--------|------|
| `gapX` | 30-50px | 同层类间水平间距 |
| `gapY` | 50-80px | 层间垂直间距 |
| `classMinW` | 160px | 类框最小宽度 |
| `memberRowH` | 22px | 每个成员（属性/方法）的行高 |
| `sectionPadding` | 8px | 类框内分区间距 |
| `packagePadding` | 20px | Package 外框内边距 |

### 3.5 类图专属规则

- 类框三段式：类名区 + 属性区 + 方法区，用水平线分隔
- 继承箭头：空心三角 + 实线，父类在正上方
- 实现箭头：空心三角 + 虚线
- 关联箭头：实心三角或无头 + 实线
- 依赖箭头：开放箭头 + 虚线
- 接口/抽象类名用斜体（或加 `<<interface>>` 标注）
- 兄弟子类水平排列，继承箭头汇聚到父类底部中心

---

## 4. 架构图 (Architecture Diagram - Layered)

### 4.1 专业工具使用的算法

| 工具 | 算法 | 说明 |
|------|------|------|
| **D2 (TALA)** | 专用架构布局 | Terrastruct 针对软件架构图设计的引擎 |
| **D2 (ELK)** | 分层 + 嵌套容器 | 支持 port 精确定位和复杂嵌套 |
| **draw.io** | mxStackLayout / mxPartitionLayout | 层内水平排列，层间垂直堆叠 |
| **Lucidchart** | 手动 + 对齐辅助 | 无专用自动布局，依赖网格对齐 |
| **PlantUML (C4)** | Graphviz dot + 容器嵌套 | 分层布局 |

**结论**：架构图没有一个"标准算法"。大多数工具使用**容器嵌套 + 分层堆叠**的方式：每一层是一个水平容器，层内组件均匀分布，层间垂直堆叠。本质上是**约束化的分层布局**，比通用 Sugiyama 简单得多。

### 4.2 布局策略

架构图的特殊性在于**层是预定义的**（用户指定哪些组件属于哪一层），不需要算法自动分层。

```
1. 层定义：
   → 用户提供层信息：[{name: "前端", nodes: [...]}, {name: "后端", nodes: [...]}, ...]
   → 层顺序 = 数组顺序（从上到下）

2. 层内布局：
   → 每层内的组件水平均匀分布
   → 组件宽度自适应内容
   → 层宽 = max(所有层宽) → 保持对齐

3. 层间连接：
   → 跨层连线垂直为主，必要时加折线
   → 同层连线水平绘制

4. 嵌套容器：
   → 层内可以有子容器（如"微服务集群"内含多个服务）
   → 子容器先内部布局，再作为整体参与层布局
```

### 4.3 推荐实现：层堆叠布局（~35 行 JS）

```javascript
function layoutArchitecture(layers, opts) {
  var gapX = opts.gapX || 30, gapY = opts.gapY || 50;
  var layerPadX = opts.layerPadX || 24, layerPadY = opts.layerPadY || 16;
  var y = 0, maxW = 0;

  // 第一遍：计算每层尺寸
  layers.forEach(function(layer) {
    var totalNodeW = layer.nodes.reduce(function(s, n) { return s + n.w; }, 0);
    layer._contentW = totalNodeW + (layer.nodes.length - 1) * gapX;
    layer._contentH = Math.max.apply(null, layer.nodes.map(function(n) { return n.h; }));
    layer._w = layer._contentW + layerPadX * 2;
    layer._h = layer._contentH + layerPadY * 2 + 28; // 28 = 层标题高度
    if (layer._w > maxW) maxW = layer._w;
  });

  // 统一宽度
  maxW = Math.max(maxW, opts.minWidth || 800);

  // 第二遍：赋坐标
  layers.forEach(function(layer) {
    layer.x = 0;
    layer.y = y;
    layer.w = maxW;
    layer.h = layer._h;

    // 层内节点居中分布
    var startX = (maxW - layer._contentW) / 2;
    var nodeY = y + 28 + layerPadY;
    layer.nodes.forEach(function(n) {
      n.x = startX;
      n.y = nodeY + (layer._contentH - n.h) / 2; // 垂直居中
      startX += n.w + gapX;
    });

    y += layer.h + gapY;
  });

  return { width: maxW, height: y - gapY };
}
```

### 4.4 关键参数

| 参数 | 典型值 | 说明 |
|------|--------|------|
| `gapX` | 20-40px | 层内组件间距 |
| `gapY` | 40-60px | 层间间距 |
| `layerPadX` | 20-30px | 层框内水平边距 |
| `layerPadY` | 12-20px | 层框内垂直边距 |
| `layerTitleH` | 24-32px | 层标题区高度 |
| `nodeMinW` | 100px | 组件最小宽度 |
| `nodeMinH` | 50px | 组件最小高度 |
| `minWidth` | 800-1000px | 画布最小宽度 |

### 4.5 架构图专属规则

- 层背景用浅色区分（每层不同浅色），层标题在左上角或顶部居中
- 层框用圆角矩形，层间有明确视觉分隔
- 跨层连接用垂直箭头，标注协议/接口名称
- 外部系统/用户放在最顶层或最底层之外，用虚线边框区分
- 数据库/存储组件用圆柱体形状
- 支持组件内嵌子组件（嵌套容器）

---

## 5. 泳道图 (Swimlane Diagram)

### 5.1 专业工具使用的算法

| 工具 | 算法 | 说明 |
|------|------|------|
| **draw.io** | mxSwimlaneLayout | 分层布局约束在泳道容器内 |
| **Lucidchart** | 磁性泳道 + 手动布局 | 泳道内形状自动吸附，移动泳道时内部形状跟随 |
| **Mermaid** | 不原生支持 | 无泳道专用布局 |
| **PlantUML** | 分区（partition） | 活动图 + partition 实现泳道效果 |
| **D2** | 容器嵌套 | 用 container 模拟泳道 |

**结论**：泳道图 = **约束化的流程图布局**。核心区别是节点有"泳道归属"约束——每个节点只能出现在指定泳道内，水平位置由泳道决定，垂直位置由流程顺序决定。

### 5.2 布局策略

```
1. 泳道宽度计算：
   → 每个泳道宽度 = max(该泳道内所有节点宽度) + 2 * padding
   → 所有泳道宽度统一为最大值（或按内容自适应）

2. 流程顺序分层：
   → 与流程图相同的拓扑分层算法
   → 但 x 坐标不由层内排序决定，而由泳道归属决定

3. 跨泳道连线路由：
   → 同泳道内：垂直直线连接
   → 跨泳道：水平 + 垂直折线
   → 路由策略：从源节点底部出发 → 垂直到中间行 → 水平到目标泳道 → 垂直到目标节点顶部

4. 判断分支：
   → 判断节点在当前泳道内
   → 分支路径可进入不同泳道
   → true/false 标注在连线上
```

### 5.3 推荐实现：泳道约束布局（~50 行 JS）

```javascript
function layoutSwimlane(lanes, nodes, edges, opts) {
  var laneW = opts.laneWidth || 220;
  var gapY = opts.gapY || 60;
  var headerH = opts.headerHeight || 50;

  // 1. 泳道 x 坐标
  lanes.forEach(function(lane, i) { lane.x = i * laneW; });

  // 2. 拓扑排序分层（同流程图）
  var inDeg = {}, adj = {}, layer = {};
  nodes.forEach(function(n) { inDeg[n.id] = 0; adj[n.id] = []; });
  edges.forEach(function(e) { inDeg[e.to]++; adj[e.from].push(e.to); });

  var queue = [];
  nodes.forEach(function(n) { if (inDeg[n.id] === 0) queue.push(n.id); });
  var currentLayer = 0;
  while (queue.length) {
    var next = [];
    queue.forEach(function(id) { layer[id] = currentLayer; });
    queue.forEach(function(id) {
      adj[id].forEach(function(to) {
        if (--inDeg[to] === 0) next.push(to);
      });
    });
    queue = next;
    currentLayer++;
  }

  // 3. 坐标赋值（x 由泳道决定，y 由层决定）
  var maxLaneH = 0;
  nodes.forEach(function(n) {
    var laneIdx = lanes.findIndex(function(l) { return l.id === n.lane; });
    n.x = lanes[laneIdx].x + (laneW - n.w) / 2; // 泳道内居中
    n.y = headerH + layer[n.id] * (n.h + gapY);
    var bottom = n.y + n.h + gapY;
    if (bottom > maxLaneH) maxLaneH = bottom;
  });

  // 4. 泳道高度统一
  lanes.forEach(function(lane) {
    lane.w = laneW;
    lane.h = maxLaneH + 20;
  });

  return { width: lanes.length * laneW, height: maxLaneH + headerH + 20 };
}
```

### 5.4 关键参数

| 参数 | 典型值 | 说明 |
|------|--------|------|
| `laneWidth` | 180-260px | 泳道宽度 |
| `laneHeaderH` | 40-56px | 泳道头部（角色名）高度 |
| `gapY` | 50-70px | 行间垂直间距 |
| `lanePadding` | 16-24px | 泳道内边距 |
| `crossLaneGap` | 8-12px | 跨泳道折线转角间距 |

### 5.5 泳道图专属规则

- 泳道头部（第一行）显示角色/部门名称，用背景色区分
- 泳道间用竖线分隔，泳道宽度可等宽或自适应
- 同一行（同层）的节点表示并行或同时发生的步骤
- 跨泳道箭头必须从源节点中心出发，水平穿越到目标泳道
- 判断菱形的 true/false 分支可以进入不同泳道
- 泳道高度统一（取最高泳道的高度）

---

## 6. 状态图 (State Diagram)

### 6.1 专业工具使用的算法

| 工具 | 算法 | 说明 |
|------|------|------|
| **Graphviz (dot)** | Sugiyama 分层 | 状态图当作有向图处理 |
| **Graphviz (fdp/neato)** | 力导向 (Fruchterman-Reingold / Kamada-Kawai) | 适合无明确层级的状态图 |
| **PlantUML** | Graphviz dot | 分层布局 |
| **Mermaid** | dagre | 分层布局 |
| **D2** | dagre/ELK | 分层布局 |
| **draw.io** | mxHierarchicalLayout / mxFastOrganicLayout | 分层或力导向可选 |

**结论**：状态图有两种有效方法——

1. **分层布局（Sugiyama）**：适合有明确流向的状态机（初始→中间→终态），大多数工具默认使用
2. **力导向布局（Fruchterman-Reingold）**：适合复杂状态机（大量自循环、双向转换、无明确层级）

**推荐**：优先使用**简化 Sugiyama**（与流程图共用），自循环和双向边做特殊处理。原因：状态图通常有初始状态和终态，天然有方向性；力导向虽然灵活但结果不稳定（每次运行可能不同），不适合"模板生成"的场景。

### 6.2 Fruchterman-Reingold 力导向算法（备选）

```
核心思路：模拟物理系统
- 所有节点对之间有斥力（库仑力），防止重叠
- 有边相连的节点间有引力（弹簧力），拉近相关节点
- 迭代计算，每次移动节点，逐步降温直到稳定

公式：
- 斥力：f_r = k^2 / d    （d = 两节点距离，k = 理想距离）
- 引力：f_a = d^2 / k
- 理想距离：k = C * sqrt(W * H / |V|)   （C 通常 = 1.0）
- 温度：每轮降低，限制最大位移

参数：
- iterations: 50-100（50 轮通常收敛）
- C: 0.5-2.0（理想距离系数）
- cooling: 0.95（每轮温度衰减比例）
```

### 6.3 推荐实现：Sugiyama + 状态图特化（~55 行 JS）

复用流程图的 Sugiyama 布局，加上状态图专属处理：

```javascript
function layoutStateDiagram(states, transitions, opts) {
  var gapX = opts.gapX || 50, gapY = opts.gapY || 70;

  // 1. 分离特殊转换：自循环、双向
  var selfLoops = [], biDir = [], normal = [];
  transitions.forEach(function(t) {
    if (t.from === t.to) { selfLoops.push(t); }
    else {
      var reverse = transitions.find(function(r) {
        return r.from === t.to && r.to === t.from && r !== t;
      });
      if (reverse && t.from < t.to) { biDir.push({ a: t, b: reverse }); }
      else if (!reverse) { normal.push(t); }
    }
  });

  // 2. 用 normal edges 做拓扑分层（同流程图 Sugiyama）
  // 初始状态 = layer 0（入度为 0 或标记为 initial）
  var inDeg = {}, adj = {}, layer = {};
  states.forEach(function(s) { inDeg[s.id] = 0; adj[s.id] = []; });
  normal.forEach(function(t) { inDeg[t.to]++; adj[t.from].push(t.to); });

  var queue = [];
  states.forEach(function(s) {
    if (s.type === 'initial' || inDeg[s.id] === 0) queue.push(s.id);
  });
  var currentLayer = 0;
  while (queue.length) {
    var next = [];
    queue.forEach(function(id) { layer[id] = currentLayer; });
    queue.forEach(function(id) {
      adj[id].forEach(function(to) {
        if (layer[to] === undefined && --inDeg[to] === 0) next.push(to);
      });
    });
    queue = next;
    currentLayer++;
  }
  // 未分配的放最后一层
  states.forEach(function(s) {
    if (layer[s.id] === undefined) layer[s.id] = currentLayer;
  });

  // 3. 坐标赋值（同流程图）
  var byLayer = {};
  states.forEach(function(s) {
    var l = layer[s.id];
    if (!byLayer[l]) byLayer[l] = [];
    byLayer[l].push(s);
  });

  Object.keys(byLayer).forEach(function(l) {
    var arr = byLayer[l];
    var totalW = arr.reduce(function(s, n) { return s + n.w; }, 0) + (arr.length - 1) * gapX;
    var startX = -totalW / 2;
    arr.forEach(function(s) {
      s.x = startX;
      s.y = Number(l) * (s.h + gapY);
      startX += s.w + gapX;
    });
  });

  // 4. 自循环绘制为节点右侧弧线
  selfLoops.forEach(function(t) {
    var s = states.find(function(s) { return s.id === t.from; });
    t._selfLoopX = s.x + s.w + 15; // 弧线 x 偏移
  });

  // 5. 双向边绘制为平行偏移线
  biDir.forEach(function(pair) {
    pair.a._offset = -6;  // 向左偏移
    pair.b._offset = 6;   // 向右偏移
  });
}
```

### 6.4 关键参数

| 参数 | 典型值 | 说明 |
|------|--------|------|
| `gapX` | 40-60px | 同层状态间距 |
| `gapY` | 60-80px | 层间间距 |
| `stateMinW` | 100px | 状态节点最小宽度 |
| `stateMinH` | 40px | 状态节点最小高度 |
| `stateRadius` | 8-12px | 状态圆角半径 |
| `selfLoopR` | 20-25px | 自循环弧线半径 |
| `biDirOffset` | 5-8px | 双向边的平行偏移量 |
| `initialR` | 8px | 初始状态实心圆半径 |
| `finalR` | 10px (外) + 6px (内) | 终态双圆半径 |

### 6.5 状态图专属规则

- 初始状态：实心黑圆（小圆点），无入边
- 终态：双圆环（外圆 + 内实心圆），无出边
- 自循环：绘制为节点右侧或上方的弧线箭头，标注触发事件
- 双向转换：两条平行偏移线，各带独立箭头和标注
- 复合状态（嵌套）：外框矩形内包含子状态机，用圆角矩形 + 标题栏
- 转换标注格式：`event [guard] / action`
- 并行状态用虚线分隔区域

---

## 总结对比

| 图表类型 | 推荐算法 | 核心思路 | JS 代码量 | 复杂度 |
|---------|---------|---------|----------|--------|
| **流程图** | 简化 Sugiyama | 拓扑分层 + 重心排序 | ~60 行 | 中 |
| **时序图** | 顺序堆叠法 | 水平等距 + 垂直堆叠 + 激活栈 | ~45 行 | 低 |
| **类图** | 继承树分层 | 继承关系驱动层分配 | ~50 行 | 中 |
| **架构图** | 层堆叠布局 | 预定义层 + 层内均匀分布 | ~35 行 | 低 |
| **泳道图** | 泳道约束流程图 | 拓扑分层 + 泳道 x 约束 | ~50 行 | 中 |
| **状态图** | Sugiyama + 状态特化 | 分层 + 自循环/双向边处理 | ~55 行 | 中 |

### 算法复用关系

```
简化 Sugiyama（拓扑分层 + 重心排序）
  ├── 流程图：直接使用
  ├── 类图：继承关系做层分配，复用坐标赋值
  ├── 泳道图：复用分层，x 坐标改为泳道约束
  └── 状态图：复用分层，增加自循环/双向边处理

层堆叠（预定义层 + 均匀分布）
  └── 架构图：直接使用

顺序堆叠（水平等距 + 垂直堆叠）
  └── 时序图：直接使用
```

核心算法只需 3 个：
1. **简化 Sugiyama**（拓扑分层 + 重心排序）— 覆盖 4 种图表
2. **层堆叠** — 覆盖架构图
3. **顺序堆叠** — 覆盖时序图

---

## 参考来源

- [Layered graph drawing - Wikipedia](https://en.wikipedia.org/wiki/Layered_graph_drawing)
- [The Sugiyama Method - Layered Graph Drawing (Disy Blog)](https://blog.disy.net/sugiyama-method/)
- [Drawing graphs with dot (Graphviz)](https://graphviz.org/pdf/dotguide.pdf)
- [Layout Engines | Graphviz](https://graphviz.org/docs/layouts/)
- [D2 Layout Documentation](https://d2lang.com/tour/layouts/)
- [Plugin-Based Layout Engines | D2 DeepWiki](https://deepwiki.com/terrastruct/d2/3.2-plugin-based-layout-engines)
- [Force-directed graph drawing - Wikipedia](https://en.wikipedia.org/wiki/Force-directed_graph_drawing)
- [Fruchterman-Reingold original paper](https://reingold.co/force-directed.pdf)
- [Graphology FR Layout](https://github.com/ambalytics/graphology-layout-fruchtermanreingold)
- [Automatic Layout of UML Class Diagrams in Orthogonal Style](https://www.researchgate.net/publication/220586569_Automatic_Layout_of_UML_Class_Diagrams_in_Orthogonal_Style)
- [PlantUML Layout Guide](https://crashedmind.github.io/PlantUMLHitchhikersGuide/layout/layout.html)
- [draw.io Automatic Layout](https://www.drawio.com/doc/faq/apply-layouts)
- [mxSwimlaneLayout API](https://jgraph.github.io/mxgraph/docs/js-api/files/layout/hierarchical/mxSwimlaneLayout-js.html)
- [mxHierarchicalLayout API](https://jgraph.github.io/mxgraph/docs/js-api/files/layout/hierarchical/mxHierarchicalLayout-js.html)
- [Coffman-Graham algorithm - Wikipedia](https://en.wikipedia.org/wiki/Coffman%E2%80%93Graham_algorithm)
- [Hierarchical Drawing Algorithms (Brown University)](https://cs.brown.edu/people/rtamassi/gdhandbook/chapters/hierarchical.pdf)
- [Barycenter Heuristic (OGDF)](https://ogdf.github.io/doc/ogdf/classogdf_1_1_barycenter_heuristic.html)
- [Sequence diagrams | Mermaid](https://mermaid.js.org/syntax/sequenceDiagram.html)
- [PlantUML Sequence Diagram](https://plantuml.com/sequence-diagram)
- [Layered Graph Layout (yWorks)](https://www.yworks.com/pages/layered-graph-layout)
