# 本地数据栈对接（可选增强）

> ⚠️ **定位**：本对接属于 **skill 的可选增强**，不是前置条件。
>
> **没有量化栈**：skill 通过 WebFetch 抓最近行情（Yahoo/雪球/AAStocks 网页），能完成 80% 的命题分析（财报+估值+产业链+决策卡全部能做）。
>
> **有量化栈**：skill 解锁剩余 20% 高阶能力（批量历史 K线 / 精确技术指标 / 快速同业对标 / 回测引擎）。
>
> skill 的**核心战斗力在方法论 + 读财报 + 独立推演**，不在是否有量化 API。

---

## Skill 能力两档

### Tier 1：基础能力（默认，Claude Code 原生）

**数据工具**：WebSearch + WebFetch

**能做**：
- ✅ 读 10-K / 10-Q / 8-K / 招股书 全文
- ✅ 读电话会文字稿 / IR PPT
- ✅ 读行业分析（信通院/艾瑞/TrendForce）
- ✅ 当前股价快照（延迟 15 分钟+）
- ✅ 最近 1-3 个月 K线（粗略）
- ✅ 手工拼同业估值对标
- ✅ 产业链推演（≥2 跳）
- ✅ 透过表象找里层信号
- ✅ 输出完整决策卡

**做不了**（或做得慢 / 粗）：
- 批量历史 K线（几年级别）
- 精确技术指标（MACD / RSI / 布林带）
- 跨 100+ 标的快速筛选
- 回测策略
- 实时 tick 数据

### Tier 2：增强能力（可选，需对接本地数据栈）

**数据工具**：本地 PG + Python 量化库 + 行情同步服务

**解锁**：
- 🚀 批量历史 K线（年级别）
- 🚀 精确技术指标全家桶
- 🚀 一键同业对标（PG 查询毫秒级）
- 🚀 回测引擎（验证策略）
- 🚀 Post-Earnings Drift 自动统计
- 🚀 Layer/主题成员快速筛选

**重点**：Tier 2 是**加速 + 增强**，不改变 skill 核心方法论。用户可以**完全不做** Tier 2，skill 仍然值得用。

---

---

## 架构三层

```
┌─────────────────────────────────────────┐
│  Skill 层（Claude Code）                  │
│  方法论 + prompt + 决策卡输出              │
│  通过 Bash 调接口层                        │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  接口层（用户实现）                        │
│  CLI 工具 / psql / MCP Server             │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  数据层（用户已有）                        │
│  Postgres + 行情同步服务 + 文件系统        │
└─────────────────────────────────────────┘
```

**职责分离**：
- **数据层**：抓取 + 存储（用户负责）
- **接口层**：暴露统一 API（用户实现）
- **Skill 层**：方法论 + 分析 + 决策（skill 提供）

---

## 两种对接方式（选一或混用）

### 方式 1：CLI 工具（推荐）

用户实现一个 `fa-data` 命令（或任何名字），提供标准输出（JSON）。

**优点**：解耦、易测试、可换实现（今天 yfinance 明天 Polygon）
**缺点**：需要用户开发 + 维护

### 方式 2：直接 psql

skill 直接连 Postgres 查 SQL。

**优点**：零开发
**缺点**：schema 强耦合，查询逻辑散落

### 混合方式（实用）

- 常用查询 → CLI 工具（语义清晰）
- 临时定制查询 → psql（灵活）

---

## 接口定义（skill 需要的查询集）

### 通用约定

- 输出格式：JSON（stdout）
- 错误：非 0 退出码 + stderr 写错误信息
- 时区：UTC（避免混乱）
- 空数据：返回 `{"data": [], "warning": "no data"}` 而非 error

### 套路 A 个股分析 需要

#### A.1 K线

```bash
fa-data kline <ticker> [--days N] [--interval 1d|1h|5m] [--format ohlcv|close-only]

# 输出
{
  "ticker": "AAPL",
  "interval": "1d",
  "data": [
    {"ts": "2026-04-20", "o": 180.5, "h": 182.3, "l": 179.1, "c": 181.5, "v": 45000000},
    ...
  ]
}
```

#### A.2 基本面历史时序

```bash
fa-data fundamentals <ticker> [--history 5y|3y|1y] [--freq quarterly|annual]

# 输出
{
  "ticker": "AAPL",
  "frequency": "quarterly",
  "data": [
    {
      "fiscal_quarter": "2026-Q1",
      "revenue": 1.2e11,
      "net_income": 3e10,
      "gross_margin": 0.45,
      "r_and_d": 7e9,
      "capex": 3e9,
      "fcf": 2.5e10,
      "cash": 1.5e11,
      "total_debt": 1.1e11,
      ...
    }
  ]
}
```

**关键字段**（建议 schema）：营收 / 净利 / 毛利率 / 运营利润率 / R&D / CapEx / FCF / 应收 / 存货 / 合同负债 / 现金 / 总债务 / 股份总数 / EPS

#### A.3 最新财报关键字段

```bash
fa-data latest-report <ticker>

# 输出：最新一季财报 + 指引
{
  "ticker": "NVDA",
  "filing_date": "2026-05-22",
  "fiscal_quarter": "FY26-Q1",
  "actual": {"revenue": 26e9, "eps": 6.12, "gross_margin": 0.784},
  "consensus": {"revenue": 24.5e9, "eps": 5.60},
  "guidance_next_q": {"revenue": 28e9, "consensus_revenue": 26.8e9},
  "earnings_call_transcript_url": "https://...",
  "10q_url": "https://sec.gov/..."
}
```

#### A.4 同业对标

```bash
fa-data peers <ticker> [--limit 5]

# 输出：同业可比公司
{
  "ticker": "NVDA",
  "peers": [
    {"ticker": "AMD", "ttm_revenue": 25e9, "ttm_pe": 45, "ps": 10, "market_cap": 2.5e11},
    {"ticker": "INTC", ...},
    ...
  ]
}
```

可选：用户可以在 PG 里手工维护 `peer_groups` 表，或者用 GICS 分类自动匹配。

---

### 套路 C 事件驱动 需要

#### C.1 历史 Beat/Miss 规律

```bash
fa-data earnings-history <ticker> [--history 8q|12q]

# 输出
{
  "ticker": "NVDA",
  "history": [
    {"quarter": "FY26-Q1", "revenue_actual": 26e9, "revenue_guided": 24e9, "beat_pct": 0.083, "stock_reaction_1d": 0.06},
    {"quarter": "FY25-Q4", ...},
    ...
  ],
  "pattern": {
    "beat_rate": 0.875,
    "avg_beat_pct": 0.06,
    "sandbag_score": 0.8  # 0-1，越高越可能是沙袋策略
  }
}
```

#### C.2 财报后漂移（Post-Earnings-Announcement Drift）

```bash
fa-data post-earnings-drift <ticker> [--last-n 8]

# 输出：过去 N 次财报后 T+1/T+5/T+30 的股价表现
{
  "ticker": "NVDA",
  "drifts": [
    {"quarter": "FY26-Q1", "beat_pct": 0.083, "t+1": 0.06, "t+5": 0.11, "t+30": 0.18},
    ...
  ]
}
```

---

### 套路 D 主题赛道 需要

#### D.1 Layer / 概念成员列表

```bash
fa-data industry-members [--layer ai-cpo|ai-power|ai-robotics] [--market us|hk|a-share]

# 输出
{
  "layer": "ai-cpo",
  "members": [
    {"ticker": "INNO.N", "name": "Innolight"},
    {"ticker": "300308.SZ", "name": "中际旭创"},
    ...
  ]
}
```

用户可在 PG 里维护 `industry_tags` 表。

#### D.2 板块资金流 / 涨跌分布

```bash
fa-data sector-flow [--layer ai-cpo] [--days 30]

# 输出：一段时间内该 Layer 成员的涨跌分布 + 资金流
```

---

## 简化版：直接 psql 查询

如果不想做 CLI 工具，skill 也可以直接 `psql` 查。需要约定 schema：

### 推荐 Schema

```sql
-- K线（OHLCV）
CREATE TABLE kline_daily (
  ticker VARCHAR(16) NOT NULL,
  ts DATE NOT NULL,
  open DECIMAL(16,4),
  high DECIMAL(16,4),
  low DECIMAL(16,4),
  close DECIMAL(16,4),
  volume BIGINT,
  adj_close DECIMAL(16,4),
  PRIMARY KEY (ticker, ts)
);
CREATE INDEX ON kline_daily (ticker, ts DESC);

-- 基本面（季度）
CREATE TABLE fundamentals_quarterly (
  ticker VARCHAR(16) NOT NULL,
  fiscal_quarter VARCHAR(16) NOT NULL,  -- "FY26-Q1"
  period_end DATE NOT NULL,
  revenue DECIMAL(20,2),
  net_income DECIMAL(20,2),
  gross_margin DECIMAL(6,4),
  operating_margin DECIMAL(6,4),
  r_and_d DECIMAL(20,2),
  capex DECIMAL(20,2),
  fcf DECIMAL(20,2),
  cash DECIMAL(20,2),
  total_debt DECIMAL(20,2),
  shares_outstanding BIGINT,
  eps DECIMAL(16,4),
  PRIMARY KEY (ticker, fiscal_quarter)
);

-- 财报披露元数据
CREATE TABLE earnings_events (
  ticker VARCHAR(16) NOT NULL,
  fiscal_quarter VARCHAR(16) NOT NULL,
  filing_date DATE,
  revenue_actual DECIMAL(20,2),
  revenue_consensus DECIMAL(20,2),
  eps_actual DECIMAL(16,4),
  eps_consensus DECIMAL(16,4),
  guidance_revenue_next_q DECIMAL(20,2),
  guidance_consensus DECIMAL(20,2),
  transcript_url TEXT,
  filing_url TEXT,
  PRIMARY KEY (ticker, fiscal_quarter)
);

-- Layer / 主题标签
CREATE TABLE industry_tags (
  ticker VARCHAR(16) NOT NULL,
  layer VARCHAR(32) NOT NULL,  -- 'ai-cpo', 'ai-power', ...
  weight DECIMAL(4,2),  -- 0-1，标的对该 Layer 的相关度
  PRIMARY KEY (ticker, layer)
);
```

### 常用 SQL 片段

```sql
-- 拿最近 90 天 K线
SELECT ts, close, volume
FROM kline_daily
WHERE ticker = 'AAPL' AND ts > current_date - interval '90 days'
ORDER BY ts;

-- 算 200 日均线
SELECT ts,
  AVG(close) OVER (ORDER BY ts ROWS BETWEEN 199 PRECEDING AND CURRENT ROW) AS ma200
FROM kline_daily
WHERE ticker = 'AAPL'
ORDER BY ts DESC
LIMIT 30;

-- 算成交量 vs 50 日均量
WITH vol_stats AS (
  SELECT ts, volume,
    AVG(volume) OVER (ORDER BY ts ROWS BETWEEN 49 PRECEDING AND 1 PRECEDING) AS ma50_vol
  FROM kline_daily
  WHERE ticker = 'AAPL' AND ts > current_date - interval '60 days'
)
SELECT ts, volume, ma50_vol, volume / ma50_vol AS vol_ratio
FROM vol_stats
WHERE ts > current_date - interval '7 days'
ORDER BY ts DESC;

-- 同业对标（基本面）
SELECT t.ticker, f.revenue, f.net_income, f.gross_margin
FROM industry_tags t
JOIN fundamentals_quarterly f ON t.ticker = f.ticker
WHERE t.layer = 'ai-cpo'
  AND f.fiscal_quarter = (SELECT MAX(fiscal_quarter) FROM fundamentals_quarterly)
ORDER BY f.revenue DESC;
```

---

## Skill 如何使用（Bash 约定）

skill 在 prompt 中被指示使用以下 Bash 命令：

```bash
# 环境变量约定
export FA_DB_URL="postgresql://user:pass@localhost:5432/quant"
export FA_TOOL_PATH="~/workspace/quant/bin/fa-data"
export FA_DATA_MODE="cli"  # cli | psql | both
```

Skill 内部逻辑：

```
1. 读取 FA_DATA_MODE 判断对接方式
2. cli 模式：调 $FA_TOOL_PATH 各子命令
3. psql 模式：用 psql -d $FA_DB_URL -c "SELECT ..."
4. 解析 JSON / 表格输出
5. 喂给 LLM 做分析
```

---

## 最小落地步骤（给用户）

### Step 1：PG schema 建好

```bash
psql -d your_db < schema.sql  # schema 见上
```

### Step 2：行情同步服务填充数据

你已有的服务继续跑，确保按约定 schema 写入。

### Step 3：实现 `fa-data` CLI（Python 示例骨架）

```python
# ~/workspace/quant/fa_data/cli.py
import click, psycopg2, json, os

@click.group()
def cli(): pass

@cli.command()
@click.argument('ticker')
@click.option('--days', default=90)
def kline(ticker, days):
    conn = psycopg2.connect(os.getenv('FA_DB_URL'))
    cur = conn.cursor()
    cur.execute("""
        SELECT ts, open, high, low, close, volume
        FROM kline_daily
        WHERE ticker = %s AND ts > current_date - interval '%s days'
        ORDER BY ts
    """, (ticker, days))
    rows = cur.fetchall()
    print(json.dumps({
        "ticker": ticker,
        "interval": "1d",
        "data": [
            {"ts": str(r[0]), "o": float(r[1]), "h": float(r[2]),
             "l": float(r[3]), "c": float(r[4]), "v": int(r[5])}
            for r in rows
        ]
    }))

# 其他子命令类似：fundamentals, latest-report, peers, earnings-history, ...

if __name__ == '__main__':
    cli()
```

### Step 4：设置环境变量

```bash
# ~/.zshrc 或 .env
export FA_DB_URL="postgresql://..."
export FA_TOOL_PATH="python ~/workspace/quant/fa_data/cli.py"
```

### Step 5：测试 skill 能调

```bash
$FA_TOOL_PATH kline AAPL --days 30 | jq .
```

通过 → skill 可用。

---

## 版本路线

| 版本 | 内容 |
|------|------|
| v0（当前） | 约定接口 + schema 建议 + psql 兜底 |
| v1 | 用户实现 `fa-data` CLI 基础命令（kline / fundamentals / latest-report） |
| v2 | 补 earnings-history / post-earnings-drift / peers |
| v3 | 补 industry-members / sector-flow / layer 聚合 |
| v4（可选） | 包装成 MCP Server（更丝滑，可被 Claude Code 直接调用） |

---

## 相关

- 数据源白名单：`~/.claude/skills/deep-research/references/sources/finance.yaml`（量化 API 子域）
- rss 一手新闻：`~/workspace/rss/daily/` （SEC / HKEX / IR 等推送）
- 行情同步服务：`~/workspace/quant/`（你已有）

## 诚实 disclaimer

- 本契约 v0 只是**约定**，skill 没有强制用户必须实现所有命令
- 没实现的命令 skill 会 fallback 到 WebFetch 公开数据（慢但能用）
- 用户可以**渐进实现**：先做 kline + fundamentals，后面按需补
