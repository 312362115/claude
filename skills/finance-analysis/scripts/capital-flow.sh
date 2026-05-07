#!/usr/bin/env bash
# 资金面分析数据源速查工具（capital-flow framework 配套脚本）
#
# 用途：
#   1. 尝试抓基础信息（总股本 / 流通股本 / 流通市值 / 换手率 / PE / PB）
#   2. 列出 5 维资金面数据的官方查询 URL（手工填决策卡用）
#   3. 决策卡资金面附录 JSON schema 模板提示
#
# 设计原则（0.4.1）：
#   - 零依赖：bash + curl + python3（macOS / Linux 自带）
#   - 优雅降级：接口故障时仍输出 URL 速查列表
#   - 不强求全自动：手工抓取是合理 fallback，不是 framework 失败
#
# 数据源：
#   - 主：sina hq.sinajs.cn（实时行情，已知稳定）
#   - 辅：eastmoney push2（基础信息，可能被反爬）
#
# 用法：
#   bash scripts/capital-flow.sh sz301486
#   bash scripts/capital-flow.sh sh600519

set -eo pipefail

if [ $# -ne 1 ]; then
  echo "用法：bash $0 <code>" >&2
  echo "示例：bash $0 sz301486" >&2
  exit 1
fi

input_code=$1
prefix=${input_code:0:2}
code=${input_code:2}

case $prefix in
  sz) secid="0.$code" ;;
  sh) secid="1.$code" ;;
  *)  echo "错误：不支持的市场前缀 '$prefix'。仅支持 sz / sh。" >&2; exit 2 ;;
esac

today=$(date +%Y-%m-%d)
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  capital-flow framework 数据速查 — $input_code @ $today"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# === 1. 实时行情（主数据源：sina）===

echo "📊 实时行情（数据源：sina hq.sinajs.cn）"
echo ""

sina_raw=$(curl -s --max-time 10 -A "$UA" -H "Referer: https://finance.sina.com.cn" \
  "http://hq.sinajs.cn/list=${input_code}" 2>/dev/null | iconv -f GBK -t UTF-8 2>/dev/null || echo "")

if [ -n "$sina_raw" ] && echo "$sina_raw" | grep -q '="[^"]'; then
  python3 <<EOF
content = '''$sina_raw'''.split('"')[1] if '"' in '''$sina_raw''' else ''
if content:
    p = content.split(',')
    if len(p) >= 32:
        name = p[0]
        prev = float(p[2]) if p[2] else 0
        price = float(p[3]) if p[3] else 0
        date = p[30]
        chg = (price - prev) / prev * 100 if prev else 0
        print(f"   名称：{name}")
        print(f"   当前价：{price:.2f} ({chg:+.2f}%)  前收：{prev:.2f}")
        print(f"   数据时点：{date} {p[31]}")
EOF
else
  echo "   ⚠️ sina 接口返回空，跳过实时行情"
fi
echo ""

# === 2. 基础信息（辅数据源：eastmoney，best-effort）===

echo "🏷️  基础信息（数据源：eastmoney push2，best-effort）"
echo ""

em_raw=""
for attempt in 1 2 3; do
  em_raw=$(curl -s --max-time 8 -A "$UA" -H "Referer: https://quote.eastmoney.com/" \
    "http://push2.eastmoney.com/api/qt/stock/get?secid=${secid}&fields=f43,f47,f57,f58,f60,f84,f85,f116,f117,f167,f168,f170" \
    2>/dev/null || echo "")
  if [ -n "$em_raw" ] && echo "$em_raw" | grep -q '"data"'; then
    break
  fi
  sleep 2
done

if [ -n "$em_raw" ] && echo "$em_raw" | grep -q '"f84"'; then
  python3 <<EOF
import json
raw = '''$em_raw'''
try:
    j = json.loads(raw)
    d = j.get('data') or {}
    if d:
        total_share = (d.get('f84') or 0) / 1e8
        float_share = (d.get('f85') or 0) / 1e8
        total_mcap = (d.get('f116') or 0) / 1e8
        float_mcap = (d.get('f117') or 0) / 1e8
        pe = (d.get('f47') or 0) / 100
        pb = (d.get('f167') or 0) / 100
        turnover = (d.get('f168') or 0) / 100
        float_ratio = float_share / total_share * 100 if total_share else 0

        print(f"   总股本：{total_share:.4f} 亿股  /  流通股本：{float_share:.4f} 亿股  /  流通比：{float_ratio:.1f}%")
        print(f"   总市值：{total_mcap:.2f} 亿  /  流通市值：{float_mcap:.2f} 亿")
        print(f"   PE：{pe:.2f}  /  PB：{pb:.2f}  /  换手率：{turnover:.2f}%")
        print()

        # C_smallcap 标签快判
        if float_mcap <= 50:
            tag = f"流通市值 {float_mcap:.0f} 亿 ≤ 50 亿 → 极小盘（5 亿资金可控盘）✅ C_smallcap 强触发"
        elif float_mcap <= 100:
            tag = f"流通市值 {float_mcap:.0f} 亿 ≤ 100 亿 → 小盘 ✅ C_smallcap 触发"
        elif float_mcap <= 200:
            tag = f"流通市值 {float_mcap:.0f} 亿 ≤ 200 亿 → 中小盘（边界）⚠️ C_smallcap 弱触发"
        else:
            tag = f"流通市值 {float_mcap:.0f} 亿 > 200 亿 → ❌ C_smallcap 不应触发"
        print(f"   🏷️  {tag}")

        if float_ratio < 50:
            print(f"   ⚠️  流通比 {float_ratio:.1f}% < 50% → 高限售比例（次新股常见），关注解禁日程")
except Exception as e:
    print(f"   ⚠️ 解析异常：{e}")
EOF
else
  echo "   ⚠️ eastmoney 接口暂时不可达（可能反爬限流），手工查询：http://stockpage.10jqka.com.cn/${code}/"
fi
echo ""

# === 3. 5 维官方数据源 URL 列表（核心功能）===

echo "🔗 5 维资金面数据源（手工抓取速查）"
echo ""
echo "   【1. 龙虎榜】（C_smallcap 必看）"
if [ "$prefix" = "sz" ]; then
  echo "      深交所：https://www.szse.cn/disclosure/margin/margin/index.html"
else
  echo "      上交所：http://www.sse.com.cn/disclosure/diclosure/announcement/"
fi
echo "      东财（推荐，含席位明细）：https://data.eastmoney.com/stock/lhb/${code}.html"
echo ""
echo "   【2. 北上 / 沪深股通持仓】（机构动向）"
echo "      港交所 CCASS：https://www3.hkexnews.hk/sdw/search/searchsdw_c.aspx"
echo "      东财（持仓变动）：https://data.eastmoney.com/hsgtcg/StockHdDetail/${code}.html"
echo "      同花顺 F10：http://q.10jqka.com.cn/sgcg/?code=${code}"
echo ""
echo "   【3. 融资余额】（杠杆资金）"
echo "      东财数据中心：https://data.eastmoney.com/rzrq/detail/${code}.html"
echo "      同花顺 F10：http://stockpage.10jqka.com.cn/${code}/finance/"
echo ""
echo "   【4. 大宗交易】（折溢价 + 受让方）"
echo "      东财：https://data.eastmoney.com/dzjy/detail/${code}.html"
echo "      ⚠️  铁律：大宗成交价 ≠ 真实股价（沪电案例）"
echo ""
echo "   【5. 流通股本 / 限售解禁】（抛压窗口）"
echo "      巨潮资讯（公告）：http://www.cninfo.com.cn/new/disclosure/stock?stockCode=${code}"
echo "      同花顺 F10 股本结构：http://stockpage.10jqka.com.cn/${code}/holder/"
echo "      东财解禁日历：https://data.eastmoney.com/dxf/q/${code}.html"
echo ""

# === 4. 决策卡 JSON schema 占位 ===

cat <<'EOF'
═══════════════════════════════════════════════════════════════
  下一步：用上述数据填决策卡 capital_flow JSON 字段（手工）
═══════════════════════════════════════════════════════════════

参考 `references/frameworks/capital-flow.md` §8 资金面附录 JSON schema：

```json
{
  "capital_flow": {
    "circulation_market_cap_yi": <填流通市值>,
    "control_score": <0-100，5 维加权后>,
    "control_level": "high | medium | low",
    "main_direction_scores": {
      "longhubang": <±30>,
      "northbound": <±25>,
      "margin": <±25>,
      "block_trade": <±20>
    },
    "main_direction_total": <总分 ±100>,
    "main_direction_label": "strong_buy | mod_buy | neutral | mod_sell | strong_sell",
    "anomaly_level": "strong | medium | weak | none",
    "ev_modifier": <0.5-1.5>,
    "ev_modifier_horizon_days": <≤ 30>,
    "operation_recommendation": "buy | follow | observe | exit | skip"
  }
}
```

完整定义见 `references/frameworks/capital-flow.md`。
EOF
