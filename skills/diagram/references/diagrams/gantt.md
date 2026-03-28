# 甘特图规范（Gantt Chart）

> 工具：HTML/SVG · Playwright 截图

---

## 适用场景

- 项目开发排期、迭代计划、里程碑跟踪

---

## 布局规则

1. 任务按 section 分组（需求、开发、测试、部署等）
2. 时间轴从左到右
3. 关键任务标注 `crit`
4. 里程碑标注 `milestone`
5. 今日线自动标注

---

## Mermaid 主题配置

```
%%{init: {'theme':'base','themeVariables':{
  'fontSize':'13px',
  'fontFamily':'PingFang SC, Inter, sans-serif',
  'sectionBkgColor':'#EFF6FF',
  'altSectionBkgColor':'#F8FAFC',
  'taskBkgColor':'#3B82F6',
  'taskTextColor':'#FFFFFF',
  'activeTaskBkgColor':'#2563EB',
  'critBkgColor':'#F43F5E',
  'critBorderColor':'#9F1239',
  'todayLineColor':'#F43F5E',
  'gridColor':'#E2E8F0',
  'textColor':'#1E293B'
}}}%%
```

---

## 模板

`templates/html/gantt.html`

---

## 生成方式

1. 生成 HTML 文件（纯 HTML+CSS+SVG，无外部依赖）
2. Playwright 截图为 PNG
