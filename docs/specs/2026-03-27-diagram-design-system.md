# 画图 Skill 设计规范（Design System）

> 所有图表工具（D2 / Mermaid / ECharts / HTML+SVG）的统一视觉规范。
> 参考：Geist (Vercel)、Radix Colors、Carbon Design System、Cloudscape。
> 风格关键词：**现代、简洁、低饱和、专业、一致**。

---

## 一、调色板（Color Palette）

### 1.1 设计原则

- **低饱和度**：不使用纯色（#FF0000），使用调和后的柔和色
- **高对比度**：文字/背景对比度 ≥ 4.5:1（WCAG AA）
- **有序递进**：同一色相有 3 级——浅底（背景）、中间色（边框）、深色（文字/图标）
- **跨工具一致**：D2 style、Mermaid theme、ECharts color[]、CSS 变量使用同一组色值

### 1.2 基础色（Neutral）

| 色号 | 色值 | 用途 |
|------|------|------|
| N-0 | `#FFFFFF` | 画布背景 |
| N-1 | `#F8FAFC` | 容器/卡片背景 |
| N-2 | `#F1F5F9` | 次级背景、交替行 |
| N-3 | `#E2E8F0` | 边框、分割线 |
| N-4 | `#CBD5E1` | 禁用、占位、连线默认色 |
| N-5 | `#94A3B8` | 连线、次级图标 |
| N-6 | `#64748B` | 次级文字、图例 |
| N-7 | `#1E293B` | 主文字 |
| N-8 | `#0F172A` | 标题文字 |

### 1.3 主题色序列（Categorical）— 8 色

用于数据系列区分、分类标识。按顺序使用，相邻色有足够对比度。

| 序号 | 名称 | 主色 | 浅底 | 中间色（边框） | 深色（文字） |
|------|------|------|------|--------------|------------|
| C-1 | Blue | `#3B82F6` | `#EFF6FF` | `#93C5FD` | `#1E40AF` |
| C-2 | Emerald | `#10B981` | `#ECFDF5` | `#6EE7B7` | `#065F46` |
| C-3 | Amber | `#F59E0B` | `#FFFBEB` | `#FCD34D` | `#92400E` |
| C-4 | Rose | `#F43F5E` | `#FFF1F2` | `#FDA4AF` | `#9F1239` |
| C-5 | Violet | `#8B5CF6` | `#F5F3FF` | `#C4B5FD` | `#5B21B6` |
| C-6 | Cyan | `#06B6D4` | `#ECFEFF` | `#67E8F9` | `#155E75` |
| C-7 | Orange | `#F97316` | `#FFF7ED` | `#FDBA74` | `#9A3412` |
| C-8 | Slate | `#64748B` | `#F8FAFC` | `#CBD5E1` | `#334155` |

### 1.4 语义色（Semantic）

| 语义 | 主色 | 浅底 | 用途 |
|------|------|------|------|
| 主要/信息 | `#3B82F6` | `#EFF6FF` | 高亮节点、当前状态、默认操作 |
| 成功/正面 | `#10B981` | `#ECFDF5` | 完成、通过、正向指标 |
| 警告/注意 | `#F59E0B` | `#FFFBEB` | 判断节点、待处理、需关注 |
| 错误/危险 | `#F43F5E` | `#FFF1F2` | 失败、异常、负向指标 |

### 1.5 层级色（Layer）

用于架构图、分层图的各层背景区分。

| 层级 | 背景色 | 边框色 | 标签色 |
|------|--------|--------|--------|
| L-1 | `#EFF6FF` | `#BFDBFE` | `#1E40AF` |
| L-2 | `#ECFDF5` | `#A7F3D0` | `#065F46` |
| L-3 | `#FFFBEB` | `#FDE68A` | `#92400E` |
| L-4 | `#F5F3FF` | `#C4B5FD` | `#5B21B6` |
| L-5 | `#FFF1F2` | `#FECDD3` | `#9F1239` |
| L-6 | `#ECFEFF` | `#A5F3FC` | `#155E75` |

---

## 二、字体（Typography）

### 2.1 字体栈

```
中文：PingFang SC, "Noto Sans CJK SC", "Microsoft YaHei", sans-serif
英文：Inter, -apple-system, "Segoe UI", sans-serif
等宽："JetBrains Mono", "SF Mono", "Fira Code", monospace
```

### 2.2 字号层级

| 级别 | 字号 | 字重 | 用途 |
|------|------|------|------|
| T-1 图表标题 | 16px | Bold (700) | 图表顶部主标题 |
| T-2 副标题 | 13px | Regular (400) | 副标题、说明文字 |
| T-3 节点文字 | 13px | Medium (500) | 流程图节点、坐标轴标签 |
| T-4 次级标签 | 12px | Regular (400) | 图例文字、辅助说明 |
| T-5 数据标注 | 11px | Medium (500) | 柱状图数值、饼图百分比 |
| T-6 注脚 | 10px | Regular (400) | 数据来源标注 |

### 2.3 行高

- 标题：1.3
- 正文/节点：1.5

---

## 三、基础组件库（Primitives）

> 所有图表由以下原子组件组合而成。每个组件有唯一的样式定义。

### 3.1 节点类型

#### 3.1.1 流程步骤（Process）

标准的处理/操作步骤。

| 属性 | 值 |
|------|-----|
| 形状 | 圆角矩形 |
| 圆角 | `6px` |
| 填充色 | `#EFF6FF`（C-1 浅底） |
| 边框 | `1.5px solid #93C5FD`（C-1 中间色） |
| 文字 | `13px Medium #1E293B`（N-7） |
| 内间距 | `10px 16px` |
| 最小宽度 | `120px` |
| 阴影 | 无（默认），重要节点可加 `0 1px 3px rgba(0,0,0,0.06)` |

#### 3.1.2 开始/结束（Terminal）

流程的起点和终点。

| 属性 | 值 |
|------|-----|
| 形状 | 椭圆 / 跑道形（stadium） |
| 填充色 | 开始：`#ECFDF5`（成功浅底），结束：`#F1F5F9`（N-2） |
| 边框 | 开始：`1.5px solid #6EE7B7`，结束：`1.5px solid #CBD5E1` |
| 文字 | `13px Medium`，开始：`#065F46`，结束：`#64748B` |
| 内间距 | `8px 20px` |

#### 3.1.3 判断/决策（Decision）

条件分支。

| 属性 | 值 |
|------|-----|
| 形状 | 菱形（diamond） |
| 填充色 | `#FFFBEB`（警告浅底） |
| 边框 | `1.5px solid #FCD34D`（Amber 中间色） |
| 文字 | `12px Medium #92400E`（Amber 深色） |
| 内间距 | `8px 12px` |
| 出口标签 | "是/否"或"通过/失败"，`11px`，紧贴出口连线 |

#### 3.1.4 数据/存储（Data Store）

数据库、文件、缓存等存储类节点。

| 属性 | 值 |
|------|-----|
| 形状 | 圆柱（cylinder） |
| 填充色 | `#F5F3FF`（Violet 浅底） |
| 边框 | `1.5px solid #C4B5FD` |
| 文字 | `13px Medium #5B21B6` |

#### 3.1.5 外部系统（External）

外部 API、第三方服务。

| 属性 | 值 |
|------|-----|
| 形状 | 圆角矩形，虚线边框 |
| 填充色 | `#F8FAFC`（N-1） |
| 边框 | `1.5px dashed #CBD5E1`（N-4） |
| 文字 | `13px Regular #64748B`（N-6） |

#### 3.1.6 高亮/关键节点（Highlight）

需要强调的核心节点。

| 属性 | 值 |
|------|-----|
| 形状 | 圆角矩形 |
| 填充色 | `#3B82F6`（C-1 主色，实心） |
| 边框 | 无 |
| 文字 | `13px Bold #FFFFFF`（白色） |
| 阴影 | `0 2px 8px rgba(59,130,246,0.25)` |

#### 3.1.7 错误/异常节点（Error）

错误状态、异常路径终点。

| 属性 | 值 |
|------|-----|
| 形状 | 圆角矩形 |
| 填充色 | `#FFF1F2`（Rose 浅底） |
| 边框 | `1.5px solid #FDA4AF` |
| 文字 | `13px Medium #9F1239` |

#### 3.1.8 成功节点（Success）

完成状态。

| 属性 | 值 |
|------|-----|
| 形状 | 圆角矩形 |
| 填充色 | `#ECFDF5`（Emerald 浅底） |
| 边框 | `1.5px solid #6EE7B7` |
| 文字 | `13px Medium #065F46` |

#### 3.1.9 注释/备注（Note）

附加说明信息。

| 属性 | 值 |
|------|-----|
| 形状 | 矩形，左边框加粗 |
| 填充色 | `#F8FAFC`（N-1） |
| 左边框 | `3px solid #3B82F6` |
| 其他边框 | `1px solid #E2E8F0` |
| 文字 | `12px Regular #64748B` |

### 3.2 连线类型

#### 3.2.1 标准连线（Default Edge）

| 属性 | 值 |
|------|-----|
| 线宽 | `1.5px` |
| 颜色 | `#94A3B8`（N-5） |
| 路由 | 直角折线（orthogonal），转角处无圆角 |
| 箭头 | 实心三角，大小 `6px` |
| 锚点 | 出入节点**居中**（上/下/左/右的中点） |

#### 3.2.2 带标签连线（Labeled Edge）

| 属性 | 值 |
|------|-----|
| 基础样式 | 同标准连线 |
| 标签字号 | `11px Regular` |
| 标签颜色 | `#64748B`（N-6） |
| 标签位置 | 连线中点偏上，不覆盖连线本身 |
| 标签背景 | `#FFFFFF`（白底），`padding: 2px 6px`，避免与线交叉 |

#### 3.2.3 虚线连线（Dashed Edge）

用于异步、可选、弱依赖关系。

| 属性 | 值 |
|------|-----|
| 线宽 | `1.5px` |
| 颜色 | `#94A3B8` |
| 虚线 | `stroke-dasharray: 6 3` |
| 箭头 | 同标准连线 |

#### 3.2.4 语义连线（Semantic Edge）

用于强调特定路径（成功/失败/高亮）。

| 语义 | 颜色 | 线宽 |
|------|------|------|
| 成功路径 | `#10B981` | `2px` |
| 失败路径 | `#F43F5E` | `2px` |
| 高亮路径 | `#3B82F6` | `2px` |

#### 3.2.5 返回/回退连线（Return Edge）

| 属性 | 值 |
|------|-----|
| 线宽 | `1px` |
| 颜色 | `#CBD5E1`（N-4，比普通连线浅） |
| 虚线 | `stroke-dasharray: 4 2` |
| 箭头 | 开放箭头（非实心） |

### 3.3 容器类型

#### 3.3.1 分组容器（Group / Cluster）

| 属性 | 值 |
|------|-----|
| 背景色 | 使用层级色浅底（L-1 ~ L-6） |
| 边框 | `1px solid` + 对应层级色边框色 |
| 圆角 | `8px` |
| 标签 | 左上角，`13px Bold`，对应层级色标签色 |
| 内间距 | `16px` |

#### 3.3.2 泳道容器（Swimlane）

| 属性 | 值 |
|------|-----|
| 标签区 | 左侧固定宽度 `60px`，背景使用主题色序列主色，文字白色 `14px Bold` |
| 内容区 | 交替使用 N-0 和 N-1 背景 |
| 分隔线 | `1px solid #E2E8F0`（N-3） |
| 圆角 | 整体容器 `8px`，标签区左上左下圆角 |

#### 3.3.3 层级容器（Architecture Layer）

用于架构图的水平分层。

| 属性 | 值 |
|------|-----|
| 布局 | 水平全宽，垂直堆叠 |
| 背景色 | 使用层级色浅底 |
| 左侧标签 | 固定宽度 `100px`，标签色文字，`14px Bold` + `11px Regular` 副标题 |
| 层间连接 | 虚线分隔 + 协议/接口标注（居中，`10px`，`#94A3B8`） |
| 层内组件 | 使用对应层级色的主色为填充，白色文字，`12px Medium`，`border-radius: 4px` |

---

## 四、排版与布局规则（Layout）

### 4.1 间距网格

- 基础单位：`4px`
- 常用间距：`8px`（紧凑）/ `12px`（默认）/ `16px`（宽松）/ `24px`（段落）/ `32px`（区块）

### 4.2 流向规则

| 图表类型 | 默认流向 | 允许的替代流向 |
|---------|---------|-------------|
| 流程图 | 从上到下（TB） | 从左到右（LR），适合步骤少但步骤内容多的情况 |
| 时序图 | 从上到下（时间轴） | 仅从上到下 |
| 架构图 | 从上到下（分层） | 仅从上到下 |
| 泳道图 | 从左到右（流程推进） | 从上到下，适合泳道数多的情况 |
| 层次图 | 从上到下（树状） | 从左到右 |
| 关系图 | 自动布局 | 无约束 |
| 状态图 | 从左到右 | 自动布局 |

### 4.3 节点对齐规则

- 同级节点**水平对齐**（TB 流向）或**垂直对齐**（LR 流向）
- 判断节点的"是/否"分支：主路径继续原方向，备选路径转向垂直方向
- 合并点（多条路径汇聚）：汇聚到同一节点，不创建额外的"合并节点"

### 4.4 连线锚点规则

- 出入节点的连接点在节点边缘的**中点**
- TB 流向：出口在底边中点，入口在顶边中点
- LR 流向：出口在右边中点，入口在左边中点
- 分支连线从判断节点的**侧边中点**出发
- 禁止连线交叉；如不可避免，用跨线桥（arc）标识

### 4.5 标题与图表的关系

```
┌─────────────────────────────────┐
│  标题（16px Bold，左对齐）         │  ← 距顶部 16px
│  副标题（13px Regular，左对齐）     │  ← 距标题 4px
│                                   │  ← 距图表区域 16px
│  ┌─────────────────────────────┐ │
│  │                             │ │
│  │      图表内容区域             │ │
│  │                             │ │
│  └─────────────────────────────┘ │
│                                   │  ← 距图例 12px
│  ○ 图例1  ○ 图例2  ○ 图例3       │  ← 底部居中
│                                   │  ← 距底部 16px
└─────────────────────────────────┘
```

---

## 五、图表专属规范（29 种）

### 5.1 流程图（Flowchart / Activity Diagram）

**工具**：D2（主）/ Mermaid（备）

**组件使用**：
- 开始节点：Terminal（成功色）
- 处理步骤：Process
- 判断：Decision
- 结束节点：Terminal（中性色）
- 错误终点：Error

**布局规则**：
- 默认 TB（从上到下）
- 主路径保持直线向下，分支向左右展开
- 判断节点的"是"路径向下，"否"路径向右（或向左）
- 回退/重试路径用虚线返回连线，走节点外侧绕回
- 节点间距：纵向 `32px`，横向 `48px`
- 子流程用分组容器包裹，标签说明子流程名称

**禁忌**：
- 不超过 15 个节点（超过应拆分为子流程）
- 不使用弧线连线
- 不使用超过 3 层嵌套的判断

### 5.2 泳道图（Swimlane Diagram）

**工具**：HTML/SVG

**组件使用**：
- 泳道容器（Swimlane Container）
- 内部节点：Process / Decision / Terminal
- 跨泳道连线：标准连线 + 标签

**布局规则**：
- 默认水平泳道（行=角色，列=时间推进）
- 泳道标签在最左侧，固定宽度，使用主题色序列
- 流程从左到右推进
- 跨泳道连线用直角折线，垂直段穿过泳道分隔线
- 同一泳道内的节点水平排列
- 泳道高度自适应内容，最小高度 `80px`
- 底部图例标注：流程步骤形状、判断形状、连线类型含义

**禁忌**：
- 不超过 5 条泳道
- 每条泳道内节点不超过 6 个
- 跨泳道连线不应超过 2 条泳道跨度

### 5.3 时序图（Sequence Diagram）

**工具**：D2（`shape: sequence_diagram`）

**组件使用**：
- 参与者：圆角矩形 + 生命线（垂直虚线）
- 激活条：窄矩形叠加在生命线上
- 消息箭头：同步实线、异步虚线、返回虚线
- 分组框：alt / loop / opt 片段

**布局规则**：
- 参与者水平排列在顶部，间距均匀（`80-120px`）
- 消息按时间顺序从上到下排列
- 消息标签在箭头上方，左对齐
- 激活条：宽 `10px`，填充 `#DBEAFE`，边框 `#93C5FD`
- 自调用（self-call）：箭头从参与者右侧出发绕回
- 分组框：浅灰边框 `#E2E8F0`，左上角标签 `#F1F5F9` 背景

**禁忌**：
- 参与者不超过 6 个
- 消息不超过 20 条
- 避免过多嵌套的分组框（最多 2 层）

### 5.4 架构图（Architecture / Component Diagram）

**工具**：HTML/CSS

**组件使用**：
- 层级容器（Architecture Layer）
- 层内组件：使用对应层级色的色块节点
- 层间连接：虚线 + 协议标注

**布局规则**：
- 从上到下分层堆叠（客户端 → 接入层 → 服务层 → 中间件 → 数据层 → 基础设施）
- 每层用全宽的层级容器，左侧标签，右侧组件水平排列
- 层与层之间用虚线分隔，标注通信协议（HTTP / gRPC / TCP 等）
- 同层组件等宽等高，水平等距排列
- 组件不带连线（架构图展示的是层级关系，不是调用关系）
- 整体宽度 `960px`，居中显示

**禁忌**：
- 不画具体连线（那是时序图/调用链路图的职责）
- 不超过 7 层
- 每层组件不超过 8 个

### 5.5 状态图（State Diagram）

**工具**：D2

**组件使用**：
- 初始状态：实心小圆点（`●`）
- 状态节点：Process 样式
- 终止状态：同心圆（`◉`）
- 转换连线：标准连线 + 事件/条件标签

**布局规则**：
- 默认 LR（从左到右）
- 初始状态在最左侧
- 终止状态在最右侧
- 主流程水平推进，异常分支向下展开
- 状态节点内可包含子状态（用分组容器）
- 自转换（self-transition）用箭头绕回自身顶部

**禁忌**：
- 状态不超过 10 个
- 避免连线交叉

### 5.6 ER 图（Entity Relationship Diagram）

**工具**：D2（`shape: sql_table`）

**组件使用**：
- 实体表：D2 的 sql_table 形状
- 关系连线：带基数标注（1:1 / 1:N / M:N）

**布局规则**：
- 核心实体居中，关联实体围绕核心展开
- 表头使用对应色系背景（不同业务域用不同色）
- PK 字段加粗，FK 字段标注来源
- 连线基数标注在连线两端
- 统一使用 D2 默认的浅色主题，不给每个表染不同的高饱和色

**禁忌**：
- 单图不超过 8 张表
- 不展示全部字段（只展示 PK/FK + 核心业务字段）

### 5.7 网络拓扑图（Network Topology）

**工具**：D2

**组件使用**：
- 网络设备：使用 D2 内置 icon 或标注形状（cloud / cylinder / rectangle）
- 网络区域：分组容器
- 连接线：标准连线，标注带宽/协议

**布局规则**：
- 从上到下：外网 → DMZ → 内网
- 网络区域用分组容器，不同区域用不同层级色
- 设备水平排列在区域内
- 连线标注端口号/协议/带宽

### 5.8 决策树（Decision Tree）

**工具**：D2

**组件使用**：
- 根节点：Highlight 样式
- 判断节点：Decision
- 叶子节点：Process / Success / Error

**布局规则**：
- 从上到下（TB），树状展开
- 每层判断条件水平对齐
- 分支标签在连线上
- 叶子节点用语义色区分结果好坏

### 5.9 数据流图（Data Flow Diagram）

**工具**：D2

**组件使用**：
- 处理过程：Process（圆角矩形）
- 数据存储：Data Store（圆柱）
- 外部实体：External（虚线矩形）
- 数据流：标准连线 + 数据名称标签

**布局规则**：
- 中央处理过程，周围环绕数据存储和外部实体
- 数据流连线标注数据名称
- 层次：上下文图 → 0 级 → 1 级，逐级细化

### 5.10 类图（Class Diagram）

**工具**：D2（`shape: class`）/ Mermaid

**组件使用**：
- 类：三栏矩形（类名 / 属性 / 方法）
- 接口：类似类，标签为 `«interface»`
- 关系：继承(▷)、实现(▷虚线)、组合(◆)、聚合(◇)、依赖(-->)

**布局规则**：
- 父类/接口在上方，子类在下方
- 继承关系用空心三角箭头
- 类名 `14px Bold`，属性/方法 `12px Regular`
- 访问修饰符前缀：`+` public / `-` private / `#` protected

### 5.11 C4 容器图（C4 Container Diagram）

**工具**：Mermaid（`C4Context` / `C4Container`）

**组件使用**：
- Person：圆角矩形 + 人物图标
- System：矩形
- Container：矩形，标注技术栈
- 外部系统：虚线矩形

**布局规则**：
- 遵循 C4 模型标准
- 人物在顶部，系统/容器在中间，外部依赖在底部或侧边
- 每个容器标注名称 + 技术栈 + 简述

### 5.12 思维导图（Mind Map）

**工具**：Mermaid（`mindmap`）

**布局规则**：
- 中心节点：Highlight 样式
- 一级分支：使用主题色序列（每个方向一种色）
- 二级以下：同方向保持同色系，渐淡
- 节点文字简洁（≤ 8 个字）
- 不超过 3 层深度

### 5.13 甘特图（Gantt Chart）

**工具**：Mermaid（`gantt`）

**布局规则**：
- 任务分组（section）用层级色区分
- 里程碑用菱形标记
- 关键路径高亮
- 时间轴标注合理（按天/周/月）
- 今日线用 Rose 颜色标注

### 5.14 时间线（Timeline）

**工具**：Mermaid（`timeline`）

**布局规则**：
- 从左到右时间推进
- 时间节点等距分布
- 事件描述简洁
- 使用主题色序列区分不同时期/阶段

### 5.15 SWOT 分析图

**工具**：HTML/SVG

**布局规则**：
- 2×2 网格布局
- 左上（优势）：Emerald 浅底，右上（劣势）：Rose 浅底
- 左下（机会）：Blue 浅底，右下（威胁）：Amber 浅底
- 每个象限标题 `14px Bold` + 语义色
- 内容条目 `13px Regular`，左对齐，行距 `1.6`
- 整体 `800px × 500px`

### 5.16 鱼骨图（Fishbone / Ishikawa）

**工具**：HTML/SVG

**布局规则**：
- 右侧：问题节点（Highlight 样式）
- 中轴：水平主线（`2px solid #94A3B8`）
- 上方 3 类 + 下方 3 类（使用主题色序列）
- 分支线 45° 角斜线
- 子原因挂在分支线上
- 类别标签 `13px Bold`，子原因 `12px Regular`

### 5.17 组织结构图（Org Chart）

**工具**：HTML/SVG

**布局规则**：
- 从上到下树状展开
- 每个节点：姓名 `14px Bold` + 职位 `12px Regular #64748B`
- 不同层级使用不同色系区分
- 连线从父节点底部中心到子节点顶部中心
- 虚线连接矩阵汇报关系

### 5.18 文氏图（Venn Diagram）

**工具**：HTML/SVG

**布局规则**：
- 2-3 个圆形，使用主题色序列
- 圆形填充使用主色 + `opacity: 0.15`
- 边框使用主色 + `opacity: 0.4`
- 交集区域自然叠加（CSS mix-blend-mode 或 SVG 透明度）
- 每个圆标注名称 `14px Bold`，交集区域标注共有特征
- 圆外标注独有特征列表

### 5.19 用户旅程图（Customer Journey Map）

**工具**：HTML/SVG

**布局规则**：
- 水平时间线（阶段从左到右）
- 上方：情感曲线（折线图，绿高红低）
- 下方：每阶段卡片（触点、行为、痛点、机会）
- 阶段标题使用主题色序列
- 卡片使用 N-1 背景，`border-radius: 8px`
- 情感曲线节点：😊 😐 😩 用颜色代替（绿/黄/红）

---

## 六、统计图表专属规范（ECharts）

### 6.1 全局 ECharts 主题

```javascript
const THEME = {
  backgroundColor: '#FFFFFF',
  color: ['#3B82F6','#10B981','#F59E0B','#F43F5E','#8B5CF6','#06B6D4','#F97316','#64748B'],
  textStyle: { fontFamily: 'PingFang SC, Inter, sans-serif', color: '#64748B' },
  title: {
    textStyle: { fontSize: 16, fontWeight: 700, color: '#0F172A' },
    subtextStyle: { fontSize: 13, color: '#64748B' },
    padding: [0, 0, 16, 0]
  },
  legend: {
    bottom: 0, textStyle: { color: '#64748B', fontSize: 12 },
    itemGap: 24, itemWidth: 12, itemHeight: 12, icon: 'roundRect'
  },
  tooltip: {
    backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderWidth: 1,
    textStyle: { color: '#1E293B', fontSize: 13 },
    extraCssText: 'box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-radius: 6px;'
  },
  grid: { left: '3%', right: '4%', bottom: '14%', top: '18%', containLabel: true },
  xAxis: {
    axisLine: { lineStyle: { color: '#E2E8F0' } },
    axisTick: { show: false },
    axisLabel: { color: '#64748B', fontSize: 12 },
    splitLine: { show: false }
  },
  yAxis: {
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#64748B', fontSize: 12 },
    splitLine: { lineStyle: { color: '#F1F5F9', type: 'dashed' } }
  }
};
```

### 6.2 柱状图（Bar Chart）

| 属性 | 规范 |
|------|------|
| 柱体圆角 | `borderRadius: [4, 4, 0, 0]` |
| 柱宽 | 单系列 `barWidth: '40%'`，多系列自适应 |
| 柱体间距 | 组间距 `barGap: '30%'` |
| 数据标签 | 柱顶上方，`11px Medium`，颜色同系列色 |
| 渐变 | **禁用**，使用纯色 |

### 6.3 折线图（Line Chart）

| 属性 | 规范 |
|------|------|
| 线宽 | `2px` |
| 数据点 | `symbol: 'circle'`，`symbolSize: 6`，填充白色，边框同系列色 `2px` |
| 面积填充 | `areaStyle: { opacity: 0.06 }`（极淡） |
| 平滑 | `smooth: false`（直线连接），除非数据趋势需要平滑 |

### 6.4 饼图（Pie / Donut Chart）

| 属性 | 规范 |
|------|------|
| 类型 | 环形图（donut）：内半径 `45%`，外半径 `72%` |
| 扇区间距 | `padAngle: 2` |
| 标签 | 外侧标签，引导线颜色 `#CBD5E1` |
| 中心文字 | 标题 `16px Bold`，数值 `28px Bold` |

### 6.5 雷达图（Radar Chart）

| 属性 | 规范 |
|------|------|
| 轴线 | `#E2E8F0` |
| 分割线 | `#F1F5F9` |
| 分割区域 | 交替 `#FFFFFF` / `#F8FAFC` |
| 数据填充 | `areaStyle: { opacity: 0.1 }` |
| 数据线宽 | `2px` |
| 数据点 | `symbolSize: 5`，实心 |

### 6.6 热力图（Heatmap）

| 属性 | 规范 |
|------|------|
| 色阶 | 从 `#EFF6FF` 到 `#1E40AF`（Blue 浅→深） |
| 单元格间距 | `2px`（白色间隙） |
| 单元格圆角 | `2px` |
| 数值标注 | 浅底用深色文字，深底用白色文字 |

### 6.7 桑基图（Sankey Diagram）

| 属性 | 规范 |
|------|------|
| 节点宽度 | `16px` |
| 节点颜色 | 使用主题色序列 |
| 流带颜色 | 来源节点色 + `opacity: 0.3` |
| 标签 | 节点右侧，`12px`，颜色 `#1E293B` |

---

## 七、输出规范

### 7.1 尺寸

| 图表类型 | 宽度 | 高度 | 缩放 |
|---------|------|------|------|
| 统计图（柱/线/散点） | 800px | 500px | 2x |
| 饼图/雷达图 | 600px | 600px | 2x |
| 热力图 | 800px | 自适应 | 2x |
| 流程图/时序图/状态图 | 自适应 | 自适应 | 2x |
| 架构图/泳道图 | 960px | 自适应 | 2x |
| ER 图/关系图 | 自适应 | 自适应 | 2x |

### 7.2 格式

- 输出：PNG（统一格式）
- 背景：白色（`#FFFFFF`）
- 内边距：四周至少 `24px` 留白
- 文件命名：`<图表类型>-<描述>.png`（英文小写 + 连字符）

---

## 八、跨工具配置映射

### 8.1 D2

```
# 使用 --theme 0 (Neutral Default) + 自定义 style
d2 --theme 0 --pad 40 input.d2 output.png
```

关键覆盖项：节点 fill/stroke、连线 stroke、font-size、border-radius。

### 8.2 Mermaid

```
%%{init: {'theme':'base','themeVariables':{
  'primaryColor':'#EFF6FF','primaryBorderColor':'#93C5FD','primaryTextColor':'#1E293B',
  'secondaryColor':'#ECFDF5','secondaryBorderColor':'#6EE7B7',
  'tertiaryColor':'#FFFBEB','tertiaryBorderColor':'#FCD34D',
  'lineColor':'#94A3B8','textColor':'#1E293B','fontSize':'13px',
  'fontFamily':'PingFang SC, Inter, sans-serif'
}}}%%
```

### 8.3 ECharts

使用第六章定义的全局主题对象，通过 `echarts.registerTheme('design-system', THEME)` 注册。

### 8.4 HTML/SVG

使用第一章定义的 CSS 变量，所有 HTML 图表模板引用同一份 CSS 变量文件。

```css
:root {
  --c-bg: #FFFFFF;  --c-surface: #F8FAFC;  --c-surface-alt: #F1F5F9;
  --c-border: #E2E8F0;  --c-border-light: #CBD5E1;
  --c-text: #1E293B;  --c-text-secondary: #64748B;  --c-text-heading: #0F172A;
  --c-blue: #3B82F6;  --c-blue-light: #EFF6FF;  --c-blue-mid: #93C5FD;  --c-blue-dark: #1E40AF;
  --c-emerald: #10B981;  --c-emerald-light: #ECFDF5;  --c-emerald-mid: #6EE7B7;  --c-emerald-dark: #065F46;
  --c-amber: #F59E0B;  --c-amber-light: #FFFBEB;  --c-amber-mid: #FCD34D;  --c-amber-dark: #92400E;
  --c-rose: #F43F5E;  --c-rose-light: #FFF1F2;  --c-rose-mid: #FDA4AF;  --c-rose-dark: #9F1239;
  --c-violet: #8B5CF6;  --c-violet-light: #F5F3FF;  --c-violet-mid: #C4B5FD;  --c-violet-dark: #5B21B6;
  --c-cyan: #06B6D4;  --c-cyan-light: #ECFEFF;  --c-cyan-mid: #67E8F9;  --c-cyan-dark: #155E75;
  --c-orange: #F97316;  --c-orange-light: #FFF7ED;  --c-orange-mid: #FDBA74;  --c-orange-dark: #9A3412;
  --c-slate: #64748B;  --c-slate-light: #F8FAFC;  --c-slate-mid: #CBD5E1;  --c-slate-dark: #334155;
  --radius-sm: 4px;  --radius-md: 6px;  --radius-lg: 8px;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);  --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
  --font-sans: 'PingFang SC','Inter',-apple-system,sans-serif;
  --font-mono: 'JetBrains Mono','SF Mono',monospace;
}
```

---

## 九、质量自检清单

每张图生成后，对照检查：

- [ ] **配色**：所有色值来自调色板，不使用调色板外的颜色
- [ ] **组件**：节点形状、连线类型符合基础组件库定义
- [ ] **文字**：字体、字号、字重符合层级规范
- [ ] **对比度**：文字与背景对比度 ≥ 4.5:1
- [ ] **连线**：线宽 1.5px，颜色 N-5，直角折线，锚点居中
- [ ] **间距**：元素间距遵循 4px 网格，不拥挤不松散
- [ ] **圆角**：节点 6px，容器 8px
- [ ] **流向**：符合图表类型的默认流向
- [ ] **留白**：四周至少 24px padding
- [ ] **一致性**：同一报告内的多张图视觉统一
- [ ] **可读性**：缩小到 50% 仍能辨认主要信息
- [ ] **节点数量**：不超过该图表类型的上限
