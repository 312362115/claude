# Changelog — finance-analysis

## 0.2.0 (2026-04-20)

**核心定位升级**：从"决策导向 skill"进化为"**命题驱动 + 3 大核心价值**"的深度分析 skill。

### 新增

- **`frameworks/command-driven-analysis.md`**（skill 主入口）
  - 3 大核心价值：数据深度（T1-T5 分级）/ 分析深度（独立推演 4 动作）/ 透过表象 + 预判未来（3 层信息 + 4 时点预判）
  - 4 类命题识别路由：个股（A）/ 政策事件（B）/ 公司事件（C）/ 主题赛道（D）
  - 每类套路的数据抓取 + 分析步骤 + 输出格式
  - 执行检查单（红线：未读原始披露 / 只抄观点 / 不预判未来 → 重做）

- **`templates/alpha-thesis-card.md`**（核心分析 template）
  - 7 问法：生意 / Layer / 竞争 / 预期差 / bear case / 估值 / 证伪
  - 预期差强度自评（≤ 2 不下注）
  - 凯利仓位计算
  - 含群核 0068.HK worked example

- **`templates/ai-daily-checkup.md`**（可选辅助）
  - 多源交叉（rss + watchlist 股价 + 公告直查 + X FinTwit）
  - rss 盲区兜底策略
  - ⚠️ skill 不主动触发，用户想用定时器自己配

- **`templates/ai-monthly-checkup.md`**（可选辅助）
  - 月度 8 层系统扫描 checklist
  - 定位：日频主力补漏，不是独立工具

### 修改

- SKILL.md 主文件升级
  - 新增"Skill 的灵魂：3 大核心价值"章节作为 skill 标签
  - 主入口从"决策路由"改为"命题驱动分析"
  - 明确"不做自动触发"（手动调用为主）
- 强化 AI 主题 framework 的四层监控体系（日频主频）
- frameworks/templates 索引重构

### 核心洞察（本轮讨论沉淀）

- **数据深度**：原始数据优先（SEC EDGAR / HKEXnews / API 机读 > 新闻摘要 > 社区观点）
- **分析深度**：不抄卖方观点，自己算自己推
- **透过表象**：信息 3 层（表层媒体标题 / 中层财报数据 / **里层数据关系 + 指引落差 + 沉默字段** = Alpha 所在）
- **预判未来**：可证伪的 T+3 / T+6 / T+12 / T+24 四点预测

## 0.1.0 (2026-04-20)
- 初始版本：从群核科技（0068.HK）首日套利案例沉淀
- 定位：**决策导向金融分析** skill，与 deep-research（研究导向）正交
- 首版覆盖：HK IPO 打新套利 framework
- 占位扩展：股票估值 / 基金分析 / 债券分析 / 技术面 / 事件驱动
- 信源复用：引用 `skills/deep-research/references/sources/{finance,blacklist}.yaml`
