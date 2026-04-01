---
priority: P3
status: open
---

# 图表风格统一 + 特殊图表补全

长期事项，按需迭代。

## 需求一：Mermaid 渲染风格与 Diagram Skill PNG 统一

当前 preview-md 中 Mermaid 渲染的视觉效果与 diagram skill PNG 输出存在差异（配色接近但布局/字体/阴影等细节不同）。

**目标**：两种输出在视觉上基本一致，用户无论看 MD 内嵌图还是 PNG 都感觉是同一套设计语言。

**可能的实现方向**：
- 写 Mermaid DSL → diagram 模板 JSON 的解析器
- 或反向：diagram 模板输出时生成与 Mermaid 主题对齐的样式

## 需求二：SWOT / 鱼骨图 / 文氏图加入 bridge.py

这 3 种图表视觉形态特殊（四象限、骨架、圆形交叠），DSL 无法表达，目前只能走 HTML 模板 → PNG。考虑加入 bridge.py 统一管道。

| 图表 | 数据结构 | 复杂度 |
|------|---------|-------|
| SWOT | 4 个列表（优势/劣势/机会/威胁） | 低 |
| 鱼骨图 | 主骨 + 分支列表 | 中 |
| 文氏图 | 2-4 个集合 + 交集描述 | 中 |
