# 网络拓扑图规范（Network Topology）

> 工具：HTML/SVG · Playwright 截图

---

## 适用场景

- 企业网络架构、云基础设施、安全边界

---

## 布局规则

1. 从上到下：外网 → DMZ → 内网
2. 网络区域用分组容器，不同区域用不同层级色
3. 设备水平排列在区域内
4. 连线标注端口/协议/带宽

---

## 区域配色

| 区域 | 层级色 |
|------|--------|
| 外网/互联网 | L-6 Cyan |
| DMZ | L-3 Amber |
| 内网-办公 | L-1 Blue |
| 内网-服务器 | L-2 Emerald |
| 内网-数据 | L-4 Violet |

---

## 模板

`templates/html/network.html`

---

## 生成方式

1. 生成 HTML 文件（纯 HTML+CSS+SVG，无外部依赖）
2. Playwright 截图为 PNG
