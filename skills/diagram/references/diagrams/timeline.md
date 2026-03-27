# 时间线规范（Timeline）

> 工具：Mermaid（`timeline`）

---

## 适用场景

- 技术演进历程、产品发展史、项目里程碑

---

## 布局规则

1. 从左到右时间推进
2. 时间节点等距分布
3. 每个时间节点标注年份/日期 + 事件
4. 可按阶段分组

---

## 模板

`templates/mermaid/timeline.mmd`

---

## 生成命令

```bash
mmdc -i input.mmd -o output.png -b white -s 2
```
