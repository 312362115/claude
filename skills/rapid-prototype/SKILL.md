---
name: rapid-prototype
version: 1.0.0
last_updated: 2026-04-08
repository: https://github.com/312362115/claude
description: >
  快速原型技能：5 分钟出可交互 demo，验证想法和交互方案。
  比 task-start 轻量得多——不需要 spec/plan，就是快速 PoC。
  输出单个 HTML 文件，浏览器直接打开可交互。
  触发词：快速出个 demo、试一下效果、原型、PoC、验证一下、快速搭个页面。
  触发场景：验证交互方案、给老板演示想法、技术可行性验证、UI 方案对比。
  和 task-start 的 UI 原型环节的区别：task-start 是流程中的一步，
  rapid-prototype 是独立的快速验证工具，可以在任何时候使用。
---

# 快速原型（Rapid Prototype）

> 想法停留在脑子里永远是完美的，做出来才知道行不行。
> 快速原型的目标不是完美，是快速验证"这条路走不走得通"。

---

## 使用场景

| 场景 | 例子 |
|------|------|
| **验证交互** | "这个拖拽排序体验怎么样？" |
| **对比方案** | "A 布局和 B 布局哪个好？" |
| **演示想法** | "给老板看一下大概长什么样" |
| **技术可行性** | "CSS Grid 能不能实现这个布局？" |
| **数据可视化** | "这批数据用什么图表展示合适？" |

---

## 执行流程

```
收到原型请求
  │
  ├─ 1. 快速确认（≤3 个问题）
  │   - 要验证什么？
  │   - 核心交互是什么？
  │   - 用真实数据还是 mock 数据？
  │
  ├─ 2. 直接写代码
  │   - 单个 HTML 文件，内联 CSS + JS
  │   - 不用框架，原生 HTML/CSS/JS
  │   - 可引入 CDN 资源（Tailwind、图表库等）
  │
  ├─ 3. 打开预览
  │   - open 命令在浏览器中打开
  │
  └─ 4. 迭代
      - 用户看完反馈 → 立即修改 → 重新预览
      - 快速迭代，不纠结细节
```

---

## 原型规范

### 技术要求

- **单文件**：一个 HTML 文件搞定，内联所有 CSS 和 JS
- **零构建**：不需要 npm install、不需要编译，浏览器直接打开
- **CDN 可用**：需要库时从 CDN 引入（Tailwind、Chart.js、Sortable.js 等）
- **真实数据**：用接近真实的示例数据，不用 lorem ipsum

### 存放位置

```
docs/prototypes/<名称>-prototype.html
```

原型是临时产出，验证完成后可以删除。如果用户决定正式开发，原型作为参考保留。

### 质量标准

| 要关注的 | 不用关注的 |
|---------|-----------|
| 核心交互能正常工作 | 像素级完美 |
| 信息结构和层级对 | 动画和过渡效果 |
| 接近真实的数据 | 响应式适配 |
| 浏览器能正常打开 | 代码质量和复用性 |
| 关键状态都能看到 | 边界情况处理 |

### 常用 CDN 资源

| 用途 | 库 | CDN |
|------|-----|-----|
| 快速样式 | Tailwind CSS | `https://cdn.tailwindcss.com` |
| 图表 | Chart.js | `https://cdn.jsdelivr.net/npm/chart.js` |
| 拖拽排序 | Sortable.js | `https://cdn.jsdelivr.net/npm/sortablejs` |
| 图标 | Lucide Icons | `https://unpkg.com/lucide@latest` |
| 日期处理 | Day.js | `https://cdn.jsdelivr.net/npm/dayjs` |
| 数据表格 | AG Grid | `https://cdn.jsdelivr.net/npm/ag-grid-community` |

---

## 与其他 skill 的关系

```
想法/灵感 → rapid-prototype（快速验证）
               │
               ├─ 验证通过 → task-start（正式立项开发）
               └─ 验证不通过 → 换方案重试 / 放弃
```

**rapid-prototype vs task-start 的 UI 原型**：
- rapid-prototype：独立使用，随时触发，目标是"快速看到效果"
- task-start UI 原型：流程中的一步，目标是"确认 UI 方向后进入方案设计"
- 两者可以衔接：先 rapid-prototype 快速试几个方案，选定后在 task-start 中正式确认
