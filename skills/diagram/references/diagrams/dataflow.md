# 数据流图规范（Data Flow Diagram）

> 工具：HTML/SVG · Playwright 截图

---

## 适用场景

- ETL 管道、数据处理流水线、消息队列流

---

## 组件使用

| 元素 | 节点类型 |
|------|---------|
| 处理过程 | Process（蓝色） |
| 数据存储 | Data Store（紫色圆柱） |
| 外部实体 | External（灰色虚线） |
| 数据流 | 标准连线 + 数据名标签 |

---

## 布局规则

1. 从左到右（LR），按数据流向排列
2. 数据源在最左，输出在最右
3. 存储节点在流程下方
4. 连线标注数据类型/格式

---

## 模板

`templates/html/dataflow.html`

---

## 生成方式

1. 生成 HTML 文件（纯 HTML+CSS+SVG，无外部依赖）
2. Playwright 截图为 PNG
