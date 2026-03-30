# 美股分析框架

> 调研涉及美股投资分析时使用。

## 核心分析框架

### 基本面分析

- **适用场景**：中长期投资、价值投资
- **核心指标**：EPS 增速、ROE、ROIC（> WACC 为价值创造）、FCF Yield（> 5% 为高）、Interest Coverage（< 3x 警惕）

### DCF 内在价值

- **适用场景**：所有有正现金流的成熟企业
- **操作步骤**：
  1. 预测未来 5-10 年自由现金流（FCFF 或 FCFE）
  2. 确定折现率（WACC，通常 8-12%）
  3. 计算终值（永续增长法或退出倍数法）
  4. 折现求和得到企业价值，减净债务得股权价值
- **关键注意**：终值通常占总价值 60-80%，WACC 和永续增长率微小变化显著影响结果

### 可比公司分析（Comps）

- **适用场景**：快速估值、IPO 定价
- **操作步骤**：选取 5-10 家可比公司 → 计算 EV/EBITDA、P/E、P/S 等倍数 → 取中位数作基准 → 应用于目标公司

### GARP

- **核心**：PEG = P/E / EPS Growth Rate。< 1 低估，1-1.5 合理，> 2 可能过高

## 估值方法（按行业）

| 行业 | 首选方法 | 辅助方法 |
|------|---------|---------|
| 科技（SaaS） | EV/Revenue、Rule of 40 | DCF |
| 消费品 | P/E、EV/EBITDA | DCF |
| 金融 | P/B、P/E | DDM |
| 医药/生物 | Pipeline DCF（rNPV） | EV/Revenue |
| 能源 | EV/EBITDA、NAV | DCF |
| REIT | P/AFFO、Cap Rate | NAV |

**Football Field Chart**：多种估值方法结果放在同一张横向柱状图，展示估值区间
**Bull/Base/Bear 三情景**：分别给出乐观/基准/悲观目标价和概率加权

**推理链**：行业趋势(TAM) → 公司护城河 → 财务模型 → 估值(DCF+Comps交叉) → 催化剂 → 风险收益比 → 仓位

## 典型研报骨架

```
Cover Page: Rating + Price Target
Executive Summary（1页）：评级、核心论点(3-5条)、财务快照
I. Company Overview（业务/管理层/行业定位）
II. Industry Analysis（TAM/竞争格局/趋势）
III. Investment Thesis（Bull/Base/Bear + 催化剂 + 护城河）
IV. Financial Analysis（Revenue Build/Margin/三表模型）
V. Valuation（DCF敏感度表 + Comps + Football Field）
VI. Risks（量化 Bear case）
```

## 数据来源

### 核心平台
- **SEC EDGAR**：10-K/10-Q/8-K/S-1（免费）
- **Bloomberg**：全品种实时行情+分析（~$24,000/年）
- **Yahoo Finance / Finviz**：基础行情+筛选（免费）
- **Seeking Alpha**：研报+投资者讨论

### 另类数据
- 信用卡交易数据（预判零售营收）、App 下载量（预判 MAU）
- 卫星图像（零售/油罐库存）、社交媒体情绪、职位招聘数据
- 65% 对冲基金已使用另类数据，可贡献约 3% 年化超额收益

## 风险分析要点

| 风险类型 | 评估工具 |
|---------|---------|
| 利率风险（Fed 政策） | Fed Funds Futures、CME FedWatch |
| 做空风险 | Short Interest > 20% 警惕 |
| 反垄断风险 | FTC/DOJ 执法动态 |
| ESG 风险 | MSCI ESG Rating |

**宏观传导**：Fed 加息 → 国债收益率↑ → 成长股贴现率↑ → 高估值承压；美元走强 → 跨国企业海外收入缩水
