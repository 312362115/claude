# 分析框架索引

> 调研第三步（分析与结论形成）时查阅本文件，选择合适的分析框架。
> 各框架的操作步骤、产出格式、常见误用见 `references/frameworks/` 目录下的独立文件。

---

## 一、通用底座速查表

| 分析需求 | 推荐框架 | 核心产出 | 常见误用 | 详见 |
|---------|---------|---------|---------|------|
| 宏观环境扫描 | PESTEL | 关键驱动因素 + 机会/威胁清单 | 沦为列清单，未落到对行业的具体影响 | [general.md](general.md) |
| 行业结构评估 | 波特五力 | 行业吸引力评分 + 利润分配判断 | 忽略互补品和平台效应 | [general.md](general.md) |
| 行业阶段判断 | 行业生命周期 | 所处阶段 + 对应策略建议 | 仅凭增长率判断，忽略结构性变化信号 | [general.md](general.md) |
| 产业链理解 | 价值链分析 | 产业链图 + 利润池分布 | 过于抽象，不落到具体环节和参与者 | [general.md](general.md) |
| 市场规模测算 | TAM/SAM/SOM | 市场天花板 + 可获取空间 | 自上而下拍 TAM，不做自下而上验证 | [general.md](general.md) |
| 竞争格局分析 | CR5/HHI + 战略组图 | 竞争态势 + 玩家定位 | 只看市场份额不看变化趋势 | [general.md](general.md) |
| 数据缺失时估算 | 费米估算 | 量级判断 + 不确定性范围 | 假设不透明，未标注关键假设的敏感性 | [general.md](general.md) |

### 标准分析流程

```
PESTEL → 行业生命周期 → 价值链 → 波特五力 → TAM/SAM/SOM → 竞争格局 → 趋势预判
```

| 深度 | 使用的框架 | 适用场景 |
|------|----------|---------|
| **快速摸底** | PESTEL(简) + 竞争格局 + 趋势 | 初步了解、快速判断 |
| **标准调研** | 全流程 | 技术选型、竞品分析 |
| **深度研究** | 全流程 + 每个框架深度展开 | 行业进入决策、投资决策 |

---

## 二、互联网执行层表

| 职能 | 核心框架 | 核心产出 | 详见 |
|------|---------|---------|------|
| **产品** | KANO、RICE、北极星、用户故事地图 | 需求优先级、产品路线图 | [internet-product.md](internet-product.md) |
| **技术** | ATAM、C4、选型矩阵、ADR、USE | 架构决策记录、选型建议 | [internet-tech.md](internet-tech.md) |
| **设计** | HEART、Nielsen 启发式、Design Sprint | UX 审计报告、设计改进建议 | [internet-design.md](internet-design.md) |
| **测试** | 测试金字塔、敏捷测试象限、质量度量 | 质量现状评估、改进路径 | [internet-testing.md](internet-testing.md) |
| **运营** | AARRR、RFM、用户生命周期、北极星+OSM | 运营分析报告、增长策略 | [internet-ops.md](internet-ops.md) |
| **市场** | STP、4P、PESO、品牌健康度 | 市场策略建议、品牌评估 | [internet-marketing.md](internet-marketing.md) |

---

## 三、互联网决策层表

| 场景 | 核心框架 | 触发词 | 核心产出 | 详见 |
|------|---------|-------|---------|------|
| **创业机会评估** | TAM-SAM-SOM、Thiel 七问、PMF | 赛道、创业、立项 | 机会评估报告 | [internet-startup.md](internet-startup.md) |
| **商业模式分析** | 商业模式画布、单元经济学、收入模型 | 商业模式、盈利、变现 | 商业模式拆解 | [internet-bizmodel.md](internet-bizmodel.md) |
| **战略决策** | 五力、McKinsey 7S、Ansoff、BCG | 战略、怎么赢、方向 | 战略选择建议 | [internet-strategy.md](internet-strategy.md) |
| **业务健康度** | a16z 16 指标、Sacks SaaS、Cohort | 健康度、诊断、体检 | 健康度仪表盘 | [internet-health.md](internet-health.md) |
| **融资与估值** | VC 估值法、Comps、Berkus | 估值、融资、BP | 估值区间 | [internet-fundraising.md](internet-fundraising.md) |
| **竞争战略** | 护城河、蓝海、颠覆式创新、飞轮 | 竞争、壁垒、护城河 | 竞争战略建议 | [internet-competition.md](internet-competition.md) |

---

## 四、金融投资表

| 领域 | 核心分析框架 | 核心估值方法 | 关键数据平台 | 详见 |
|------|------------|------------|------------|------|
| **A 股** | 宏观驱动、景气度、行业轮动 | PE/PB/PEG/DCF | Wind/Choice/东方财富 | [finance-a-share.md](finance-a-share.md) |
| **美股** | 基本面、DCF、Comps | DCF + Comps（Football Field） | Bloomberg/SEC EDGAR/Finviz | [finance-us-stock.md](finance-us-stock.md) |
| **港股** | AH 溢价、流动性双驱动、老千股识别 | 通用 + NAV 折让 + 股息率 | 港交所披露易/AAStocks | [finance-hk-stock.md](finance-hk-stock.md) |
| **加密货币** | 链上分析、叙事周期、代币经济学 | NVT/MVRV/S2F/协议 P/S | Glassnode/Dune/DeFiLlama | [finance-crypto.md](finance-crypto.md) |
| **固收/债券** | 利率分析、信用五维度、久期凸性 | YTM/信用利差/OAS | 中债信息网/Wind | [finance-bond.md](finance-bond.md) |
| **基金** | Brinson 归因、因子归因、风格箱 | Sharpe/IR/Calmar/最大回撤 | 天天基金/晨星/Wind | [finance-fund.md](finance-fund.md) |

---

## 五、分析视角选择

| 视角 | 触发词 | 核心问题 | 时间尺度 | 产出重点 |
|------|-------|---------|---------|---------|
| **券商/分析师** | 估值、值不值得买、目标价 | "值多少钱？" | 6-12 个月 | 估值 + 目标价 + 投资评级 |
| **咨询/战略** | 怎么做、战略、进入、优化 | "怎么赢？" | 3-5 年 | 战略选择 + 实施路径 |
| **VC/创业** | 赛道、创业、融资、机会 | "能不能 10x？" | 5-10 年 | 市场规模 + 壁垒 + 增长飞轮 |

**默认**：不确定时用咨询视角（最通用）。

---

## 六、框架自动选择规则

**输入**：调研类型 + 行业关键词 + 用户角色/目的

**选择逻辑**：
1. 根据调研类型，从通用底座中选择 2-3 个最相关的框架
2. 识别行业关键词 → 如果命中互联网/金融，叠加特化框架
3. 根据调研深度（快速/标准/深度）决定框架展开程度
4. 根据分析视角调整产出重点

| 调研类型 | 推荐的通用底座框架 |
|---------|----------------|
| 技术选型 | 价值链 + 费米估算 |
| 行业分析 | 全套：PESTEL → 生命周期 → 价值链 → 五力 → TAM → 竞争格局 |
| 竞品分析 | 竞争格局 + 价值链 |
| 可行性探索 | TAM/SAM/SOM + 费米估算 |
