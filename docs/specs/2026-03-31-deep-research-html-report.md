## 技术方案：Deep Research 报告支持 HTML 格式输出

### 1. 背景与目标

**目标**：deep-research skill 新增可选 HTML 格式报告输出，与 MD 格式并存。

**验收标准**：
- 用户指定 HTML 格式时，生成自包含 HTML 报告（单文件，浏览器直接打开）
- 图表以 HTML/SVG 内嵌（不导出 PNG），保留交互性（hover 提示等）
- 报告包含左侧目录导航、锚点跳转、专业排版
- 默认仍输出 MD，不影响现有流程

**不做**：
- 多视觉主题（先做一个通用专业主题）
- PDF 导出
- 在线编辑/协作

### 2. 现状分析

**当前报告生成流程**：
```
SKILL.md 第四步：图表生成
  ├─ 统计图：bridge.py -c config.json -o xxx.png  →  PNG
  ├─ 结构图：手写 HTML → capture.py → PNG
  └─ 输出到 docs/research/assets/*.png

SKILL.md 第五步：撰写报告
  ├─ MD 报告正文，内嵌 ![](assets/xxx.png)
  └─ 输出到 docs/research/YYYY-MM-DD-<topic>.md
```

**已有能力**：
- `bridge.py` 已支持 `-f html` 输出自包含 HTML 图表
- `capture.py` 已支持 `-f html` 输出内联版 HTML
- diagram skill 的模板本身就是 HTML/SVG + JS，中间产物可直接嵌入
- `lib/base.css` + `lib/utils.js` 提供统一的图表样式基础

**核心差距**：
- SKILL.md 流程中没有 HTML 报告分支
- 没有 HTML 报告的外壳模板（目录、导航、排版样式）
- 图表嵌入逻辑只写了 MD 引用方式

### 3. 方案设计

#### 整体思路

不改变调研流程（第一到三步不变），只在第四步（图表生成）和第五步（报告撰写）加入 HTML 分支。

```
第一步：理解命题 → 不变
第二步：信息搜集 → 不变
第三步：分析结论 → 不变
第四步：图表生成 → 新增 HTML 分支（输出 HTML 片段而非 PNG）
第五步：撰写报告 → 新增 HTML 报告组装逻辑
```

#### 3.1 格式选择逻辑

在 SKILL.md 第 1.6 节（与用户对齐）中新增输出格式确认：

```
调研命题：xxx
调研类型：技术选型
报告风格：商务蓝灰
输出格式：Markdown / HTML   ← 新增
...
```

**格式判断规则**：
- 默认：MD
- 用户提到"HTML"、"网页版"、"富文本"、"好看点的"→ HTML
- 用户提到"嵌入图表"、"交互式"→ HTML

#### 3.2 图表生成 — HTML 分支

**统计图表**：bridge.py 已支持 `-f html`，输出 HTML 片段。

```bash
# MD 模式（现有）
python bridge.py -c config.json -o docs/research/assets/<name>.png

# HTML 模式（新增）
python bridge.py -c config.json -o /tmp/<name>.html -f html
```

**结构图表**：capture.py 已支持 `-f html`，或直接使用手写的 HTML 源文件。

```bash
# MD 模式（现有）
python capture.py input.html docs/research/assets/<name>.png

# HTML 模式（新增）
python capture.py input.html /tmp/<name>.html -f html
# 或直接用 input.html（已是自包含的）
```

HTML 模式下图表暂存 `/tmp/`，后续由报告组装脚本读取并内嵌。

#### 3.3 HTML 报告组装

新增 `scripts/assemble_html.py` 脚本，职责：

1. **读取 MD 报告内容**（Claude 先按正常流程写 MD）
2. **MD → HTML 转换**（用 Python 内置能力或简单正则，不引入重依赖）
3. **替换图表引用**：将 `![alt](assets/xxx.png)` 替换为对应的 HTML 图表片段
4. **注入外壳模板**：包裹报告 HTML 模板（header、目录导航、样式、footer）
5. **输出自包含 HTML 文件**

**或者更简单的方案**（推荐）：

Claude 直接生成 HTML 报告正文（而非先写 MD 再转换），图表部分直接嵌入 HTML 片段。提供一个 HTML 报告模板供 Claude 参照格式。

**推荐方案 B：Claude 直接写 HTML**。理由：
- 省去 MD→HTML 转换的损失和复杂性
- Claude 已有能力直接生成结构化 HTML
- 图表嵌入更自然（直接在写报告时粘贴 HTML 片段）
- 不需要额外脚本依赖

#### 3.4 HTML 报告模板设计

新增 `references/html-report-template.html` — 一个通用的专业风格 HTML 外壳。

**核心特性**：
- **左侧固定目录**：自动从 h2/h3 标签生成，锚点跳转，当前章节高亮
- **响应式布局**：窄屏时目录收起
- **印刷级排版**：正文宽度限制、行高优化、表格美化
- **配色方案**：专业蓝灰色调（与 tech-blue 图表主题协调）
- **图表容器**：带边框、阴影、标题样式，图表 HTML 直接嵌入
- **引用样式**：上标脚注、来源层级[T1/T2/T3]的颜色区分
- **打印友好**：打印时隐藏目录，正文全宽

**模板结构**：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>{{报告标题}}</title>
  <style>/* 内联所有 CSS */</style>
</head>
<body>
  <nav class="sidebar"><!-- 自动目录 --></nav>
  <main class="content">
    <header><!-- 报告元信息 --></header>
    <article><!-- 报告正文 --></article>
  </main>
  <script>/* 目录生成 + 滚动高亮 JS */</script>
</body>
</html>
```

#### 3.5 报告输出

```
docs/research/
├── YYYY-MM-DD-<topic>.md       ← MD 模式（现有）
├── YYYY-MM-DD-<topic>.html     ← HTML 模式（新增）
└── assets/
    └── *.png                    ← 仅 MD 模式需要
```

HTML 模式不产生 assets 目录下的 PNG 文件（图表内嵌到 HTML 中）。

### 4. 具体改动点

| 文件 | 改动 | 说明 |
|------|------|------|
| `SKILL.md` | 修改第 1.6、4、5 节 | 新增 HTML 分支逻辑 |
| `references/html-report-template.html` | **新增** | HTML 报告外壳模板 + CSS + JS |
| `references/templates/_common.md` | 补充说明 | 添加 HTML 模式下的使用指引 |

### 5. 实施计划

1. **设计并实现 HTML 报告模板**（html-report-template.html）
   - 通用专业主题 CSS
   - 自动目录 JS
   - 图表嵌入容器样式
   - 验收：用示例内容填充模板，浏览器打开效果良好

2. **修改 SKILL.md — 新增 HTML 分支**
   - 1.6 节：格式选择逻辑
   - 第四步：HTML 模式下图表生成方式
   - 第五步：HTML 报告撰写流程 + 模板引用
   - 质量检查：新增 HTML 格式检查项
   - 验收：SKILL.md 逻辑清晰，MD/HTML 两条路径不冲突

3. **更新 _common.md 模板说明**
   - 补充 HTML 模式下的使用指引

### 6. 风险与边界

- **风险**：HTML 文件体积可能较大（内嵌图表 JS/CSS）→ 可接受，单文件便利性优先
- **风险**：Claude 直接写 HTML 可能格式不一致 → 通过模板 + 示例约束
- **不做**：MD↔HTML 双向转换、多主题切换、PDF 导出
- **影响**：不影响现有 MD 报告流程，纯增量改动
