# 思维导图规范（Mind Map）

> 工具：HTML/SVG · Playwright 截图

---

## 适用场景

- 知识结构梳理、头脑风暴、概念关联

---

## 配色规则

- 中心节点：Highlight（`#3B82F6` 实心白字）
- 一级分支：使用主题色序列（每个方向一种色）
- 二级以下：同方向保持同色系
- Mermaid mindmap 自动着色，用 theme base 配置

---

## 布局规则

1. 中心节点居中
2. 一级分支放射展开
3. 节点文字简洁（≤ 8 字）
4. 不超过 3 层深度
5. 一级分支不超过 6 个

---

## 模板

`templates/html/mindmap.html`

---

## 生成方式

1. 生成 HTML 文件（纯 HTML+CSS+SVG，无外部依赖）
2. Playwright 截图为 PNG
