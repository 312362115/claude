# 决策树规范（Decision Tree）

> 工具：HTML/SVG · Playwright 截图

---

## 适用场景

- 技术选型决策、故障排查路径、分类逻辑

---

## 组件使用

| 元素 | 节点类型 |
|------|---------|
| 根节点 | Highlight（蓝色实心） |
| 判断节点 | Decision（黄色菱形） |
| 推荐结果 | Success（绿色） |
| 不推荐结果 | Error（红色） |
| 中性结果 | Process（蓝色） |

---

## 布局规则

1. 从上到下，树状展开
2. 每层判断条件水平对齐
3. 分支标签在连线上
4. 深度不超过 4 层

---

## 模板

`templates/html/decision-tree.html`

---

## 生成方式

1. 生成 HTML 文件（纯 HTML+CSS+SVG，无外部依赖）
2. Playwright 截图为 PNG
