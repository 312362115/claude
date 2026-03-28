# Dagre 布局算法源码深度分析

> 基于 [dagrejs/dagre](https://github.com/dagrejs/dagre) 最新 TypeScript 版本的逐行源码分析。
> 目标：理解每一步算法细节，足以独立重新实现。

---

## 目录

1. [总体架构](#1-总体架构)
2. [数据结构](#2-数据结构)
3. [参数表](#3-参数表)
4. [算法全流程](#4-算法全流程)
5. [Phase 1: 预处理](#5-phase-1-预处理)
6. [Phase 2: 层级分配 (Rank Assignment)](#6-phase-2-层级分配-rank-assignment)
7. [Phase 3: 节点排序 (Crossing Reduction)](#7-phase-3-节点排序-crossing-reduction)
8. [Phase 4: 坐标分配 (Coordinate Assignment)](#8-phase-4-坐标分配-coordinate-assignment)
9. [Phase 5: 后处理](#9-phase-5-后处理)
10. [rankdir 处理机制](#10-rankdir-处理机制)
11. [边路由与控制点](#11-边路由与控制点)
12. [边标签定位](#12-边标签定位)
13. [子图/集群支持](#13-子图集群支持)
14. [最小化实现方案](#14-最小化实现方案)

---

## 1. 总体架构

Dagre 实现的是经典的 **Sugiyama 分层布局算法**（又称 Sugiyama-Tagawa-Toda 方法），论文来源主要是 *Gansner et al., "A Technique for Drawing Directed Graphs"*（即 dot 算法论文）。

算法分为 4 大阶段（加上预处理和后处理共 6 阶段）：

```
输入图 → 预处理 → 层级分配 → 节点排序 → 坐标分配 → 后处理 → 输出图
```

入口函数在 `lib/layout.ts` 的 `runLayout()`，按严格顺序执行 25 个步骤：

```
1.  makeSpaceForEdgeLabels    — 为边标签腾出空间
2.  removeSelfEdges           — 移除自环边
3.  acyclic.run               — 消除环路（反转后向边）
4.  nestingGraph.run          — 处理子图嵌套
5.  rank                      — 层级分配（核心）
6.  injectEdgeLabelProxies    — 注入边标签代理节点
7.  removeEmptyRanks          — 移除空层级
8.  nestingGraph.cleanup      — 清理嵌套图辅助结构
9.  normalizeRanks            — 归一化层级（最小层级=0）
10. assignRankMinMax           — 计算子图的层级范围
11. removeEdgeLabelProxies     — 移除边标签代理节点
12. normalize.run              — 长边拆分（插入虚拟节点）
13. parentDummyChains          — 虚拟节点的父子关系
14. addBorderSegments          — 子图边界节点
15. order                      — 节点排序/交叉减少（核心）
16. insertSelfEdges            — 重新插入自环边
17. adjustCoordinateSystem     — LR/RL 时交换宽高
18. position                   — 坐标分配（核心）
19. positionSelfEdges          — 自环边坐标
20. removeBorderNodes          — 移除子图边界节点
21. normalize.undo             — 恢复长边（移除虚拟节点）
22. fixupEdgeLabelCoords       — 修正边标签坐标
23. undoCoordinateSystem       — 恢复坐标系统
24. translateGraph             — 平移图使左上角对齐原点
25. assignNodeIntersects       — 计算边与节点边框的交点
26. reversePoints              — 反转被翻转边的点序列
27. acyclic.undo               — 恢复被反转的边
```

---

## 2. 数据结构

### 2.1 Graph 对象（来自 @dagrejs/graphlib）

Dagre 使用 graphlib 的 `Graph` 类，支持：
- **有向图** (directed)
- **多重边** (multigraph) — 同一对节点间可有多条边
- **复合图** (compound) — 节点可嵌套（父子关系）

关键 API：
```typescript
graph.setNode(v, label)    // 设置节点
graph.setEdge(v, w, label) // 设置边（或 setEdge({v, w, name}, label)）
graph.node(v)              // 获取节点标签
graph.edge(e)              // 获取边标签
graph.parent(v)            // 获取父节点
graph.children(v)          // 获取子节点
graph.inEdges(v)           // 入边
graph.outEdges(v)          // 出边
graph.sources()            // 没有入边的节点
graph.sinks()              // 没有出边的节点
graph.predecessors(v)      // 前驱节点
graph.successors(v)        // 后继节点
graph.neighbors(v)         // 邻居（无向）
graph.nodeEdges(v)         // 所有关联边
```

### 2.2 NodeLabel

```typescript
interface NodeLabel {
    width: number;          // 节点宽度（用户提供）
    height: number;         // 节点高度（用户提供）
    x?: number;             // 计算得到的 x 坐标（中心点）
    y?: number;             // 计算得到的 y 坐标（中心点）
    rank?: number;          // 所在层级
    order?: number;         // 层内排序位置
    dummy?: string;         // 虚拟节点类型：'edge' | 'border' | 'edge-label' | 'edge-proxy' | 'selfedge' | 'root'
    // 子图相关
    borderTop?: string;     // 子图顶部边界节点
    borderBottom?: string;  // 子图底部边界节点
    borderLeft?: string[];  // 每层的左边界节点
    borderRight?: string[]; // 每层的右边界节点
    minRank?: number;       // 子图最小层级
    maxRank?: number;       // 子图最大层级
    // 长边拆分后的引用
    edgeLabel?: EdgeLabel;  // 原始边标签
    edgeObj?: Edge;         // 原始边对象
}
```

### 2.3 EdgeLabel

```typescript
interface EdgeLabel {
    points?: Point[];       // 边的控制点列表
    width?: number;         // 边标签宽度
    height?: number;        // 边标签高度
    minlen?: number;        // 最小跨层数（默认 1）
    weight?: number;        // 边权重（默认 1）
    labelpos?: 'l'|'c'|'r'; // 标签位置
    labeloffset?: number;   // 标签偏移量（默认 10）
    labelRank?: number;     // 标签所在层级
    x?: number;             // 标签 x 坐标
    y?: number;             // 标签 y 坐标
    reversed?: boolean;     // 是否被反转（消除环路时）
    cutvalue?: number;      // 网络单纯形的割值
    nestingEdge?: boolean;  // 是否是嵌套边
}
```

### 2.4 GraphLabel

```typescript
interface GraphLabel {
    rankdir?: 'TB'|'BT'|'LR'|'RL';  // 布局方向
    align?: 'UL'|'UR'|'DL'|'DR';     // 对齐方式
    rankalign?: 'top'|'center'|'bottom'; // 层内垂直对齐
    nodesep?: number;        // 同层节点间距
    edgesep?: number;        // 同层边间距（虚拟节点间距）
    ranksep?: number;        // 层间距
    marginx?: number;        // 水平边距
    marginy?: number;        // 垂直边距
    acyclicer?: 'greedy';    // 消环算法
    ranker?: 'network-simplex'|'tight-tree'|'longest-path'; // 层级算法
    // 运行时属性
    nestingRoot?: string;    // 嵌套图根节点
    nodeRankFactor?: number; // 节点层级因子
    dummyChains?: string[];  // 虚拟节点链头列表
    maxRank?: number;        // 最大层级
}
```

---

## 3. 参数表

### 3.1 图级参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `rankdir` | `'TB'\|'BT'\|'LR'\|'RL'` | `'TB'` | 布局方向。TB=上到下, BT=下到上, LR=左到右, RL=右到左 |
| `align` | `'UL'\|'UR'\|'DL'\|'DR'` | `undefined` | 节点对齐方式（BK 算法使用）。undefined 时取 4 种对齐的中位数 |
| `rankalign` | `'top'\|'center'\|'bottom'` | `'center'` | 层内垂直对齐方式 |
| `nodesep` | `number` | `50` | 同一层中相邻节点间的最小间距（像素） |
| `edgesep` | `number` | `20` | 同一层中相邻边（虚拟节点）间的最小间距（像素） |
| `ranksep` | `number` | `50` | 相邻层之间的间距（像素）。注意内部会除以 2 |
| `marginx` | `number` | `0` | 图的水平外边距 |
| `marginy` | `number` | `0` | 图的垂直外边距 |
| `acyclicer` | `'greedy'\|undefined` | `undefined` | 消环算法。undefined=DFS, 'greedy'=贪心FAS |
| `ranker` | `string` | `'network-simplex'` | 层级分配算法 |

### 3.2 节点参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `width` | `number` | `0` | 节点宽度 |
| `height` | `number` | `0` | 节点高度 |

### 3.3 边参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `minlen` | `number` | `1` | 边的最小跨层数 |
| `weight` | `number` | `1` | 边的权重（影响布局紧凑度） |
| `width` | `number` | `0` | 边标签宽度 |
| `height` | `number` | `0` | 边标签高度 |
| `labelpos` | `'l'\|'c'\|'r'` | `'r'` | 边标签位置（左/中/右） |
| `labeloffset` | `number` | `10` | 边标签偏移量 |

---

## 4. 算法全流程

### 伪代码

```
function layout(inputGraph):
    layoutGraph = buildLayoutGraph(inputGraph)  // 复制 + 规范化
    runLayout(layoutGraph)
    updateInputGraph(inputGraph, layoutGraph)    // 结果回写
    return layoutGraph

function runLayout(g):
    // ---- Phase 0: 预处理 ----
    makeSpaceForEdgeLabels(g)       // ranksep /= 2, minlen *= 2
    removeSelfEdges(g)              // 自环暂存到节点上
    acyclic.run(g)                  // 反转后向边使图变 DAG

    // ---- Phase 1: 嵌套图处理 ----
    nestingGraph.run(g)             // 子图→边界节点+嵌套边
    rank(asNonCompoundGraph(g))     // 在非复合图上分层
    injectEdgeLabelProxies(g)       // 边标签占位节点
    removeEmptyRanks(g)             // 删除空层
    nestingGraph.cleanup(g)         // 清理嵌套辅助结构
    normalizeRanks(g)               // rank 从 0 开始
    assignRankMinMax(g)             // 子图 minRank/maxRank
    removeEdgeLabelProxies(g)       // 移除占位节点

    // ---- Phase 2: 长边标准化 ----
    normalize.run(g)                // 长边拆分为单位长度
    parentDummyChains(g)            // 虚拟节点设置正确的父节点
    addBorderSegments(g)            // 子图边界节点

    // ---- Phase 3: 节点排序 ----
    order(g)                        // 交叉减少

    // ---- Phase 4: 坐标分配 ----
    insertSelfEdges(g)              // 自环变虚拟节点
    coordinateSystem.adjust(g)      // LR/RL 时 swap width/height
    position(g)                     // BK 算法分配 x/y

    // ---- Phase 5: 后处理 ----
    positionSelfEdges(g)            // 自环控制点
    removeBorderNodes(g)            // 计算子图尺寸后删除边界节点
    normalize.undo(g)               // 恢复长边，收集控制点
    fixupEdgeLabelCoords(g)         // 修正标签坐标
    coordinateSystem.undo(g)        // 恢复坐标系
    translateGraph(g)               // 平移到原点
    assignNodeIntersects(g)         // 边端点裁剪到节点边界
    reversePointsForReversedEdges(g)
    acyclic.undo(g)                 // 恢复被反转的边
```

---

## 5. Phase 1: 预处理

### 5.1 makeSpaceForEdgeLabels

**目的**：为边标签在层间创造空间。

**算法**：
1. `ranksep /= 2` — 将层间距减半
2. 每条边的 `minlen *= 2` — 边的最小跨层数翻倍
3. 如果标签不在中间位置（labelpos !== 'c'），根据方向增加边的宽度或高度

**原理**：翻倍 minlen 后，原本相邻层之间会多出一个"虚拟层"，用于放置边标签。ranksep 减半使得最终总间距不变。

```
原始：  rank0 ---[ranksep=50]--- rank1
变换后：rank0 --[25]-- 标签层 --[25]-- rank1（边 minlen=2 保证跨 2 层）
```

### 5.2 removeSelfEdges

**目的**：自环边在分层布局中没有意义（源和目标是同一节点），暂时移除。

**算法**：
```
for each edge e where e.v === e.w:
    node = graph.node(e.v)
    node.selfEdges.push({e, label: graph.edge(e)})
    graph.removeEdge(e)
```

自环信息暂存在节点的 `selfEdges` 属性中，后续 `insertSelfEdges` 会重新插入。

### 5.3 acyclic.run — 消除环路

**目的**：Sugiyama 算法要求输入是 DAG，需要找到并反转一些边使图无环。

**两种算法**：

#### 5.3.1 DFS 消环（默认）

```
function dfsFAS(graph):
    fas = []           // feedback arc set（需要反转的边集）
    stack = {}         // 当前 DFS 路径上的节点
    visited = {}       // 已访问节点

    function dfs(v):
        if v in visited: return
        visited[v] = true
        stack[v] = true
        for each outEdge e of v:
            if e.w in stack:    // 发现后向边（环）
                fas.push(e)
            else:
                dfs(e.w)
        delete stack[v]

    for each node v in graph:
        dfs(v)
    return fas
```

找到 FAS 后，对每条边执行反转：
```
for each edge e in fas:
    label = graph.edge(e)
    graph.removeEdge(e)
    label.reversed = true
    label.forwardName = e.name
    graph.setEdge(e.w, e.v, label, uniqueId("rev"))  // 反转方向
```

#### 5.3.2 Greedy FAS（acyclicer='greedy'）

来自论文 *Eades, Lin, Smyth, "A fast and effective heuristic for the feedback arc set problem"*。

**算法**：
1. 为每个节点计算 `in`（加权入度）和 `out`（加权出度）
2. 创建 `2*(maxIn + maxOut) + 3` 个桶，`zeroIdx = maxIn + 1`
3. 将每个节点放入桶中：
   - `out == 0` → 桶 0（sink）
   - `in == 0` → 最后一个桶（source）
   - 其他 → 桶 `out - in + zeroIdx`
4. 循环直到图为空：
   - 先移除所有 sink（桶 0），不记录
   - 再移除所有 source（最后一个桶），不记录
   - 如果还有节点，取差值最大的桶（从高到低扫描），移除一个节点，**记录其入边到 FAS**
5. 移除节点时更新邻居的 in/out 值并重新分桶

**复杂度**：O(|V| + |E|)，比纯 DFS 通常能找到更小的 FAS。

### 5.4 acyclic.undo — 恢复反转的边

在所有布局完成后，将被反转的边恢复原方向：
```
for each edge e where e.label.reversed:
    graph.removeEdge(e)
    delete label.reversed
    graph.setEdge(e.w, e.v, label, forwardName)
```

---

## 6. Phase 2: 层级分配 (Rank Assignment)

**目的**：为每个节点分配一个整数层级（rank），使得所有边从低层级指向高层级，且满足 `rank(w) - rank(v) >= minlen(v→w)`。

三种算法可选，默认 `network-simplex`。

### 6.1 Longest Path（最长路径）

**最简单但效果最差的算法**。

```
function longestPath(graph):
    visited = {}

    function dfs(v):
        if v in visited: return node(v).rank
        visited[v] = true

        outEdges = graph.outEdges(v)
        minRank = min(dfs(e.w) - e.minlen for each e in outEdges)

        if minRank == +Infinity:  // 叶子节点
            minRank = 0

        return node(v).rank = minRank

    for each source node v:
        dfs(v)
```

**特点**：
- 叶子节点（sink）rank = 0，其他节点尽量靠近叶子
- 导致底层（rank 0）非常宽，上层很窄
- 边倾向于比必要的更长
- 时间复杂度 O(|V| + |E|)

### 6.2 Tight Tree（紧树）

```
function tightTreeRanker(graph):
    longestPath(graph)     // 先用最长路径初始化
    feasibleTree(graph)    // 再构建紧树调整
```

### 6.3 Network Simplex（网络单纯形，默认）

**最复杂但效果最好的算法**，来自 Gansner 论文。

#### 6.3.1 整体流程

```
function networkSimplex(graph):
    graph = simplify(graph)    // 多重边合并为单边
    longestPath(graph)         // 初始排名
    tree = feasibleTree(graph) // 构建可行紧树
    initLowLimValues(tree)     // DFS 编号
    initCutValues(tree, graph) // 计算割值

    while (e = leaveEdge(tree)):     // 找负割值边
        f = enterEdge(tree, graph, e) // 找替换边
        exchangeEdges(tree, graph, e, f) // 交换
```

#### 6.3.2 simplify — 多重边合并

```
function simplify(graph):
    newGraph = new Graph()
    copy all nodes
    for each edge e:
        existing = newGraph.edge(e.v, e.w)
        if existing:
            existing.weight += e.weight
            existing.minlen = max(existing.minlen, e.minlen)
        else:
            newGraph.setEdge(e.v, e.w, {weight: e.weight, minlen: e.minlen})
```

#### 6.3.3 feasibleTree — 构建可行紧树

**定义**：紧边（tight edge）= slack 为 0 的边，其中 `slack(e) = rank(w) - rank(v) - minlen(e)`。

```
function feasibleTree(graph):
    tree = new UndirectedGraph()
    tree.setNode(graph.nodes()[0])  // 从任意节点开始

    while tightTree(tree, graph) < graph.nodeCount():
        // 树还没有覆盖所有节点
        edge = findMinSlackEdge(tree, graph)  // 找一端在树内一端在树外的最小 slack 边
        delta = tree.hasNode(edge.v) ? slack(edge) : -slack(edge)
        // 移动树中所有节点的 rank，使该边变紧
        shiftRanks(tree, graph, delta)

    return tree
```

`tightTree` 通过 DFS 扩展树：从树中现有节点出发，沿着 slack=0 的边加入新节点。

`findMinSlackEdge` 扫描所有边，找一端在树中一端不在且 slack 最小的边。

`shiftRanks` 将树中所有节点的 rank 加上 delta，使目标边变为紧边。

#### 6.3.4 initLowLimValues — DFS 编号

对树做 DFS，为每个节点分配 `low` 和 `lim` 值：
- `low(v)` = v 的子树中最小的 DFS 后序号
- `lim(v)` = v 自身的 DFS 后序号
- `parent(v)` = v 在树中的父节点

这些值用于 O(1) 判断一个节点是否是另一个节点的后代：
```
isDescendant(v, root) = root.low <= v.lim && v.lim <= root.lim
```

#### 6.3.5 initCutValues — 计算割值

对树的每条边计算**割值（cut value）**。割值衡量的是：如果移除这条树边，图被分成两部分（尾部和头部），跨越这两部分的边的权重总和（尾→头为正，头→尾为负）。

```
function calcCutValue(tree, graph, child):
    parent = tree.node(child).parent
    childIsTail = graph.hasEdge(child, parent)  // 确定方向
    if not childIsTail:
        graphEdge = graph.edge(parent, child)

    cutValue = graphEdge.weight

    for each edge of child in graph (except parent edge):
        other = opposite end of edge
        isOutEdge = edge.v === child
        pointsToHead = isOutEdge === childIsTail

        cutValue += pointsToHead ? edge.weight : -edge.weight

        if edge(child, other) is in tree:
            cutValue += pointsToHead ? -tree.edge(child,other).cutvalue
                                     : tree.edge(child,other).cutvalue

    return cutValue
```

使用后序遍历计算，从叶子到根，每个节点的割值依赖于其子树中已计算的割值。

#### 6.3.6 leaveEdge — 找离开边

扫描树的所有边，返回第一条割值为负的边。负割值意味着存在改进空间。

```
function leaveEdge(tree):
    return tree.edges().find(e => tree.edge(e).cutvalue < 0)
```

#### 6.3.7 enterEdge — 找进入边

找到一条非树边来替换要移除的树边。

```
function enterEdge(tree, graph, edge):
    v = edge.v, w = edge.w
    if not graph.hasEdge(v, w): swap(v, w)  // 确保 v 是尾

    vLabel = tree.node(v)
    wLabel = tree.node(w)
    tailLabel = vLabel
    flip = false

    if vLabel.lim > wLabel.lim:  // root 在尾部
        tailLabel = wLabel
        flip = true

    // 找候选边：一端在尾侧，一端在头侧
    candidates = graph.edges().filter(e =>
        flip === isDescendant(e.v, tailLabel) &&
        flip !== isDescendant(e.w, tailLabel))

    // 取 slack 最小的
    return candidates.reduce((best, e) =>
        slack(e) < slack(best) ? e : best)
```

#### 6.3.8 exchangeEdges — 交换边

```
function exchangeEdges(tree, graph, leaveEdge, enterEdge):
    tree.removeEdge(leaveEdge.v, leaveEdge.w)
    tree.setEdge(enterEdge.v, enterEdge.w, {})
    initLowLimValues(tree)     // 重新计算 DFS 编号
    initCutValues(tree, graph) // 重新计算割值
    updateRanks(tree, graph)   // 更新所有节点的 rank
```

`updateRanks` 从根节点出发，按前序遍历重新计算每个节点的 rank：
```
function updateRanks(tree, graph):
    root = tree.nodes().find(v => !tree.node(v).parent)
    for each v in preorder(tree, root) (skip root):
        parent = tree.node(v).parent
        edge = graph.edge(v, parent)  // 或 graph.edge(parent, v)
        if edge is (v→parent): // 边从子到父
            rank(v) = rank(parent) - edge.minlen
        else:                  // 边从父到子
            rank(v) = rank(parent) + edge.minlen
```

#### 6.3.9 Network Simplex 复杂度

- 理论最坏 O(|V|^2 * |E|)，实践中通常很快
- 每次迭代的 `initCutValues` 和 `initLowLimValues` 都是 O(|V|)
- `enterEdge` 中对所有边的扫描是 O(|E|)
- 迭代次数通常远小于 |V|

### 6.4 层级后处理

#### normalizeRanks
使最小 rank 变为 0：
```
minRank = min(rank(v) for all v)
for each v: rank(v) -= minRank
```

#### removeEmptyRanks
移除没有节点的层级（由嵌套图产生的空层），但保留 `nodeRankFactor` 的倍数层。

---

## 7. Phase 3: 节点排序 (Crossing Reduction)

**目的**：确定每一层中节点的左右顺序，最小化层间的边交叉数。

### 7.1 长边标准化 (normalize.run)

**前置步骤**：在排序之前，必须确保所有边只跨一层。

```
function normalizeEdge(graph, e):
    v = e.v, vRank = node(v).rank
    w = e.w, wRank = node(w).rank

    if wRank === vRank + 1: return  // 已经是短边

    graph.removeEdge(e)
    edgeLabel = originalEdgeLabel

    for rank from vRank+1 to wRank-1:
        dummy = addDummyNode(graph, "edge", {
            width: 0, height: 0,
            edgeLabel: edgeLabel,  // 引用原始边
            edgeObj: e,
            rank: rank
        })

        if rank === edgeLabel.labelRank:
            // 这个虚拟节点承载边标签
            dummy.width = edgeLabel.width
            dummy.height = edgeLabel.height
            dummy.dummy = "edge-label"

        graph.setEdge(prevNode, dummy, {weight: edgeLabel.weight})
        if first dummy:
            graph.dummyChains.push(dummy)  // 记录链头

        prevNode = dummy

    graph.setEdge(prevNode, w, {weight: edgeLabel.weight})
```

**示例**：
```
A(rank=0) → B(rank=3) 变为：
A(rank=0) → d1(rank=1) → d2(rank=2) → B(rank=3)
```

### 7.2 normalize.undo — 恢复长边

```
function undo(graph):
    for each chain head v in graph.dummyChains:
        node = graph.node(v)
        origLabel = node.edgeLabel
        graph.setEdge(node.edgeObj, origLabel)  // 恢复原始边

        while node.dummy:
            w = graph.successors(v)[0]
            graph.removeNode(v)
            origLabel.points.push({x: node.x, y: node.y})  // 收集控制点
            if node.dummy === "edge-label":
                origLabel.x = node.x
                origLabel.y = node.y
                origLabel.width = node.width
                origLabel.height = node.height
            v = w
            node = graph.node(v)
```

**关键**：虚拟节点的 x, y 坐标成为最终边的控制点。

### 7.3 initOrder — 初始排序

```
function initOrder(graph):
    visited = {}
    layers = [[] for 0..maxRank]

    function dfs(v):
        if visited[v]: return
        visited[v] = true
        layers[node(v).rank].push(v)
        for each successor w of v:
            dfs(w)

    // 按 rank 排序后 DFS
    orderedNodes = simpleNodes.sort(by rank)
    orderedNodes.forEach(dfs)

    return layers
```

通过 DFS 赋予初始排序，保证连接的节点倾向于相邻。

### 7.4 order — 主排序循环

**核心算法**：层扫描（layer-by-layer sweep）+ 重心法（barycenter heuristic）

```
function order(graph, opts):
    maxRank = util.maxRank(graph)

    // 构建层图：每层一个图，包含该层节点及与上/下层的连接
    downLayerGraphs = buildLayerGraphs(graph, [1..maxRank], "inEdges")
    upLayerGraphs = buildLayerGraphs(graph, [maxRank-1..0], "outEdges")

    layering = initOrder(graph)
    assignOrder(graph, layering)

    bestCC = +Infinity
    best = null

    for i = 0; lastBest < 4; i++, lastBest++:
        // 交替向下扫描和向上扫描
        if i % 2 == 1: sweep(downLayerGraphs)
        else:           sweep(upLayerGraphs)

        // i%4 >= 2 时 biasRight=true
        biasRight = (i % 4 >= 2)

        layering = buildLayerMatrix(graph)
        cc = crossCount(graph, layering)

        if cc < bestCC:
            lastBest = 0
            best = layering
            bestCC = cc

    assignOrder(graph, best)
```

**终止条件**：连续 4 次迭代没有改善就停止。

**biasRight**：交替使用左偏和右偏来打破平局，增加探索多样性。

### 7.5 sweepLayerGraphs

```
function sweepLayerGraphs(layerGraphs, biasRight, constraints):
    constraintGraph = new Graph()

    for each layerGraph lg:
        // 应用用户约束
        constraints.forEach(con => constraintGraph.setEdge(con.left, con.right))

        root = lg.graph().root
        sorted = sortSubgraph(lg, root, constraintGraph, biasRight)
        sorted.vs.forEach((v, i) => lg.node(v).order = i)
        addSubgraphConstraints(lg, constraintGraph, sorted.vs)
```

### 7.6 buildLayerGraph

为每一层构建一个**层图**，包含：
- 该层的所有节点（保持层次结构）
- 一个虚拟根节点作为无父节点的容器
- 与相邻层的边（权重聚合）

```
function buildLayerGraph(graph, rank, relationship, nodesWithRank):
    root = createRootNode(graph)
    result = new CompoundGraph({root: root})

    for each v in nodesWithRank:
        if node(v).rank === rank or node(v) spans rank:
            result.setNode(v)
            result.setParent(v, parent(v) || root)

            // 添加与相邻层的边
            for each edge e via relationship(v):  // inEdges or outEdges
                u = other end
                weight = existingWeight + graph.edge(e).weight
                result.setEdge(u, v, {weight})
```

### 7.7 sortSubgraph — 递归排序

```
function sortSubgraph(graph, v, constraintGraph, biasRight):
    movable = graph.children(v)
    bl = node(v).borderLeft   // 子图左边界
    br = node(v).borderRight  // 子图右边界

    if bl: movable = movable.filter(w => w !== bl && w !== br)

    // 1. 计算重心
    barycenters = barycenter(graph, movable)

    // 2. 递归处理子图
    for each entry in barycenters:
        if entry has children:
            subResult = sortSubgraph(graph, entry.v, constraintGraph, biasRight)
            mergeBarycenters(entry, subResult)

    // 3. 解决约束冲突
    entries = resolveConflicts(barycenters, constraintGraph)

    // 4. 展开子图
    expandSubgraphs(entries, subgraphs)

    // 5. 排序
    result = sort(entries, biasRight)

    // 6. 添加边界节点
    if bl and br:
        result.vs = [bl, ...result.vs, br]

    return result
```

### 7.8 barycenter — 重心计算

**核心公式**：节点 v 的重心 = 其上层邻居位置的加权平均

```
function barycenter(graph, movable):
    return movable.map(v =>
        inEdges = graph.inEdges(v)
        if no inEdges:
            return {v}  // 无重心，自由节点

        sum = 0, weight = 0
        for each inEdge e:
            sum += edge(e).weight * node(e.v).order
            weight += edge(e).weight

        return {v, barycenter: sum / weight, weight}
    )
```

**示例**：
```
上层：A(order=0)  B(order=1)  C(order=2)
边：A→X(w=1), C→X(w=2)
X 的重心 = (1*0 + 2*2) / (1+2) = 4/3 ≈ 1.33
```

### 7.9 resolveConflicts — 冲突解决

基于 Forster 的论文 *"A Fast and Simple Heuristic for Constrained Two-Level Crossing Reduction"*。

当约束图（constraintGraph）中有 A→B 的边（表示 A 必须在 B 左边），但重心建议 B 在 A 左边时，需要将 A 和 B 合并为一个组。

```
function resolveConflicts(entries, constraintGraph):
    // 构建入度图
    for each constraint edge (u→v):
        if both u, v in entries:
            v.indegree++
            u.out.push(v)

    sourceSet = entries with indegree == 0

    while sourceSet not empty:
        entry = sourceSet.pop()
        // 尝试合并入边方向的节点
        for each predecessor u of entry:
            if u.barycenter undefined or u.barycenter >= entry.barycenter:
                merge(entry, u)  // 合并：合并 vs 列表，加权平均重心
        // 减少后继的入度
        for each successor w of entry:
            w.indegree--
            if w.indegree == 0: sourceSet.push(w)

    return unmerged entries
```

### 7.10 sort — 最终排序

```
function sort(entries, biasRight):
    sortable = entries with barycenter     // 有重心的
    unsortable = entries without barycenter // 无重心的，按原始 index 降序

    // 按重心排序
    sortable.sort(by barycenter, tie-break by index)

    // 将无重心的节点插入到它们原始位置附近
    vs = []
    vsIndex = 0
    consumeUnsortable(vs, unsortable, vsIndex)

    for each sortable entry:
        vsIndex += entry.vs.length
        vs.push(entry.vs)
        consumeUnsortable(vs, unsortable, vsIndex)

    return {vs: flatten(vs)}
```

`consumeUnsortable`：将原始 index 不超过当前 vsIndex 的无重心节点插入。

**biasRight** 的作用：平局时，`biasRight=false` 优先保留原始顺序，`biasRight=true` 优先反转。

### 7.11 crossCount — 交叉计数

使用 Barth et al. 的 **"Bilayer Cross Counting"** 算法，基于归并排序思想的累加树。

```
function twoLayerCrossCount(graph, northLayer, southLayer):
    southPos = {node: index for each node in southLayer}

    // 收集所有跨层边，按北层位置排序
    southEntries = []
    for each v in northLayer:
        for each outEdge e of v:
            southEntries.push({pos: southPos[e.w], weight: e.weight})
        sort by pos

    // 构建累加树（大小为 2 * nextPowerOf2(southLayer.length) - 1）
    firstIndex = nextPowerOf2(southLayer.length) - 1
    tree = Array(2 * firstIndex + 1).fill(0)

    cc = 0
    for each entry in southEntries:
        index = entry.pos + firstIndex  // 叶子位置
        tree[index] += entry.weight

        // 向上累加，统计右侧已有的权重
        weightSum = 0
        while index > 0:
            if index is odd:  // 左子节点
                weightSum += tree[index + 1]  // 右兄弟的权重 = 已插入的在其右侧的边
            index = (index - 1) >> 1  // 父节点
            tree[index] += entry.weight

        cc += entry.weight * weightSum

    return cc
```

**复杂度**：O(|E| * log|V|)

**原理**：累加树是一种分段树。对于每条边，我们在插入时统计之前已插入的、位置在其右侧的边数——这些边与当前边形成交叉。

---

## 8. Phase 4: 坐标分配 (Coordinate Assignment)

### 8.1 positionY — Y 坐标

```
function positionY(graph):
    layering = buildLayerMatrix(graph)
    ranksep = graph.ranksep
    prevY = 0

    for each layer:
        maxHeight = max(node.height for each node in layer)

        for each node v in layer:
            if rankalign === "top":
                v.y = prevY + v.height / 2
            elif rankalign === "bottom":
                v.y = prevY + maxHeight - v.height / 2
            else:  // center (default)
                v.y = prevY + maxHeight / 2

        prevY += maxHeight + ranksep
```

**注意**：坐标是节点**中心点**。Y 坐标从上到下递增。

### 8.2 positionX — X 坐标（BK 算法）

基于 Brandes & Köpf 的论文 *"Fast and Simple Horizontal Coordinate Assignment"*。

#### 8.2.1 总体思路

1. 检测冲突（Type-1 和 Type-2）
2. 进行 4 次对齐（UL, UR, DL, DR 四个方向组合）
3. 每次对齐包含：垂直对齐 → 水平压缩
4. 找最窄的对齐作为基准
5. 将 4 种对齐对齐到基准
6. 取中位数作为最终坐标

```
function positionX(graph):
    layering = buildLayerMatrix(graph)
    conflicts = findType1Conflicts(graph, layering)
                + findType2Conflicts(graph, layering)

    xss = {}
    for vert in ["u", "d"]:           // 上对齐 / 下对齐
        adjustedLayering = vert=="u" ? layering : reversed(layering)

        for horiz in ["l", "r"]:      // 左对齐 / 右对齐
            if horiz=="r":
                adjustedLayering = each layer reversed

            neighborFn = vert=="u" ? predecessors : successors
            align = verticalAlignment(graph, adjustedLayering, conflicts, neighborFn)
            xs = horizontalCompaction(graph, adjustedLayering, align.root, align.align, horiz=="r")

            if horiz=="r":
                xs = mapValues(xs, x => -x)  // 翻转回来

            xss[vert+horiz] = xs

    smallestWidth = findSmallestWidthAlignment(graph, xss)
    alignCoordinates(xss, smallestWidth)
    return balance(xss, graph.align)
```

#### 8.2.2 冲突检测

**Type-1 冲突**：非内部线段与内部线段交叉。内部线段 = 两端都是虚拟节点（dummy）的边。

```
function findType1Conflicts(graph, layering):
    conflicts = {}
    for each pair of adjacent layers [prevLayer, layer]:
        k0 = 0       // 上一个内部线段在上层的位置
        scanPos = 0

        for each v in layer at position i:
            w = findOtherInnerSegmentNode(graph, v)  // v 是 dummy 且有 dummy 前驱
            k1 = w ? node(w).order : prevLayer.length

            if w or v is last in layer:
                // 扫描 scanPos..i 的所有节点
                for each scanNode in layer[scanPos..i]:
                    for each predecessor u of scanNode:
                        uPos = node(u).order
                        if (uPos < k0 or k1 < uPos) and not (both dummy):
                            addConflict(conflicts, u, scanNode)
                scanPos = i + 1
                k0 = k1

    return conflicts
```

**Type-2 冲突**：内部线段之间的交叉，发生在子图边界处。

#### 8.2.3 verticalAlignment — 垂直对齐

将节点组织成**块（block）**——同一块中的节点在垂直方向对齐。

使用两个数组：
- `root[v]`：v 所属块的根节点
- `align[v]`：v 在块中的下一个节点（链表）

```
function verticalAlignment(graph, layering, conflicts, neighborFn):
    root = {v: v for all v}
    align = {v: v for all v}
    pos = {}

    // 缓存位置
    for each layer, for each (v, order): pos[v] = order

    for each layer:
        prevIdx = -1
        for each v in layer:
            ws = neighborFn(v).sort(by pos)
            if ws is empty: continue

            // 取中位数邻居
            mp = (ws.length - 1) / 2
            for i from floor(mp) to ceil(mp):
                w = ws[i]
                if align[v] === v          // v 还没被对齐
                   && prevIdx < pos[w]     // w 在上一个对齐的右边（不交叉）
                   && !hasConflict(v, w):  // 没有冲突
                    align[w] = v
                    align[v] = root[v] = root[w]
                    prevIdx = pos[w]

    return {root, align}
```

**中位数**：当邻居数为偶数时，尝试两个中间位置（floor 和 ceil）。优先左中位数（先尝试 floor），但如果已被占用则用右中位数。

#### 8.2.4 horizontalCompaction — 水平压缩

将对齐的块分配具体的 x 坐标。

**步骤**：
1. 构建**块图（block graph）**：每个块是一个节点，相邻块之间有边表示最小间距
2. 第一遍：从左到右分配最小坐标
3. 第二遍：从右到左收紧

```
function horizontalCompaction(graph, layering, root, align, reverseSep):
    xs = {}
    blockG = buildBlockGraph(graph, layering, root, reverseSep)

    // Pass 1: 分配最小坐标（拓扑排序，从左到右）
    for each node elem in topological order:
        xs[elem] = max(xs[predecessor] + separation for each predecessor)
        if no predecessors: xs[elem] = 0

    // Pass 2: 收紧（从右到左）
    for each node elem in reverse topological order:
        min = min(xs[successor] - separation for each successor)
        if min != +Infinity and node is not border:
            xs[elem] = max(xs[elem], min)

    // 将块根的坐标传播给块内所有节点
    for each v: xs[v] = xs[root[v]]

    return xs
```

**buildBlockGraph** 中的间距计算：

```
function sep(nodeSep, edgeSep, reverseSep):
    return (g, v, w):
        sum = 0
        sum += v.width / 2
        // 考虑标签位置偏移
        if v has labelpos:
            delta = labelpos=="l" ? -v.width/2 : v.width/2
            sum += reverseSep ? delta : -delta

        // 根据节点类型选择间距
        sum += (v.dummy ? edgeSep : nodeSep) / 2
        sum += (w.dummy ? edgeSep : nodeSep) / 2

        sum += w.width / 2
        // 同样考虑 w 的标签位置
        return sum
```

**关键**：虚拟节点（dummy）之间用 `edgeSep`，真实节点之间用 `nodeSep`。

#### 8.2.5 findSmallestWidthAlignment

```
function findSmallestWidthAlignment(graph, xss):
    return alignment with minimum (max(x + width/2) - min(x - width/2))
```

#### 8.2.6 alignCoordinates

将 4 种对齐方式统一到相同的参考线：
- 左偏对齐（ul, dl）：最小 x 对齐到最窄对齐的最小 x
- 右偏对齐（ur, dr）：最大 x 对齐到最窄对齐的最大 x

#### 8.2.7 balance

如果指定了 `align` 参数，直接使用对应的对齐方式。否则取 4 种对齐的**中位数**（排序后取第 2 和第 3 个值的平均）。

```
function balance(xss, align):
    if align specified:
        return xss[align.toLowerCase()]

    for each v:
        values = [xss.ul[v], xss.ur[v], xss.dl[v], xss.dr[v]].sort()
        result[v] = (values[1] + values[2]) / 2
    return result
```

---

## 9. Phase 5: 后处理

### 9.1 positionSelfEdges

自环边生成 5 个控制点，形成一个右侧的弧形：

```
function positionSelfEdges(graph):
    for each selfedge dummy node:
        selfNode = original node
        x = selfNode.x + selfNode.width / 2  // 节点右边缘
        y = selfNode.y                        // 节点中心
        dx = dummyNode.x - x                  // 向右偏移
        dy = selfNode.height / 2              // 半高

        points = [
            {x + 2dx/3, y - dy},    // 右上
            {x + 5dx/6, y - dy},    // 更右上
            {x + dx,    y},          // 最右中
            {x + 5dx/6, y + dy},    // 更右下
            {x + 2dx/3, y + dy}     // 右下
        ]
```

### 9.2 removeBorderNodes

计算子图的最终尺寸和位置：
```
for each compound node v:
    top = node(v.borderTop)
    bottom = node(v.borderBottom)
    left = node(last of v.borderLeft)
    right = node(last of v.borderRight)

    v.width = |right.x - left.x|
    v.height = |bottom.y - top.y|
    v.x = left.x + width/2
    v.y = top.y + height/2

then: remove all nodes with dummy="border"
```

### 9.3 translateGraph

将整个图平移使左上角在 (marginx, marginy)：

```
function translateGraph(graph):
    minX = min(node.x - node.width/2 for all nodes and labeled edges)
    minY = min(node.y - node.height/2 for all nodes and labeled edges)

    for each node: node.x -= (minX - marginX), node.y -= (minY - marginY)
    for each edge point: point.x -= (minX - marginX), point.y -= (minY - marginY)

    graph.width = maxX - minX + marginX
    graph.height = maxY - minY + marginY
```

### 9.4 assignNodeIntersects

计算边的起止点，使其落在节点矩形边界上：

```
function assignNodeIntersects(graph):
    for each edge e:
        nodeV = node(e.v), nodeW = node(e.w)

        if no points:
            points = []
            p1 = nodeW, p2 = nodeV
        else:
            p1 = points[0], p2 = points[last]

        // 在起始端插入交点
        points.unshift(intersectRect(nodeV, p1))
        // 在终止端追加交点
        points.push(intersectRect(nodeW, p2))
```

**intersectRect** 算法：

```
function intersectRect(rect, point):
    dx = point.x - rect.x
    dy = point.y - rect.y
    w = rect.width / 2
    h = rect.height / 2

    if |dy| * w > |dx| * h:
        // 交点在上边或下边
        if dy < 0: h = -h
        sx = h * dx / dy
        sy = h
    else:
        // 交点在左边或右边
        if dx < 0: w = -w
        sx = w
        sy = w * dy / dx

    return {x: rect.x + sx, y: rect.y + sy}
```

### 9.5 fixupEdgeLabelCoords

修正标签位置，考虑 labeloffset：
```
for each edge with label:
    if labelpos == "l" or "r":
        edge.width -= labeloffset
    if labelpos == "l":
        edge.x -= edge.width/2 + labeloffset
    if labelpos == "r":
        edge.x += edge.width/2 + labeloffset
```

---

## 10. rankdir 处理机制

**核心思路**：算法始终按 TB（上到下）计算，对于其他方向通过坐标变换实现。

### 10.1 adjust（布局前）

```
if rankdir == 'LR' or 'RL':
    swapWidthHeight(graph)  // 所有节点和边标签的 width/height 互换
```

LR/RL 时，"层"的方向是水平的，所以将宽高互换后用 TB 算法计算。

### 10.2 undo（布局后）

```
if rankdir == 'BT' or 'RL':
    reverseY(graph)  // 所有 y 坐标取负

if rankdir == 'LR' or 'RL':
    swapXY(graph)            // x/y 互换
    swapWidthHeight(graph)   // 宽高换回来
```

**完整变换**：

| rankdir | adjust（前） | undo（后） | 效果 |
|---------|-------------|-----------|------|
| TB | 无 | 无 | 正常上到下 |
| BT | 无 | reverseY | 下到上 |
| LR | swapWH | swapXY + swapWH | 左到右 |
| RL | swapWH | reverseY + swapXY + swapWH | 右到左 |

---

## 11. 边路由与控制点

### 11.1 控制点来源

边的控制点来自三个来源：

1. **虚拟节点坐标**（normalize.undo）：长边拆分产生的虚拟节点，其 x/y 坐标成为控制点
2. **节点交点**（assignNodeIntersects）：边起止端裁剪到节点矩形边界
3. **自环边**（positionSelfEdges）：手工构造的 5 个弧形控制点

### 11.2 最终 points 格式

```
edge.points = [
    {x, y},   // 起始节点边框交点
    {x, y},   // 虚拟节点 1 的位置（中间控制点）
    {x, y},   // 虚拟节点 2 的位置
    ...
    {x, y}    // 终止节点边框交点
]
```

对于跨 1 层的短边：`points = [startIntersect, endIntersect]`（2 个点）
对于跨 N 层的长边：`points = [startIntersect, dummy1, dummy2, ..., dummyN-2, endIntersect]`

### 11.3 使用方式

这些控制点可以用于：
- **折线**：直接连接所有点
- **贝塞尔曲线**：作为 cubic bezier 的控制点
- dagre-d3 / dagre-graphviz 等渲染库通常用 d3.curveBasis 绘制

---

## 12. 边标签定位

### 12.1 labelpos 选项

| 值 | 说明 |
|----|------|
| `'c'` | 标签在边的中间（占据整个边宽度） |
| `'l'` | 标签在边的左侧 |
| `'r'` | 标签在边的右侧（默认） |

### 12.2 实现流程

1. `makeSpaceForEdgeLabels`：如果 labelpos 不是 'c'，增加边的宽度（加上 labeloffset）
2. `normalize.run`：边标签所在的虚拟节点（dummy="edge-label"）继承标签的宽度和高度
3. 布局引擎将 edge-label 节点当作正常节点参与布局
4. `normalize.undo`：从 edge-label 虚拟节点提取 x/y 坐标赋给边标签
5. `fixupEdgeLabelCoords`：根据 labelpos 调整标签的最终 x 坐标

---

## 13. 子图/集群支持

### 13.1 nestingGraph.run

将复合图（compound graph）的层次结构转换为扁平的边约束。

**步骤**：
1. 计算每个节点的树深度
2. 创建 `nestingRoot` 虚拟根节点
3. 将所有边的 `minlen *= nodeSep`（其中 `nodeSep = 2 * treeHeight + 1`）
4. 为每个子图创建 `borderTop` 和 `borderBottom` 虚拟节点
5. 添加嵌套边：top→children, children→bottom（高权重确保紧凑）
6. root→每个无父叶子节点（weight=0, 保证连通）
7. 记录 `nodeRankFactor = nodeSep`

### 13.2 parentDummyChains

确保长边拆分产生的虚拟节点被放在正确的子图中。通过 LCA（最近公共祖先）计算虚拟节点应属于哪个子图。

### 13.3 addBorderSegments

为跨越多层的子图，在每一层添加左右边界虚拟节点：
```
for each rank in [minRank..maxRank]:
    node.borderLeft[rank] = addDummyNode("border", "_bl")
    node.borderRight[rank] = addDummyNode("border", "_br")
    // 相邻层的边界节点用 weight=1 的边连接
```

---

## 14. 最小化实现方案

### 14.1 使用场景

目标场景：5-15 个节点，无子图，正交边（直角折线），TB/LR 方向。

### 14.2 可以省略的模块

| 模块 | 是否需要 | 原因 |
|------|---------|------|
| nestingGraph | **不需要** | 无子图 |
| parentDummyChains | **不需要** | 无子图 |
| addBorderSegments | **不需要** | 无子图 |
| removeBorderNodes | **不需要** | 无子图 |
| greedy-fas | **不需要** | DFS 消环足够 |
| resolveConflicts | **简化** | 无子图约束，可以直接排序 |
| addSubgraphConstraints | **不需要** | 无子图 |
| Type-2 conflicts | **不需要** | 仅与子图边界相关 |
| 自环处理 | **可选** | 取决于是否有自环 |
| edge label | **简化** | 如果不需要边标签可以大幅简化 |

### 14.3 最小实现的步骤

```
1. 消环（DFS FAS）                    ~40 行
2. 层级分配（longest-path 即可）         ~30 行
3. 长边标准化（虚拟节点）               ~40 行
4. 初始排序（DFS）                     ~25 行
5. 交叉减少（barycenter + 扫描）        ~80 行
6. 交叉计数（累加树）                   ~40 行
7. Y 坐标分配                          ~15 行
8. X 坐标分配（简化 BK 或直接重心法）    ~100 行
9. 恢复长边 + 收集控制点               ~25 行
10. 节点交点计算                        ~20 行
11. 坐标系变换（LR/RL 支持）            ~30 行
12. 平移到原点                          ~20 行
13. 图数据结构                          ~100 行
```

### 14.4 进一步简化选项

**如果只需要正交边**：
- 控制点只需要在每层的固定 y 位置，x 与虚拟节点对齐
- 可以直接用 x 坐标生成折线，不需要 BK 算法的复杂对齐
- 正交边路由：在虚拟节点位置做直角转弯

**如果可以接受简单的 x 坐标**：
- 用重心法直接分配 x 坐标（每个节点取其邻居的平均位置）
- 多次迭代直到收敛
- 比 BK 算法简单得多，但结果不如 BK 紧凑

### 14.5 代码量估算

| 方案 | 估计行数（JS） | 说明 |
|------|---------------|------|
| **完整移植** | ~1200 行 | 移除子图支持后的完整 dagre |
| **简化 BK** | ~600 行 | 用简化的 BK（只做 1 次对齐而非 4 次） |
| **重心法坐标** | ~400 行 | 用迭代重心法代替 BK |
| **极简版** | ~300 行 | longest-path + 单次 barycenter 扫描 + 重心坐标 |

### 14.6 推荐方案

对于 5-15 节点的场景，推荐 **~400 行方案**：

1. **层级分配**：longest-path（30 行）— 节点少时效果与 network simplex 差别不大
2. **排序**：barycenter + 4 次上下扫描（80 行）— 这是效果提升最大的部分
3. **坐标**：迭代重心法分配 x（60 行）— 简单有效
4. **正交边路由**：虚拟节点位置做直角转弯（20 行）

**核心权衡**：
- Network simplex vs longest-path：15 个节点以下差异很小，longest-path 够用
- BK 算法 vs 重心法坐标：BK 更紧凑但实现复杂，重心法对小图足够
- 4 次扫描 vs 更多次：4 次扫描（dagre 默认最多 ~8 次）对小图完全足够

### 14.7 最小图数据结构

不需要完整的 graphlib，一个简单的邻接表即可：

```typescript
interface SimpleGraph {
    nodes: Map<string, NodeData>;
    edges: Array<{v: string, w: string, label: EdgeData}>;
    outEdges: Map<string, Edge[]>;
    inEdges: Map<string, Edge[]>;
}
```

约 80 行即可实现所需的图操作。

---

## 附录 A：关键引用论文

1. **Gansner, Koutsofios, North, Vo** — *"A Technique for Drawing Directed Graphs"* (1993)
   - 整体 Sugiyama 框架、network simplex 层级分配

2. **Brandes, Köpf** — *"Fast and Simple Horizontal Coordinate Assignment"* (2001)
   - BK 坐标分配算法（4 次对齐 + 中位数）

3. **Barth, Jünger, Mutzel** — *"Bilayer Cross Counting"* (2002)
   - 高效交叉计数（累加树方法）

4. **Eades, Lin, Smyth** — *"A fast and effective heuristic for the feedback arc set problem"* (1993)
   - 贪心 FAS 算法

5. **Forster** — *"A Fast and Simple Heuristic for Constrained Two-Level Crossing Reduction"* (2004)
   - 约束冲突解决

6. **Sander** — *"Layout of Compound Directed Graphs"* (1996)
   - 嵌套图/子图处理

## 附录 B：dagre 默认值速查

```
Graph:   rankdir=TB, rankalign=center, nodesep=50, edgesep=20, ranksep=50
Node:    width=0, height=0
Edge:    minlen=1, weight=1, width=0, height=0, labeloffset=10, labelpos=r
Ranker:  network-simplex
Acyclic: DFS (not greedy)
Order:   up to 4 iterations without improvement, then stop
BK:      4 alignments (UL,UR,DL,DR), balanced by median
```
