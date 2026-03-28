# 画图 Skill 动态布局引擎方案设计

## 背景与动机

### 为什么要做

第一阶段完成了 26 种图表的 HTML/SVG 模板和统一设计规范。但当前有 11 个模板使用硬编码坐标，无法适应不同数据量的真实场景——节点数量变化、文字长度不同、分支结构变化都可能导致重叠、截断、布局混乱。

### 提出方

画图 Skill 自身迭代需求。第一阶段 review 过程中反复出现的重叠/截断问题证明了静态模板的局限性。

### 约束条件

- 保持纯 HTML+CSS+SVG + 内联 JS 的技术栈，不引入外部依赖
- 保持现有设计规范（配色、字体、间距、组件样式）不变
- 生成的图表质量不低于当前手调的模板效果
- 支持 Playwright fullPage 截图输出 PNG

---

## 现状分析

### 当前状态

| 类型 | 数量 | 布局方式 | 问题 |
|------|------|---------|------|
| 动态布局 | 15 个 | JS 计算坐标 | 基本可用，部分需优化 |
| 静态硬编码 | 11 个 | SVG 坐标写死 | 数据变化即破 |

### 已有动态模板（可复用经验）

mindmap（双侧树形）、pie（弧形+防碰撞）、radar（极坐标）、bar/line/scatter（笛卡尔）、heatmap（网格）、sankey（流带）、timeline（纵向列表）、gantt（日期轴）、c4（分层容器）、decision-tree（树形）、dataflow（左右流）、network（分层+侧边栏）、orgchart（树形+侧边树线）

### 需要改造的静态模板

flowchart、sequence、er、class、architecture、swimlane、state、fishbone、swot、venn、journey

### 不改会怎样

每次用户数据不同就需要手动调坐标，失去了"自动生成"的核心价值。skill 无法在真实项目中可靠使用。

---

## 调研与备选方案

### 方案 A：每个模板内置独立布局引擎

- **调研内容**：参考现有 15 个动态模板的实现方式，每个模板 JS 代码中包含完整的布局逻辑
- **验证方式**：已有 15 个模板证明可行
- **验证结果**：可用，但模板间大量重复代码（文字宽度计算、节点创建、碰撞检测每个都写一遍）
- **结论**：可行但维护成本高

### 方案 B：抽取公共布局工具库 + 各模板专用布局

- **调研内容**：将通用功能（文字测量、节点绘制、连线路由、碰撞检测）抽取为公共模块，各模板只写布局算法
- **验证方式**：分析现有 15 个动态模板的公共代码
- **验证结果**：至少 6 个函数可公共化：`measureText()`、`createNode()`、`drawLine()`、`detectOverlap()`、`routeLine()`、`autoResize()`
- **结论**：最佳方案，复用+专用结合

### 方案 C：统一布局引擎（大一统）

- **调研内容**：做一个通用的图布局引擎，所有图表类型都走同一套算法
- **验证方式**：分析 26 种图表的布局需求差异
- **验证结果**：差异太大——树形 vs 网格 vs 径向 vs 笛卡尔 vs 自由布局，强行统一会过度抽象
- **结论**：不可行，过度设计

---

## 决策与取舍

**采用方案 B**：公共工具库 + 各模板专用布局。

### 核心理由

1. 公共库消除重复代码，新增图表类型时只需写布局算法
2. 专用布局保证每种图表的质量（不用"万能算法"妥协效果）
3. 已有 15 个动态模板验证了"JS 内联布局"的可行性

### 取舍说明

- 放弃方案 C 的"一套代码画所有图"的优雅性，换取每种图表的最佳效果
- 公共库通过 `<script>` 标签内联（不是外部文件），保持零依赖

### 遗留风险

- 公共库代码会在每个 HTML 模板中重复嵌入（因为要零依赖）
- 解法：生成时由 Claude 负责嵌入最新版本的公共代码

---

## 技术方案

### 整体架构

```
用户需求
  ↓
Claude 分析 → 选择图表类型 → 读取专属规范
  ↓
根据数据调用布局算法 → 计算节点坐标 → 生成 SVG
  ↓
运行验证检查 → 发现问题自动修正
  ↓
Playwright 截图 → PNG 输出
```

### 一、公共工具库（diagram-utils）

不是独立文件，而是一组**标准函数**，生成图表时内联到 HTML 中。

#### 1.1 文字测量

```javascript
// 估算文字渲染宽度（中英文混排）
function measureText(str, fontSize) {
  var w = 0;
  for (var i = 0; i < str.length; i++) {
    w += str.charCodeAt(i) > 127 ? fontSize : fontSize * 0.6;
  }
  return w;
}
```

#### 1.2 节点尺寸计算

```javascript
// 根据文字内容计算节点宽高
function calcNodeSize(label, opts) {
  var padX = opts.padX || 16;
  var padY = opts.padY || 10;
  var fontSize = opts.fontSize || 13;
  var w = measureText(label, fontSize) + padX * 2;
  var h = fontSize + padY * 2;
  return { w: Math.max(w, opts.minW || 80), h: Math.max(h, opts.minH || 32) };
}
```

#### 1.3 碰撞检测

```javascript
// 检测两个矩形是否重叠
function isOverlap(a, b, gap) {
  gap = gap || 0;
  return !(a.x + a.w + gap <= b.x || b.x + b.w + gap <= a.x ||
           a.y + a.h + gap <= b.y || b.y + b.h + gap <= a.y);
}

// 检测节点数组中的所有重叠
function findOverlaps(nodes, minGap) {
  var overlaps = [];
  for (var i = 0; i < nodes.length; i++) {
    for (var j = i + 1; j < nodes.length; j++) {
      if (isOverlap(nodes[i], nodes[j], minGap)) {
        overlaps.push([i, j]);
      }
    }
  }
  return overlaps;
}
```

#### 1.4 连线路由

```javascript
// 简单直线连接（从 source 边缘到 target 边缘）
function connectNodes(src, tgt, direction) {
  // direction: 'tb'(上下), 'lr'(左右)
  if (direction === 'tb') {
    return { x1: src.x + src.w/2, y1: src.y + src.h, x2: tgt.x + tgt.w/2, y2: tgt.y };
  } else {
    return { x1: src.x + src.w, y1: src.y + src.h/2, x2: tgt.x, y2: tgt.y + tgt.h/2 };
  }
}
```

#### 1.5 画布自适应

```javascript
// 根据所有节点计算最小画布尺寸
function calcCanvasSize(nodes, padding) {
  var pad = padding || 24;
  var minX = Infinity, minY = Infinity, maxX = 0, maxY = 0;
  nodes.forEach(function(n) {
    if (n.x < minX) minX = n.x;
    if (n.y < minY) minY = n.y;
    if (n.x + n.w > maxX) maxX = n.x + n.w;
    if (n.y + n.h > maxY) maxY = n.y + n.h;
  });
  return { w: maxX - minX + pad * 2, h: maxY - minY + pad * 2, offsetX: -minX + pad, offsetY: -minY + pad };
}
```

### 二、布局算法分类

| 算法 | 适用图表 | 核心思路 |
|------|---------|--------|
| **树形布局** | flowchart, decision-tree, orgchart | 递归算子树宽度 → 自顶向下分配 x/y |
| **分层布局** | C4, architecture, network, dataflow | 按层分组 → 层内均匀分布 → 层间连线 |
| **网格布局** | gantt, heatmap, class, er | 行列对齐 → 单元格内内容居中 |
| **笛卡尔坐标** | bar, line, scatter | 数据映射到坐标轴 → 绘制数据元素 |
| **径向布局** | pie, radar | 角度+半径 → 极坐标转换 |
| **双侧树形** | mindmap | 左右分流 → 各侧独立树形 |
| **泳道布局** | swimlane | 角色分行 → 流程横向推进 |
| **时序布局** | sequence | 参与者等距排列 → 消息纵向堆叠 |
| **卡片布局** | swot, venn, journey, fishbone | 固定结构骨架 → 内容动态填充 |
| **流布局** | sankey | 节点分层 → 流带宽度按值比例 |
| **通用兜底** | 未知类型 | 网格排列 + 自动连线 |

### 三、专用布局与通用兜底的关系

```
收到画图需求
  ↓
匹配已知 26 种类型？
  ├─ 是 → 使用专用布局算法 + 专属规范
  └─ 否 → 使用通用兜底算法
            ├─ 有层级关系 → 树形布局
            ├─ 有流向关系 → 分层布局
            ├─ 有网格关系 → 网格布局
            └─ 其他 → 力导向自由布局
```

通用兜底的核心是**自动识别数据结构**，选择最合适的布局策略。不追求完美，但保证可用。

### 四、验证检查机制

每次生成图表后，运行以下检查：

```javascript
function validateDiagram(nodes, lines, canvas) {
  var issues = [];

  // 1. 节点重叠
  var overlaps = findOverlaps(nodes, 8);
  if (overlaps.length > 0) issues.push({ type: 'overlap', pairs: overlaps });

  // 2. 内容超出画布
  nodes.forEach(function(n) {
    if (n.x < 0 || n.y < 0 || n.x + n.w > canvas.w || n.y + n.h > canvas.h) {
      issues.push({ type: 'out_of_bounds', node: n });
    }
  });

  // 3. 连线穿越节点
  lines.forEach(function(l) {
    nodes.forEach(function(n) {
      if (lineIntersectsRect(l, n) && n !== l.src && n !== l.tgt) {
        issues.push({ type: 'line_cross', line: l, node: n });
      }
    });
  });

  // 4. 最小间距
  nodes.forEach(function(a) {
    nodes.forEach(function(b) {
      if (a !== b && distance(a, b) < 20) {
        issues.push({ type: 'too_close', nodes: [a, b] });
      }
    });
  });

  return issues;
}
```

验证不通过时，自动修正策略：
- **重叠** → 推开节点（增大间距重新布局）
- **超出画布** → 扩大画布或缩小间距
- **连线穿越** → 改用折线绕行
- **间距不足** → 整体缩放间距系数

### 五、生成流程

```
1. Claude 读取专属规范（references/diagrams/<type>.md）
2. 根据用户数据构造数据结构（nodes + edges）
3. 内联公共工具函数
4. 调用专用布局算法计算坐标
5. 按设计规范渲染 SVG（先连线层，后节点层）
6. 运行 validateDiagram() 检查
7. 有问题则自动修正，重新渲染
8. calcCanvasSize() 自适应画布
9. Playwright 截图输出 PNG
```

### 六、改造优先级

| 批次 | 模板 | 算法 | 理由 |
|------|------|------|------|
| P0 | flowchart, sequence, er | 树形 / 时序 / 网格 | 最高频，当前硬编码最痛 |
| P1 | class, architecture, swimlane | 网格 / 分层 / 泳道 | 常用，数据变化大 |
| P2 | state, fishbone, swot, venn, journey | 树形 / 卡片 | 结构较固定 |

### 七、配色方案扩展性

当前只有一套配色（design-system.md 中定义）。后续需要支持多套配色方案，适配不同场景（如：科技蓝、商务灰、活力橙、暗黑模式等）。

**架构设计**：布局算法与配色方案解耦。

```javascript
// 配色方案定义为独立对象
var themes = {
  default: {
    // 结构图
    node: { bg: '#EFF6FF', border: '#93C5FD', text: '#1E293B' },
    highlight: { bg: '#3B82F6', border: '#3B82F6', text: '#FFFFFF' },
    decision: { bg: '#FFFBEB', border: '#FCD34D', text: '#92400E' },
    error: { bg: '#FFF1F2', border: '#FDA4AF', text: '#9F1239' },
    success: { bg: '#ECFDF5', border: '#6EE7B7', text: '#065F46' },
    line: '#94A3B8', lineLabel: '#64748B',
    canvas: '#FFFFFF', title: '#1a1a2e', subtitle: '#888',
    // 统计图序列色
    series: ['#667eea', '#f5576c', '#43e97b', '#4facfe', '#fa8231', '#a55eea', '#fc5c65', '#26de81'],
    // 层级色（架构图、C4 等分层用）
    layers: ['#667eea', '#43e97b', '#4facfe', '#f59e0b', '#8b5cf6', '#f43f5e'],
  },
  // 后续扩展：
  // dark: { ... },
  // business: { ... },
  // vibrant: { ... },
};
```

**使用方式**：布局函数接收 `theme` 参数，所有颜色从 theme 对象取值，不硬编码。

```javascript
function renderFlowchart(data, theme) {
  theme = theme || themes.default;
  // 所有节点颜色从 theme 取
  createNode(node, { bg: theme.node.bg, border: theme.node.border });
}
```

**扩展新配色**：只需新增一个 theme 对象，不改任何布局代码。

**SKILL.md 中的使用**：Claude 根据用户场景或明确指定选择配色方案。默认用 `default`，用户说"暗色风格"就切换到 `dark`。

---

### 八、最小宽度约束

所有图表输出宽度 ≥ 1000px（匹配 Markdown 预览宽度），不设固定上限：
- 横向图：宽度 ≥ 1000px
- 纵向图：宽度 ≥ 800px
- 内容超过最小宽度时按实际内容尺寸

### 九、成功标准

1. 11 个静态模板全部改为动态布局
2. 每种图表通过 4 级复杂度验证（见下表），均无重叠、无截断
3. 通用兜底算法能处理未知图表类型，生成可用（不一定完美）的图
4. 验证检查通过率 > 95%（允许极端数据量下的少量妥协）

### 十、分图表类型验证标准

不同图表类型的合理数据量差异很大，统一倍率不现实。验证标准按图表特性分别定义，每种图表必须通过 4 级复杂度测试。

**验证原则**：
- 每级复杂度需构造真实场景数据（不是随机填充）
- 验收标准：无重叠、无截断、无超出画布、连线不穿越节点
- 超级复杂级允许画布高度很大，但必须保持可读性

#### P0 图表

| 复杂度 | flowchart | sequence | er |
|--------|-----------|----------|-----|
| **L1 简单** | 4 步，0 判断 | 3 参与者，5 消息 | 3 表，3 关系 |
| **L2 中等** | 8 步，2 判断 | 5 参与者，12 消息 | 6 表，8 关系 |
| **L3 复杂** | 12 步，3 判断，多节点类型 | 8 参与者，20 消息，含自调用 | 10 表，15 关系，含多对多 |
| **L4 超级复杂** | 15 步，4 判断（规范上限） | 10 参与者，30 消息，含片段 | 15 表，25 关系 |

#### P1 图表

| 复杂度 | class | architecture | swimlane |
|--------|-------|-------------|----------|
| **L1 简单** | 3 类，2 关系 | 3 层，各 2 节点 | 2 泳道，4 步骤 |
| **L2 中等** | 6 类，5 关系 | 5 层，各 3 节点 | 3 泳道，8 步骤 |
| **L3 复杂** | 9 类含枚举/接口，10 关系 | 7 层，含多行 | 4 泳道，12 步骤含判断 |
| **L4 超级复杂** | 15 类，20 关系，复杂继承 | 10 层，混合节点 | 5 泳道，15 步骤 |

#### P2 图表

| 复杂度 | state | fishbone/swot/venn/journey |
|--------|-------|---------------------------|
| **L1 简单** | 4 状态，4 转换 | 3 条目/分支 |
| **L2 中等** | 6 状态，8 转换 | 6 条目/分支 |
| **L3 复杂** | 8 状态含自循环，12 转换 | 10 条目/分支 |
| **L4 超级复杂** | 12 状态含并行，20 转换 | 15 条目/分支 |

> **说明**：流程图规范限制 15 节点上限（超过应拆子流程），因此 L4 不超过 15 步。其他图表类型按各自的实际使用极限设定。
