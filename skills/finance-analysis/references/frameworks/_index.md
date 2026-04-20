# Frameworks 路由表

> SKILL.md 触发后，根据命题关键词路由到对应 framework。

## 已落地（0.1.0）

| Framework | 适用场景 | 关键词触发 |
|-----------|---------|-----------|
| [hk-ipo-arbitrage.md](./hk-ipo-arbitrage.md) | 港股 IPO 首日套利 | 打新、IPO、孖展、暗盘、港股新股 |
| [alpha-generation.md](./alpha-generation.md) | 10x 股 + 顶级 IPO 早期捕捉 | 10 倍股、中长期机会、大牛股、Alpha |
| [ai-thematic-investing.md](./ai-thematic-investing.md) | AI 革命主题投资 + 趋势启动识别 | AI 投资、英伟达、CPO、具身智能、空间智能、大模型投资 |

## 占位扩展（TODO，按需迭代）

### 估值类
| Framework | 场景 | 版本目标 |
|-----------|------|---------|
| valuation-relative.md | 相对估值（PE/PS/PB 对标同业） | 0.2.0 |
| valuation-dcf.md | DCF 估值（成长股 / 现金流折现） | 0.2.0 |

### 选股 / 选基类
| Framework | 场景 | 版本目标 |
|-----------|------|---------|
| stock-selection.md | 选股（赛道 + 龙头 + 质量 + 成长） | 0.2.0 |
| fund-analysis.md | 基金分析（夏普 / 回撤 / 持仓归因） | 0.3.0 |

### 事件 / 技术面
| Framework | 场景 | 版本目标 |
|-----------|------|---------|
| event-driven.md | 财报 / 政策 / 并购事件交易 | 0.4.0 |
| technical.md | 技术面（支撑压力 / 趋势 / 量价） | 0.4.0 |

### 债券 / 宏观
| Framework | 场景 | 版本目标 |
|-----------|------|---------|
| bond-analysis.md | 债券（久期 / 信用 / 利差） | 0.3.0 |
| macro-overlay.md | 宏观择时（利率 / 汇率 / 大宗） | 0.4.0 |

### 美股 / 加密
| Framework | 场景 | 版本目标 |
|-----------|------|---------|
| us-ipo-arbitrage.md | 美股 IPO 规则（不同于港股） | 0.2.0 |
| crypto-thematic.md | 加密货币主题投资 | 0.5.0 |

## 路由规则

Lead agent 接到命题时：

1. **匹配关键词** → 加载对应 framework
2. **跨 framework 组合**（一个命题可能触发多个）：
   - "港股打新 + 中长期持有" → `hk-ipo-arbitrage` + `alpha-generation`
   - "AI 选股 + 估值分析" → `ai-thematic-investing` + `valuation-relative`
   - "MiniMax / Zhipu IPO 分析" → `hk-ipo-arbitrage` + `alpha-generation` + `ai-thematic-investing`
3. **未匹配**（框架缺失）→ fallback 到 `alpha-generation.md` 的通用方法论

## Framework 写作规范（新增 framework 时遵循）

每个 framework 必须包含：

1. **核心定位**：适用 / 不适用场景
2. **决策树**：末端是可执行动作，不是"完整理解"
3. **量化信号**：每个节点是可观测阈值（不是主观判断）
4. **EV 或评分计算**：至少有一个数学模型
5. **执行纪律**：最容易翻车的环节写清楚
6. **Worked Example**：至少 1 个真实案例验证
7. **失效场景**：何时这套方法不适用
8. **相关 template**：决策卡 / 监控表指向 `templates/`
9. **诚实 disclaimer**：方法论不等于预测

**长度**：一个 framework 应 800-1500 行（过短不深入，过长读者退出）。

## 优先级说明

**0.2.0 最优先落地**：
- `valuation-relative.md`（所有选股必备）
- `stock-selection.md`（alpha-generation 的可执行简化版）

**不做**：
- 日内技术分析（和决策导向定位不符）
- 期权策略（本 skill 专注股票/债券/基金/IPO）
