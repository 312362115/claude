#!/usr/bin/env bash
# 实时行情批量抓取（铁律 0 股价时点校准工具）
#
# 用途：绕开 WebSearch 片段里的历史股价，直抓实时行情并带日期时间戳。
# 数据源：新浪财经行情接口 hq.sinajs.cn（零依赖 / 免 API key）
#
# 用法：
#   bash scripts/quote.sh sz002463 sh601985 rt_hk00068 gb_nvda
#
# 代码前缀：
#   sz      深市 A 股（例：sz002463 沪电股份、sz300308 中际旭创）
#   sh      沪市 A 股（例：sh601985 中国核电、sh600900 长江电力）
#   rt_hk   港股（例：rt_hk00068 群核科技、rt_hk00700 腾讯）
#   gb_     美股（例：gb_nvda、gb_googl）
#
# 输出：结构化表格（代码 / 名称 / 当前价 / 涨跌% / 时点 / 状态）
# 铁律 0：引用这些股价时必须标注此时点；数据未确认严禁引用。

set -eo pipefail

if [ $# -eq 0 ]; then
  echo "用法：bash $0 <code1> <code2> ..." >&2
  echo "示例：bash $0 sz002463 sh601985 rt_hk00068" >&2
  exit 1
fi

codes=$(IFS=,; echo "$*")

raw=$(curl -s --max-time 10 \
  -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Referer: https://finance.sina.com.cn" \
  "http://hq.sinajs.cn/list=${codes}" | iconv -f GBK -t UTF-8)

if [ -z "$raw" ]; then
  echo "错误：行情接口返回空" >&2
  exit 2
fi

today=$(date +%Y-%m-%d)

# 数据新鲜度判断：当日=实时/最新；1-3 天内=上一交易日收盘（正常）；>3 天=陈旧
judge_freshness() {
  local d="$1" t="$2"
  [ -z "$d" ] && { echo "⚠️ 时点缺失"; return; }
  if [ "$d" = "$t" ]; then
    echo "✅ 当日"
    return
  fi
  # 计算天数差（macOS date 和 Linux date 兼容写法）
  local d_epoch t_epoch diff
  d_epoch=$(date -j -f "%Y-%m-%d" "$d" "+%s" 2>/dev/null || date -d "$d" "+%s" 2>/dev/null || echo "")
  t_epoch=$(date -j -f "%Y-%m-%d" "$t" "+%s" 2>/dev/null || date -d "$t" "+%s" 2>/dev/null || echo "")
  if [ -z "$d_epoch" ] || [ -z "$t_epoch" ]; then
    echo "✅ $d"
    return
  fi
  diff=$(( (t_epoch - d_epoch) / 86400 ))
  if [ "$diff" -le 3 ] && [ "$diff" -ge 0 ]; then
    echo "✅ ${diff}天前收盘"
  elif [ "$diff" -lt 0 ]; then
    echo "✅ $d"
  else
    echo "⚠️ ${diff}天前（陈旧）"
  fi
}

printf "%-14s | %-12s | %-10s | %-8s | %-20s | %s\n" \
  "代码" "名称" "当前价" "涨跌%" "数据时点" "状态"
printf -- "-%.0s" {1..90}; echo ""

while IFS= read -r line; do
  [ -z "$line" ] && continue
  code=$(echo "$line" | sed -E 's/^var hq_str_([^=]+)=.*/\1/')
  content=$(echo "$line" | sed -E 's/^var hq_str_[^=]+="(.*)";$/\1/')

  if [ -z "$content" ]; then
    printf "%-14s | %-12s | %-10s | %-8s | %-20s | %s\n" \
      "$code" "UNKNOWN" "--" "--" "--" "❌ 代码无效"
    continue
  fi

  # --- 港股 rt_hk ---
  if [[ "$code" == rt_hk* ]]; then
    name=$(echo "$content" | awk -F, '{print $1}')
    price=$(echo "$content" | awk -F, '{print $7}')
    chg_pct=$(echo "$content" | awk -F, '{print $9}')
    date_raw=$(echo "$content" | awk -F, '{print $18}')
    time_raw=$(echo "$content" | awk -F, '{print $19}')
    date_fmt=$(echo "${date_raw:-}" | tr '/' '-')
    status=$(judge_freshness "$date_fmt" "$today")
    printf "%-14s | %-12s | %-10s | %-8s | %-20s | %s\n" \
      "$code" "${name:-UNKNOWN}" "${price:---}" "${chg_pct:---}%" "${date_fmt:---} ${time_raw:-}" "$status"
    continue
  fi

  # --- 美股 gb_ ---
  if [[ "$code" == gb_* ]]; then
    name=$(echo "$content" | awk -F, '{print $1}')
    price=$(echo "$content" | awk -F, '{print $2}')
    chg_pct=$(echo "$content" | awk -F, '{print $3}')
    date_raw=$(echo "$content" | awk -F, '{print $4}')
    printf "%-14s | %-12s | %-10s | %-8s | %-20s | %s\n" \
      "$code" "${name:-UNKNOWN}" "${price:---}" "${chg_pct:---}%" "${date_raw:---}" "美股"
    continue
  fi

  # --- A 股 sz/sh ---
  name=$(echo "$content" | awk -F, '{print $1}')
  prev=$(echo "$content" | awk -F, '{print $3}')
  price=$(echo "$content" | awk -F, '{print $4}')
  date_str=$(echo "$content" | awk -F, '{print $31}')
  time_str=$(echo "$content" | awk -F, '{print $32}')

  if [ -z "$price" ] || [ "$price" = "0.000" ]; then
    printf "%-14s | %-12s | %-10s | %-8s | %-20s | %s\n" \
      "$code" "${name:-UNKNOWN}" "--" "--" "--" "⚠️ 停牌或无效"
    continue
  fi

  chg_pct=$(awk -v p="$price" -v pc="$prev" 'BEGIN{if(pc>0)printf "%+.2f", (p-pc)/pc*100; else print "--"}')

  status=$(judge_freshness "$date_str" "$today")

  printf "%-14s | %-12s | %-10s | %-8s | %-20s | %s\n" \
    "$code" "$name" "$price" "${chg_pct}%" "${date_str:-未知} ${time_str:-}" "$status"

done <<< "$raw"

echo ""
echo "铁律 0：引用股价必须标注上方的数据时点；'非当日'数据属于历史价，须另行说明。"
