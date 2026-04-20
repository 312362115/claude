# Deep Research 行业信源矩阵调研

> 调研日期：2026-04-20
> 关联 backlog：`docs/backlog/2026-04-20-deep-research-multi-agent.md`（P1）
> 后续：基于本 spec 拆 plan 生成首批 3 份 YAML

---

## 背景与动机

deep-research skill 的 P1 子项"行业信源矩阵"需要为每个行业预置一份权威数据源白名单（YAML），搜索时 80% 预算倾斜白名单，避免被 SEO 内容农场误导。

本次调研为首批 3 份 YAML 打地基：
- **`internet-tech.yaml`**（1 个行业）
- **`finance.yaml`**（汇总金融：A 股 / 美股 / 港股 / 加密货币 / 债券宏观 5 子块）
- **`academic.yaml`**（1 个行业）

## 打分维度（五维，0-5）

| 维度 | 含义 | 评分规则 |
|------|------|---------|
| **authority** 权威性 | 一手/官方/监管认证 | 5=原始一手（监管/财报/交易所），3=主流媒体，1=转引聚合 |
| **freshness** 时效性 | 更新频率 | 5=实时，4=日，3=周，2=月，1=季度+ |
| **accessibility** 可访问性 | 免费 + 爬取便利 | 5=免费 WebFetch 直取，3=需 Playwright，1=付费/强反爬 |
| **density** 信息密度 | 单次抓取有效量 | 5=结构化数据批量，3=可全文提取，1=散乱一句话 |
| **chinese_coverage** 中文覆盖 | 中文原生 + 中国市场 | 5=原生中文+中国市场，0=纯英文非中国，`-1`=不适用 |

## 白名单启用边界（重要）

**行业信源白名单只在"命题调研"场景启用**，以下场景直接绕过：

| 场景 | 路径 |
|------|------|
| 具体 API 用法、命令参数、语法查询 | Lead 自查 → 官方 docs 一跳到底 |
| 某 bug 复现、错误信息排查 | 自查 → 官方 issue / docs |
| 行业分析、竞品对比、市场研究、技术选型、学术综述 | **加载白名单** → 派 sub-agent |

这条判断将作为未来 `_router.md` 的第一道闸门：先识别"具体查询 vs 命题调研"，后者才进入行业标签识别流程。

---

## 一、互联网技术（internet-tech）

### T1 核心源

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | Access | 一句话 |
|------|-----|------|------|------|------|------|--------|--------|
| GitHub Trending | github.com/trending | 5 | 5 | 5 | 4 | 1 | WebFetch/API | 全球代码热度事实标准，API 5000 req/h |
| Stack Overflow Developer Survey | survey.stackoverflow.co | 5 | 2 | 5 | 5 | 1 | WebFetch | 年度行业基准，CSV 可下载 2011-2025 |
| Hacker News | news.ycombinator.com | 4 | 5 | 5 | 3 | 0 | WebFetch/API | Firebase API 免费，投票过滤高信噪比 |
| Hugging Face Daily Papers | huggingface.co/papers | 5 | 5 | 5 | 4 | 1 | WebFetch/Hub API | Papers with Code 已并入 HF |
| MDN Web Docs | developer.mozilla.org | 5 | 4 | 5 | 3 | 2 | WebFetch | Web 标准权威，开源于 GitHub mdn/content |
| Google AI / DeepMind Blog | blog.google/technology/ai | 5 | 3 | 5 | 2 | 0 | WebFetch | Gemini/AlphaFold 原厂一手 |
| Anthropic News | anthropic.com/news | 5 | 3 | 5 | 2 | 0 | WebFetch | Claude 模型唯一权威发布源 |
| OpenAI Blog | openai.com/news | 5 | 3 | 5 | 2 | 0 | WebFetch | GPT/Sora 原始发布 |

### T2 二手/社区

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | Access | 一句话 |
|------|-----|------|------|------|------|------|--------|--------|
| Reddit r/MachineLearning | reddit.com/r/MachineLearning | 4 | 5 | 3 | 2 | 0 | WebFetch/付费 API | 2023 API 收费；r/programming 已封 AI 内容 |
| InfoQ 中文站 | infoq.cn | 3 | 5 | 4 | 3 | 5 | WebFetch | QCon 主办方，编委会审核 |

### china_specific

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | Access | 一句话 |
|------|-----|------|------|------|------|------|--------|--------|
| 中国信通院白皮书库 | caict.ac.cn/kxyj/qwfb/bps | 5 | 2 | 2 | 3 | 5 | WebFetch（反爬） | 工信部直属智库，季度/年度白皮书 |
| 阮一峰科技爱好者周刊 | ruanyifeng.com/blog | 3 | 3 | 5 | 2 | 5 | WebFetch/RSS | 个人整理，中文开发者信号源 |
| 掘金 | juejin.cn | 2 | 5 | 3 | 3 | 5 | Playwright | 字节旗下，原创与搬运混杂 |

### blacklist

| 名称 | 理由 |
|------|------|
| CSDN（csdn.net） | 大量 AI 洗稿/转引/搬运，强反爬+强制登录，内容农场特征明显 |

### 互联网组 surprises

- **Papers with Code 已 301 重定向至 Hugging Face**，两者合并；单独列 paperswithcode.com 无意义
- **中国信通院 SSL 证书问题 + 412 反爬**，权威源可访问性反而差
- **r/programming 2026-04 封禁 AI LLM 内容**，头部技术社区开始抵制 AI 内容泛滥
- **CSDN 在 HN 被明确评价为"质量存疑的聚合平台"**，应进 blacklist
- **掘金原创激励机制效果有限**，转引/搬运比例仍高

---

## 二、金融 - A 股（china-a-shares）

### T1 监管/交易所

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | Access | 一句话 |
|------|-----|------|------|------|------|------|--------|--------|
| 巨潮资讯网 | cninfo.com.cn | 5 | 5 | 3 | 5 | 5 | WebFetch（Angular 动态） | A 股公告法定一手源，三所全量 |
| 中国证监会 | csrc.gov.cn | 5 | 3 | 4 | 3 | 5 | WebFetch | 监管文件+处罚决定书+发审 |
| 上交所 | sse.com.cn | 5 | 5 | 3 | 4 | 5 | WebFetch | 沪市/科创板公告+行情 |
| 深交所 | szse.cn | 5 | 5 | 3 | 4 | 5 | WebFetch | 深市/创业板公告 |
| 北交所 | bse.cn | 5 | 4 | 4 | 3 | 5 | WebFetch | 北交所唯一法定源 |
| 中证网（上海证券报） | cnstock.com | 4 | 4 | 4 | 3 | 5 | WebFetch | 证监会法定披露媒体 |
| 国家统计局 | stats.gov.cn | 5 | 3 | 4 | 4 | 5 | WebFetch | GDP/CPI/PMI 权威源 |
| 中证指数公司 | csindex.com.cn | 5 | 4 | 2 | 4 | 5 | Playwright（反爬） | 沪深 300/中证 500 指数官方 |

### T2 披露媒体

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | 一句话 |
|------|-----|------|------|------|------|------|--------|
| 证券时报·e 公司 | stcn.com | 4 | 4 | 3 | 4 | 5 | 龙虎榜/融资追踪增值数据 |
| 财新网 | caixin.com | 4 | 4 | 2 | 3 | 5 | 独家财新 PMI；付费墙较高 |
| 21 世纪经济报道 | 21jingji.com | 3 | 4 | 4 | 2 | 5 | 政策信号捕获 |

### china_specific

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | 一句话 |
|------|-----|------|------|------|------|------|--------|
| Tushare Pro | tushare.pro | 3 | 4 | 4 | 5 | 5 | 积分制免费 API；2025 年有过停运，单点故障风险 |
| 申万宏源行业指数 | swsindex.com | 4 | 3 | 2 | 4 | 5 | 行业分类事实标准（31 个一级行业），官网不稳 |

### blacklist

| 名称 | 理由 |
|------|------|
| 东方财富股吧 guba.eastmoney.com | 680 万条学术样本中确认大规模机器刷帖/水军 |
| 雪球 xueqiu.com | WAF 强反爬，数据为转发聚合，讨论情绪化 |

### A 股 surprises

- **申万指数官网超时不可达**，官方数据实际依赖 Tushare 等第三方中转
- **中证指数公司官网反爬**（JS 渲染 + 空内容），商业授权才能完整历史
- **Tushare Pro 2025 年曾停运**，暴露单点故障风险
- **雪球 WAF 极强**，WebFetch 返回加密页面

---

## 三、金融 - 美股（us-equities）

### T1 监管/政府

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | Access | 一句话 |
|------|-----|------|------|------|------|------|--------|--------|
| **SEC EDGAR + data.sec.gov API** | sec.gov/edgar, data.sec.gov | 5 | 4 | 5 | 5 | 1 | 免费 REST API | 10-K/10-Q/8-K/DEF 14A 全量，XBRL 可机读 |
| NYSE Data Products | nyse.com/data-products | 5 | 5 | 2 | 5 | 1 | 付费订阅 | TAQ/L2/企业行动；L1 基础免费 |
| NASDAQ / Nasdaq Data Link | nasdaq.com/solutions | 5 | 5 | 3 | 5 | 1 | 部分免费注册 | TotalView L2 付费；Data Link 含 Quandl 遗产 |
| FINRA 市场数据中心 | finra-markets.morningstar.com | 4 | 3 | 4 | 3 | 1 | WebFetch | OTC + TRACE 固收数据 |
| FRED (圣路易斯联储) | fred.stlouisfed.org | 5 | 3 | 5 | 4 | 1 | 免费 API（需 key） | 840k 经济时序，API 业界标杆 |
| BEA 经济分析局 | bea.gov | 5 | 2 | 4 | 3 | 1 | 免费 API | GDP/PCE 一手，亦镜像至 FRED |
| BLS 劳工统计局 | bls.gov | 5 | 2 | 4 | 3 | 1 | 免费 API（v2 需 key） | CPI/NFP 一手 |

### T2 财经媒体 + 聚合

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | 一句话 |
|------|-----|------|------|------|------|------|--------|
| Yahoo Finance | finance.yahoo.com | 3 | 4 | 5 | 4 | 2 | 无官方 API；yfinance 社区库不稳 |
| Bloomberg Terminal | bloomberg.com/professional | 5 | 5 | 1 | 5 | 2 | 年费 $24k/席，API BLPAPI |
| Reuters | reuters.com | 4 | 5 | 4 | 3 | 2 | 新闻免费；Refinitiv Eikon 付费 |
| WSJ | wsj.com/market-data | 4 | 4 | 2 | 3 | 1 | 付费墙严格，调查报道价值高 |
| CNBC | cnbc.com/us-markets | 3 | 5 | 5 | 3 | 1 | 速度优先，评论性内容多 |
| MarketWatch | marketwatch.com | 3 | 5 | 5 | 3 | 1 | 道琼斯旗下免费版 |
| Finviz | finviz.com | 3 | 3 | 5 | 4 | 1 | 筛选器+热力图利器 |
| Seeking Alpha | seekingalpha.com | 3 | 4 | 3 | 4 | 1 | Quant Ratings 底层数据来自 S&P Global |

### T3 情绪

| 名称 | URL | 一句话 |
|------|-----|--------|
| StockTwits | stocktwits.com | 散户情绪另类数据，无分析权威性 |

### 美股 surprises

- **data.sec.gov 提供完全免费无认证的 REST JSON API**，直接拉 XBRL 财务数据，是最被低估的官方入口
- **FINRA 自己声明"不保证数据准确性"**，其行情数据不应单独依赖（监管披露权威，行情数据不是）
- **NYSE TAQ 全面迁移到 AWS 云 + Kafka 流**，交易所数据正在云原生化
- **Yahoo Finance 无官方 API**，yfinance 社区库是生产环境风险点

---

## 四、金融 - 港股（hk-equities）

### T1 交易所/监管

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | Access | 一句话 |
|------|-----|------|------|------|------|------|--------|--------|
| **港交所披露易 HKEXnews** | hkexnews.hk | 5 | 5 | 3 | 5 | 5 | WebFetch（PDF+动态） | 港股公告法定一手，中英双语 |
| HKEX 市场数据 | hkex.com.hk/Market-Data | 5 | 4 | 4 | 4 | 5 | WebFetch | 成交统计+指数+GEM |
| HKEX 沪深港通统计 | hkex.com.hk/Mutual-Market | 5 | 4 | 3 | 4 | 5 | WebFetch | 南下资金唯一官方，CCASS 仅保留 12 个月滚动 |
| 披露易权益披露 SDI | hkexnews.hk/di | 5 | 4 | 3 | 4 | 5 | WebFetch | 大股东/董监高持股变动 |
| 香港证监会 SFC | sfc.hk | 5 | 4 | 5 | 3 | 5 | WebFetch | 监管/执法/持牌人 |
| 香港金管局 HKMA | hkma.gov.hk | 5 | 3 | 4 | 3 | 4 | WebFetch（SSL 问题） | HIBOR/外汇储备/银行监管 |
| 巨潮（H 股中文联合披露） | cninfo.com.cn | 4 | 5 | 4 | 5 | 5 | WebFetch | A+H 双重上市中文版唯一源 |

### T2 港股媒体

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | 一句话 |
|------|-----|------|------|------|------|------|--------|
| AAStocks 阿斯达克 | aastocks.com | 3 | 4 | 3 | 3 | 5 | 行情原创接入，新闻转引；HTTPS→HTTP 降级 |
| 财华社 Finet HK | finet.hk | 3 | 4 | 4 | 3 | 5 | 本身是 GEM 上市 08317，繁中原创 |
| 智通财经 | zhitongcaijing.com | 3 | 5 | 4 | 3 | 5 | 简中原创港股资讯最大供应商 |
| 富途牛牛 | futunn.com | 3 | 5 | 3 | 4 | 5 | 大行研报聚合，需注册 |
| 香港经济日报 ET Net | etnet.com.hk | 3 | 4 | 3 | 3 | 4 | 本港非中资企业覆盖最深 |

### T3 二次加工

| 名称 | URL | 一句话 |
|------|-----|--------|
| 东方财富沪深港通 | data.eastmoney.com/hsgt | 南下资金可视化，国内访问友好但属二次加工 |

### 港股 surprises

- **CCASS 南向持股仅保留 12 个月滚动**，超期不可查，历史研究须提前存档
- **财华社本身是 GEM 上市公司（08317）**，"监管对象即数据源"的罕见案例
- **智通财经是东方财富/同花顺的港股内容源头**，研究南下情绪应溯源到此
- **HKMA 官网 SSL 证书在标准工具中报错**
- **披露易 Historical Daily 需 JS 执行环境**（Playwright）

---

## 五、金融 - 加密货币（crypto）

### T1 链上/DeFi

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | Access | 一句话 |
|------|-----|------|------|------|------|------|--------|--------|
| Etherscan | etherscan.io | 5 | 5 | 4 | 3 | 1 | 免费 API | 以太坊链上事实标准 |
| BscScan | bscscan.com | 5 | 5 | 4 | 3 | 2 | 免费 API | BNB Chain 权威 |
| Solscan | solscan.io | 5 | 5 | 4 | 3 | 1 | 免费 API | Solana 链上必备 |
| **DefiLlama** | defillama.com | 5 | 4 | 5 | 5 | 2 | 免费无需 key | DeFi TVL 事实标准，可访问性最高 |
| Dune Analytics | dune.com | 4 | 4 | 3 | 5 | 1 | 免费基础 + 付费 Pro | SQL 自定义分析，社区看板丰富 |
| CoinGecko | coingecko.com | 4 | 4 | 5 | 4 | 3 | 免费层 10k/月 | 价格聚合权威 |
| Ethereum Foundation / Vitalik Blog | blog.ethereum.org, vitalik.eth.limo | 5 | 3 | 5 | 3 | 1 | WebFetch | EIP/协议升级权威 |
| 香港证监会 SFC 虚拟资产专页 | sfc.hk/TC/Rules-and-Standards/Virtual-assets | 5 | 3 | 4 | 2 | 5 | WebFetch | VASP 牌照名单+中文监管 |

### T2 数据/研究

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | 一句话 |
|------|-----|------|------|------|------|------|--------|
| CoinMarketCap | coinmarketcap.com | 4 | 4 | 4 | 3 | 4 | Binance 旗下有利益冲突，历史最长 |
| Glassnode | glassnode.com | 5 | 4 | 2 | 5 | 1 | BTC/ETH 宏观链上黄金标准，机构付费 |
| CryptoQuant | cryptoquant.com | 4 | 5 | 3 | 4 | 2 | 交易所流动数据最实时 |
| Nansen | nansen.ai | 4 | 4 | 2 | 4 | 1 | 500M+ 标签地址，$150+/月 |
| Messari | messari.io | 4 | 3 | 3 | 4 | 1 | Crypto Theses 年度报告必读 |
| The Graph | thegraph.com | 4 | 5 | 3 | 5 | 1 | DeFi 协议原始数据 GraphQL |

### T3 中文媒体

| 名称 | URL | 一句话 |
|------|-----|--------|
| PANews | panewslab.com | 中文原创质量较高，监管政策解读有价值 |
| BlockBeats 律动 | theblockbeats.info | 海外内容翻译为主，少量原创 |

### blacklist

| 名称 | 理由 |
|------|------|
| "一周涨 10x" / "代打新" / "必涨清单"类站点 | 诱导欺诈，无调研价值 |
| 金色财经 jinse.cn | 流量最大中文加密媒体，付费软文混杂，原创极少 |

### 加密 surprises

- **DefiLlama 免费无需 key**，可访问性最高且权威性 5 分，性价比最佳 T1
- **金色财经因软文问题入 blacklist**，反映中文加密媒体商业模式普遍问题
- **Nansen 已推 NXP 代币质押**，平台自身 DeFi 化

---

## 六、金融 - 债券/宏观（bond-macro）

### T1 - 全球核心

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | Access | 一句话 |
|------|-----|------|------|------|------|------|--------|--------|
| FRED | fred.stlouisfed.org | 5 | 5 | 5 | 5 | 1 | 免费 API（需 key） | 840k 时序，美国宏观首选 |
| 美联储 H.15 选定利率 | federalreserve.gov/releases/h15 | 5 | 5 | 4 | 3 | 0 | WebFetch/CSV | 政策利率一手源 |
| **BIS Data Portal** | data.bis.org | 5 | 3 | 4 | 4 | 1 | SDMX API 免费 | 全球离岸债 IDS+跨境银行敞口独一档 |
| 中国人民银行 | pbc.gov.cn | 5 | 4 | 2 | 3 | 5 | WebFetch（PDF 为主） | LPR/汇率中间价/M2 法定源 |
| 国家统计局 data.stats | data.stats.gov.cn | 5 | 4 | 3 | 4 | 5 | WebFetch | GDP/CPI/PMI 权威；无 REST API |
| 中债登 yield.chinabond | yield.chinabond.com.cn | 5 | 4 | 2 | 4 | 5 | WebFetch + 邮件申请 | 国债收益率曲线法定估值机构 |
| 中国货币网 CFETS | chinamoney.com.cn | 5 | 5 | 2 | 4 | 5 | 部分 WebFetch | Shibor/DR007 银行间市场唯一权威 |
| IMF 数据门户 | data.imf.org | 5 | 3 | 4 | 4 | 2 | SDMX API 免费 | WEO 含未来 5 年预测 |

### T2 - 专项接入

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | 一句话 |
|------|-----|------|------|------|------|------|--------|
| 美国财政部 Fiscal Data | fiscaldata.treasury.gov | 5 | 5 | 5 | 3 | 0 | 免费 REST，无需 key |
| BLS | bls.gov | 5 | 4 | 4 | 4 | 0 | CPI/NFP 原始，v2 API |
| BEA | bea.gov | 5 | 4 | 4 | 3 | 0 | GDP/PCE 原始 |
| 外汇管理局 SAFE | safe.gov.cn | 5 | 3 | 3 | 3 | 5 | 外汇储备+BOP |
| 财政部（中） | mof.gov.cn/zhengwuxinxi/caizhengshuju | 5 | 4 | 2 | 3 | 5 | 国债招标结果 |
| 世界银行数据 | data.worldbank.org | 4 | 2 | 5 | 4 | 3 | API v2 免费，年度为主 |
| 上清所 SHCH | shclearing.cn | 4 | 4 | 2 | 3 | 5 | 信用债估值+IRS 定盘价 |

### 债券宏观 surprises

- **CFETS 收益率曲线每分钟更新**，远超预期，但机构访问壁垒高
- **BIS SDMX API 完全免费无需注册**，与其冷门形象不符
- **美国财政部 Fiscal Data API 无需 key**，知名度远不及 FRED 但同为一手
- **中债登机构数据需邮件申请**，缺乏现代化 API
- **IMF WEO 含未来 5 年预测**，可直接机读

---

## 七、学术研究（academic）

### T1 预印本/索引

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | Access | 一句话 |
|------|-----|------|------|------|------|------|--------|--------|
| **arXiv** | arxiv.org | 5 | 5 | 5 | 5 | 2 | 免费 OAI-PMH+REST | 物理/数学/CS/ML 预印本事实标准 |
| Semantic Scholar | semanticscholar.org | 4 | 4 | 5 | 4 | 1 | 免费 Graph API | AI 增强，200M+ 论文 |
| **OpenAlex** | openalex.org | 4 | 4 | 5 | 3 | 3 | 免费 CC0，需 key | Web of Science 开放替代，2024 已入主流排名 |
| PubMed / PMC | pubmed.ncbi.nlm.nih.gov | 5 | 5 | 5 | 4 | 1 | E-utilities API | 生物医学黄金标准，2026-08 旧 FTP 下线 |
| bioRxiv / medRxiv | biorxiv.org, medrxiv.org | 4 | 5 | 5 | 5 | 1 | REST API | 2025-03 已移交 openRxiv |
| Papers with Code | paperswithcode.com | 4 | 5 | 5 | 4 | 1 | REST API | 已并入 HF，ML 论文-代码-数据集三联 |
| OpenReview | openreview.net | 5 | 4 | 4 | 5 | 1 | Python SDK | NeurIPS/ICLR 完整审稿，2025-11 有 API 安全事件 |

### T2 元数据/出版商

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | 一句话 |
|------|-----|------|------|------|------|------|--------|
| CrossRef | crossref.org | 5 | 4 | 5 | 2 | 2 | DOI 骨干，月 10 亿 API 请求 |
| IEEE Xplore | ieeexplore.ieee.org | 5 | 3 | 3 | 3 | 1 | 元数据免费，全文机构订阅 |
| **ACM Digital Library** | dl.acm.org | 5 | 3 | 4 | 4 | 1 | **2026-01 起全 OA**，CS 顶会全文可达 |
| SSRN | ssrn.com | 4 | 4 | 3 | 4 | 1 | 社科 arXiv，Elsevier 已收购 |
| ChemRxiv | chemrxiv.org | 4 | 4 | 5 | 4 | 1 | 化学领域专属 |
| OSF Preprints | osf.io/preprints | 3 | 4 | 5 | 4 | 1 | PsyArXiv/SocArXiv 聚合 |

### 反爬警告

| 名称 | URL | 说明 |
|------|-----|------|
| Google Scholar | scholar.google.com | 反爬极强，无官方 API；scholarly/SerpAPI 不稳定，不适合批量 |

### china_specific

| 名称 | URL | 权威 | 时效 | 可访 | 密度 | 中文 | 一句话 |
|------|-----|------|------|------|------|------|--------|
| CNKI 中国知网 | cnki.net | 5 | 4 | 2 | 5 | 5 | 核心期刊 95%+ 完整率，付费无 API |
| 万方数据 | wanfangdata.com.cn | 4 | 4 | 2 | 4 | 5 | 中文学术第二大 |
| 维普 VIP | qikan.cqvip.com | 4 | 3 | 2 | 4 | 5 | 13000+ 中文期刊 |

### 学术 surprises

- **ACM Digital Library 2026-01 完成全 OA 转型**，CS 领域今年最大可访问性变化
- **OpenAlex 2024 被主流大学排名系统采用**，正成为 Web of Science 开放替代
- **bioRxiv/medRxiv 2025-03 移交 openRxiv**
- **OpenReview 2025-11 API 安全事件**（暴露评审人身份）
- **PubMed Central 2026-08 旧 FTP 下线**，需迁移到新 OA Web Service API
- **中文无 arXiv 对标**（chinaxiv.org 活跃度有限），是最大基础设施空白

---

## 八、量化行情数据 API（补充维度）

> **维度说明**：前 7 节偏"权威调研视角"（分析师找一手信源做判断）。本节补开发者视角：**给定股票拉 K线/基本面/盘口/Tick** 该用什么 API。两类源基本不重叠：调研源重权威与信息密度，量化 API 重免费额度与结构化程度。
>
> 本节打分多加一维 **free_tier_quota**（0-5）：5=免费可生产，4=免费够原型，3=免费够试用，2=免费限制严（如 5 req/min），1=仅付费

### 8.1 A 股 K线/基本面

| 名称 | URL | Auth | 权威 | 时效 | 可访 | 密度 | 免费额度 | 中文 | 覆盖 | 一句话 |
|------|-----|------|------|------|------|------|---------|------|------|--------|
| **BaoStock** | baostock.com | 无 | 3 | 3 | 5 | 3 | 5 | 5 | K线+基本面+财报 | 完全免费无注册；1990+ 日 K，1999+ 分钟 K；稳定性优于 AKShare |
| AKShare | akshare.akfamily.xyz | 无 | 2 | 4 | 5 | 4 | 5 | 5 | K线+Tick+基本面+宏观 | 聚合新浪/东财；覆盖最广但接口频变+封 IP 风险 |
| Tushare Pro | tushare.pro | API key | 3 | 3 | 3 | 4 | 2 | 5 | K线+基本面+财报+公告+股东 | 积分制；主流 A 股需 2000 分（约 200 元/年） |
| efinance | github.com/Micro-sheep/efinance | 无 | 1 | 4 | 5 | 3 | 5 | 5 | K线+基本面 | 个人项目，包装东财接口；非官方，接口易失效 |
| 新浪财经接口 | hq.sinajs.cn | 无 | 1 | 5 | 5 | 2 | 5 | 5 | 实时快照+盘口 | 非官方；仅实时快照无历史；高并发封 IP |
| Wind / Choice / iFinD | — | 付费 | 5 | 5 | 1 | 5 | 1 | 5 | 全套 | 机构终端，年费万元级，开发者不作重点 |

**A 股首选**：**BaoStock**（免费可生产）+ Tushare Pro（需更丰富基本面/公告时升级）

### 8.2 美股 K线/基本面

| 名称 | URL | Auth | 权威 | 时效 | 可访 | 密度 | 免费额度 | 覆盖 | 一句话 |
|------|-----|------|------|------|------|------|---------|------|--------|
| **Finnhub** | finnhub.io | API key | 3 | 4 | 5 | 3 | 4 | K线+基本面 | 免费 60 次/分，同类最慷慨；含 WebSocket+新闻情绪 |
| Polygon.io | polygon.io（→ massive.com） | API key | 4 | 5 | 3 | 5 | 2 | K线+Tick+盘口+基本面 | 美股全量 Tick+Level2；2024 被 Massive 收购；免费 5 次/分 |
| yfinance | github.com/ranaroussi/yfinance | 无 | 1 | 3 | 5 | 3 | 5 | K线+基本面+财报+股东 | Yahoo 社区库，最快上手；非官方生产慎用 |
| Alpha Vantage | alphavantage.co | API key | 4 | 3 | 4 | 4 | 2 | K线+基本面+财报 | 2024 底免费层从 500/天砍到 25/天；付费 $50/月起 |
| Tiingo | tiingo.com | API key | 3 | 3 | 4 | 3 | 3 | K线+基本面 | 量化研究者向，EOD 为主；有学术折扣 |
| Twelve Data | twelvedata.com | API key | 3 | 4 | 4 | 3 | 3 | K线+基本面 | 免费 8 次/分≈800/天；支持多资产 |
| Nasdaq Data Link | data.nasdaq.com | API key | 5 | 2 | 4 | 3 | 3 | K线+基本面+宏观 | 原 Quandl；WIKI EOD 免费但 2018 停更 |
| EODHD | eodhd.com | API key | 3 | 4 | 4 | 4 | 2 | K线+基本面+财报 | 覆盖全球 150k+ 标的；免费 20/天 |
| ~~IEX Cloud~~ | iexcloud.io | — | 0 | 0 | 0 | 0 | 0 | — | **已于 2024-08-31 停服**，迁移至 Polygon.io / Finnhub |

**美股首选**：**Finnhub**（免费层最大，原型到低频生产够用）；需 Tick → Polygon.io 付费

### 8.3 港股 K线/基本面

| 名称 | URL | Auth | 权威 | 时效 | 可访 | 密度 | 免费额度 | 中文 | 覆盖 | 一句话 |
|------|-----|------|------|------|------|------|---------|------|------|--------|
| **富途 Futu OpenAPI** | openapi.futunn.com | 开户 | 5 | 5 | 3 | 5 | 3 | 5 | K线+Tick+盘口+基本面 | 开户后港股 LV2 免费；唯一免费实时盘口；需本地跑 FutuOpenD |
| 老虎 Tiger OpenAPI | quant.tigerbrokers.com.cn | 开户 | 5 | 5 | 3 | 4 | 3 | 5 | K线+Tick+盘口+基本面 | 定位类似富途，选一即可 |
| HKEX 延迟行情 | hkex.com.hk | API key | 5 | 3 | 4 | 2 | 4 | 5 | K线 | 官方 15 分钟延迟；实时需授权数据商付费 |
| 新浪港股接口 | hq.sinajs.cn | 无 | 1 | 4 | 5 | 2 | 5 | 5 | 实时快照 | 非官方，`hk00700` 代码格式；低频监控可用 |

**港股首选**：**富途 Futu OpenAPI**（唯一免费实时 Level2），无券商账户退到 HKEX 延迟

### 8.4 加密货币 K线/Tick/盘口

| 名称 | URL | Auth | 权威 | 时效 | 可访 | 密度 | 免费额度 | 覆盖 | 一句话 |
|------|-----|------|------|------|------|------|---------|------|--------|
| **CCXT** | github.com/ccxt/ccxt | API key（私有）| 4 | 5 | 5 | 4 | 5 | K线+Tick+盘口 | 108+ 交易所统一接口事实标准；REST 免费，WebSocket 需 Pro |
| Binance API | developers.binance.com | 无（公共） | 5 | 5 | 5 | 4 | 5 | K线+Tick+盘口 | 最大流动性，公共行情 1200 权重/分；中国大陆需代理 |
| OKX API | okx.com/docs-v5 | 无（公共） | 5 | 5 | 5 | 4 | 5 | K线+Tick+盘口 | 中英文档完整，支持现货/永续/期权 |
| Bybit API | bybit-exchange.github.io | 无（公共） | 5 | 5 | 5 | 3 | 5 | K线+Tick+盘口 | 120 次/分；历史深度略弱 |
| Kraken API | docs.kraken.com | 无（公共） | 5 | 5 | 4 | 3 | 5 | K线+Tick+盘口 | 合规记录优秀，历史 Tick 仅 720 条 |
| Tardis.dev | tardis.dev | API key 付费 | 4 | 2 | 3 | 5 | 2 | Tick+盘口 | 业界最完整历史 Tick；每月 1 号数据免费；$30+/月 |
| Kaiko | kaiko.com | 付费 | 5 | 5 | 1 | 5 | 1 | K线+Tick+盘口 | 机构级，无免费层，与 Tardis 互补 |

**Crypto 首选**：**CCXT + Binance**（统一接口层 + 最大流动性数据源）；历史回测补 Tardis.dev

### 8.5 量化 API surprises

- **IEX Cloud 已于 2024-08-31 正式停服**，原用户需迁移到 Polygon.io / Finnhub
- **Polygon.io 2024 被 Massive.com 收购**，域名已重定向，定价策略待观察
- **Alpha Vantage 免费层 2024 底从 500/天砍到 25/天**，对依赖免费层的原型影响大
- **AKShare 封 IP 问题比 2022 年前显著**，生产稳定性下降
- **Tardis.dev 每月 1 号数据免费**，无需 API key，是验证回测框架的低成本入口
- **CCXT Pro（WebSocket）是付费版**，标准 CCXT 仅 REST 轮询，高频策略须注意

### 8.6 量化 API gaps

- 雪球 / AAStocks 非官方接口当前反爬强度未验证
- Binance 分钟权重限额细节未完整 fetch
- Financial Modeling Prep（FMP，免费 250/天）未展开评估
- 掘金量化 JoinQuant / 米筐 RQData A 股数据质量未验证
- Quiver Quant 国会交易/内部人士交易另类数据未评估

### 8.7 量化 API 维度与调研源的对应关系

YAML 结构建议把两类源分字段存：

```yaml
industry: finance.us-equities
# 调研视角（来自第三节）
tier_1_sources:
  - { name: "SEC EDGAR", ... }
# 量化视角（来自本节，新增字段）
quant_api_sources:
  - { name: "Finnhub", free_tier_quota: 4, data_coverage: ["K线","基本面"], ... }
```

两类源在 router 里也区分启用：
- 命题含"财报/监管/行业格局" → 加载 tier_1_sources
- 命题含"K线/回测/基本面数据/股价" → 加载 quant_api_sources
- 含"API/接口/量化" 关键词 → 优先 quant_api_sources

---

## 跨行业观察

1. **"免费 + 可机读 API + 一手"三角的 T1 典范**：SEC EDGAR（美股）、FRED（宏观）、DefiLlama（crypto）、arXiv（学术）—— 都是性价比最高的 T1，应第一批接入
2. **BIS / 美国财政部 Fiscal Data / OpenAlex 是"被低估的 T1"**：权威 5 分但知名度低，应在 YAML 里加优先级标记
3. **中文权威源普遍 API 缺失**：央行/中债登/CNKI 都权威性 5 分但 accessibility 2 分，YAML 里需标"需 Playwright / 邮件申请 / 付费"
4. **SEO 内容农场通用识别规则**：无实名、无原始数据引用、标题夸张承诺、付费软文混杂——CSDN / 东财股吧 / 金色财经 / "必涨清单"站都是这套特征
5. **已知 blacklist 共识**：CSDN、东方财富股吧、雪球、金色财经、各类"内幕"站
6. **官网反爬 vs 数据开放度悖论**：中国信通院、中证指数、雪球——权威源反而反爬强；是 YAML 里必须明确 access_method 的原因

---

## 下一步（方向调整：精简版 A 架构）

### 架构决策（2026-04-20）

原 P1 计划"每行业一份完整 YAML"存在**穷举不可能 + 快速腐烂**两个根本问题：
- 互联网技术有无穷子域，新框架每周出现，硬编码追不上
- AI/LLM 赛道一季度一变，死清单 3 个月过时
- IEX Cloud 停服、Polygon 被收购、paperswithcode 并入 HF —— 本次调研就抓到 3 例腐烂

**采纳精简版 A**：死配置只做 **"LLM top-of-mind 里没有的冷门权威源"**，其余靠启发式 prompt。

### YAML 体系设计（3 层）

```
references/sources/
├── blacklist.yaml              ← 全域共享，最高优先级
├── _source_heuristics.md       ← 一手源识别启发式（互联网/AI 走这条，不穷举）
├── _router.md                  ← 命题 → 路径判断：白名单启用边界 + 标签匹配
├── _schema.yaml                ← YAML 格式规范
├── finance.yaml                ← 精简版：10-15 条冷门权威
└── academic.yaml               ← 精简版：10-15 条冷门权威
```

**不做**：`internet-tech.yaml`（靠 heuristics 代替）、`ai-ml.yaml`（同）、穷举类 YAML

### 维护纪律

**只收 "LLM top-of-mind 没有的"**。判断标准：**"不看 YAML，sub-agent 自己能想到吗？"** —— 能想到的不进。

#### finance.yaml 候选（精选 10-15 条）

| 收录 | 不收录（LLM 自己知道） |
|-----|---------------------|
| BIS Data Portal（SDMX 免费） | SEC EDGAR |
| 中债登 yield.chinabond | FRED |
| CFETS / 中国货币网（Shibor/DR007） | NASDAQ / NYSE 官方 |
| 美国财政部 Fiscal Data（无需 key） | 人民银行 / 国家统计局 |
| 上清所 SHCH（信用债估值） | Bloomberg / Reuters |
| HKEX 披露易 SDI + CCASS 南向 | 巨潮 / 证监会 / 交易所 |
| 外汇管理局 SAFE | Yahoo Finance / CoinMarketCap |
| 申万宏源行业指数 | Coinbase / Binance API |
| Tardis.dev（crypto 历史 Tick 免费日） | CoinGecko / DefiLlama |
| BaoStock（A 股免费可生产量化 API） | AKShare / Tushare / yfinance |
| Finnhub（免费 60/分） | Alpha Vantage / Polygon |
| IEX Cloud → 迁移至 Finnhub（腐烂标记） | — |

#### academic.yaml 候选（精选 10-15 条）

| 收录 | 不收录 |
|-----|-------|
| OpenAlex（2024 入主流排名，替代 WoS） | arXiv / PubMed / Google Scholar |
| bioRxiv / medRxiv（2025 移交 openRxiv） | Nature / Science / IEEE |
| ChemRxiv（化学专属预印本） | Semantic Scholar |
| OpenReview（ML 顶会完整审稿） | CNKI（LLM 知道但不开放） |
| CrossRef（DOI 骨干 + 开放引用） | — |
| ACM DL 全 OA 转型（2026-01） | — |
| SSRN（Elsevier 收购后） | — |
| OSF Preprints（聚合社科预印本） | — |
| Papers with Code → 并入 HF（腐烂标记） | — |

#### blacklist.yaml（全域共享，最高价值）

```yaml
blacklist:
  - name: CSDN
    domain: csdn.net
    reason: "AI 洗稿 + 转引为主，强反爬，内容农场"
    category: tech_spam

  - name: 东方财富股吧
    domain: guba.eastmoney.com
    reason: "680 万样本中确认大规模机器刷帖/水军"
    category: finance_spam

  - name: 雪球
    domain: xueqiu.com
    reason: "WAF 强反爬，数据为转发聚合，讨论情绪化"
    category: finance_spam

  - name: 金色财经
    domain: jinse.cn
    reason: "付费软文混杂，原创极少"
    category: crypto_spam

  # SEO 内容农场通用识别规则
patterns:
  - pattern: "无实名作者 + 无原始数据引用 + 标题夸张承诺"
    examples: ["一周涨 10x 必涨清单", "内幕消息", "AI 选股"]
    action: blacklist
  - pattern: "域名含常见 SEO 标记"
    examples: ["-news.com", "baijiahao.baidu.com 纯转载"]
    action: downgrade_to_t3
```

### _source_heuristics.md 核心规则

告诉 sub-agent：**没有白名单的领域（互联网/AI/新兴产业）如何识别一手源**。

```markdown
## 一手源识别优先级（高到低）

1. **官方网站 docs/blog**（`<product>.org/docs`, `<product>.io/blog`, `blog.<company>.com`）
2. **官方 GitHub releases**（`github.com/<org>/<repo>/releases`）
3. **官方规范/RFC**（`w3.org/TR/...`, `tc39.es/proposal-...`, EIP/BIP 等）
4. **顶会论文官网**（非聚合站，去对应会议官网）
5. **官方 Twitter/X 账号**（认证蓝标）
6. **原厂技术博客**（Google/Meta/Anthropic/OpenAI/Mozilla 等）
7. **主流社区（有审核机制）**：HN / r/<strict-mod> / InfoQ / LWN

## 必避开

- 任何 blacklist.yaml 列入的域名
- `*.csdn.net` / 掘金搬运类 / 百家号纯转载
- 标题含「震撼」「揭秘」「必涨」「一定要看」的 SEO 站
- 生成式 AI 洗稿站（无实名作者 + 无引用溯源）

## AI/LLM 赛道的一手源推导示例

命题："Claude 3.7 Sonnet 编码能力对比"
→ 一手：anthropic.com/news, anthropic.com/engineering
→ 评测：lmarena.ai, artificialanalysis.ai, livebench.ai, swebench.com
→ 社区：huggingface.co/papers, news.ycombinator.com

命题："Cursor vs Windsurf 差异"
→ 一手：cursor.com/blog, codeium.com/blog（Windsurf 母公司）
→ 社区：news.ycombinator.com, r/ChatGPTCoding
→ 避开：csdn.net / 各类"XX 神器推荐"文
```

### _router.md 核心规则（第一版）

```
## 白名单启用闸门
1. 是否"具体查询"？（API 用法/命令参数/bug 复现）
   → 是：Lead 自查官方 docs，跳过白名单
   → 否：进入 2

2. 命题关键词匹配：
   - "股票/财报/监管/利率/汇率/央行/债券/加密/链上/DeFi" → 加载 finance.yaml
   - "论文/研究/综述/学术" → 加载 academic.yaml
   - 其他技术/AI/产品命题 → 走 _source_heuristics.md（不加载 YAML）

3. 所有命题都加载 blacklist.yaml（最高优先级过滤）

4. 有 YAML 加载时：
   - 搜索预算 70% 倾斜 YAML 冷门权威（因为 LLM 自己知道的不在 YAML 里，需要特别强调）
   - 20% 开放搜索扩展
   - 10% heuristics 发现新一手源
```

### 落地拆子任务（出 plan）

见 `docs/plans/2026-04-20-deep-research-sources-plan.md`

---

## 调查拓扑

| 指标 | 数值 |
|------|------|
| 命题复杂度 | complex |
| 派发 Sub-agent 数 | 8（round 1 × 7 + round 2 × 1 补调研） |
| 最深递归层级 | 2（round 2 的 sub-08 由 Lead 识别维度盲区后 fork） |
| Synthesis 轮次 | 2 |
| 总 WebSearch 次数 | 32 |
| 总 WebFetch 次数 | 61 |
| 总 Findings 数 | 131 |

**Sub-agent 分解**：

| ID | Parent | Round | Topic | Spawn Reason | Budget Used (search/fetch) | Findings | Status |
|----|--------|-------|-------|--------------|---------------------------|----------|--------|
| sub-01 | — | 1 | 互联网技术 | 初始拆解 | 4/8 | 15 | completed |
| sub-02 | — | 1 | 金融-A 股 | 初始拆解 | 3/8 | 15 | completed |
| sub-03 | — | 1 | 金融-美股 | 初始拆解 | 4/7 | 16 | completed |
| sub-04 | — | 1 | 金融-港股 | 初始拆解 | 4/8 | 13 | completed |
| sub-05 | — | 1 | 金融-加密货币 | 初始拆解 | 3/7 | 16 | completed |
| sub-06 | — | 1 | 金融-债券宏观 | 初始拆解 | 4/5 | 15 | completed |
| sub-07 | — | 1 | 学术研究 | 初始拆解 | 4/6 | 17 | completed |
| sub-08 | — | 2 | 量化行情数据 API | missing_dimension（round 1 漏掉开发者视角） | 6/12 | 24 | completed |

**放弃的线索**：无（本次调研无主动放弃的线索，但各 sub-agent 在 gaps 中记录了未覆盖点，见各行业 gaps 段落汇总）

**未覆盖点汇总（gaps，作为后续补充研究线索）**：
- 付费终端（Wind / Choice / iFind / Bloomberg / Refinitiv / FactSet）未验证
- 中证指数公司反爬机制未确认
- ORCID / ResearchGate / NSTL 等辅助学术源未深入
- 中文预印本（chinaxiv.org）活跃度未评估
- 华尔街见闻/老虎证券等中文美股二手源未专项评估

---

## 参考资料

本次调研所有数据均来自 sub-agent 实地访问各源官网、API 文档、社区讨论，原始 JSON 回传归档于 `/tmp/sub-0X-*.json`（调研会话 20260420-1030）。主要权威引用链：

- **一手来源 [T1]**：各监管机构/交易所/央行/预印本平台官网（见各行业表格 URL）
- **二手来源 [T2]**：主流财经媒体、技术社区（见各行业 T2/T3 表格）
- **元信息来源**：Anthropic Multi-Agent Research System（本次调研遵循的架构蓝本）
