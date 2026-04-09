---
name: perf-profiling
version: 1.0.0
last_updated: 2026-04-08
repository: https://github.com/312362115/claude
description: >
  前后端性能分析技能：定位瓶颈、跑 benchmark、对比优化前后效果。
  前端覆盖 Core Web Vitals（LCP/FID/CLS）、Lighthouse 审计、Bundle 分析。
  后端覆盖 API 响应时间、数据库查询性能、内存/CPU profiling。
  核心原则：基于数据定位瓶颈，不做无依据的"优化"。
  触发词：性能优化、太慢了、性能分析、LCP、首屏、响应时间慢、profiling、benchmark。
  触发场景：性能相关需求验收、用户反馈慢、性能指标超标、重构后性能回归验证。
---

# 性能分析（Perf Profiling）

> 优化的前提是度量。不知道慢在哪，就不知道该优化哪。
> 每次优化都要有"前"和"后"的数据对比，否则不算优化。

---

## 第一步：明确分析目标

```
性能问题
  │
  ├─ 前端性能？（页面加载慢、交互卡顿、首屏慢）
  │   └─ 前端分析流程
  │
  ├─ 后端性能？（API 响应慢、数据库查询慢、CPU/内存高）
  │   └─ 后端分析流程
  │
  └─ 不确定？
      └─ 先用浏览器 DevTools Network 面板判断瓶颈在前端还是后端
```

用 `AskUserQuestion` 确认：
- **具体症状**：哪里慢？慢到什么程度？（要数据，不要"感觉"）
- **性能基线**：当前是多少？目标是多少？
- **复现条件**：特定页面？特定数据量？特定并发？

---

## 前端性能分析

### 2.1 Core Web Vitals 度量

| 指标 | 含义 | 达标 | 需改进 | 差 |
|------|------|------|--------|---|
| **LCP** | 最大内容绘制 | ≤2.5s | ≤4s | >4s |
| **INP** | 交互到下一次绘制 | ≤200ms | ≤500ms | >500ms |
| **CLS** | 累计布局偏移 | ≤0.1 | ≤0.25 | >0.25 |

**度量工具**：

```bash
# Lighthouse CLI（如果可用）
npx lighthouse <url> --output=json --output-path=./lighthouse-report.json

# 或用 Playwright 采集性能数据
# 通过 MCP playwright 工具访问页面并执行 performance API
```

### 2.2 Bundle 分析

```bash
# Webpack
npx webpack-bundle-analyzer stats.json

# Vite
npx vite-bundle-visualizer

# Next.js
ANALYZE=true next build
```

关注点：
- 总 bundle 大小（gzip 后）
- 最大的几个依赖占比
- 有没有重复打包的依赖
- 是否做了 code splitting

### 2.3 前端常见瓶颈与优化方向

| 瓶颈 | 诊断方式 | 优化方向 |
|------|---------|---------|
| 首屏大图/大资源阻塞 LCP | Lighthouse / Network 瀑布图 | 懒加载、压缩、CDN、preload 关键资源 |
| JS Bundle 过大 | Bundle 分析 | Code splitting、tree shaking、动态导入 |
| 未优化图片 | Lighthouse 图片审计 | WebP/AVIF、响应式图片、压缩 |
| 布局抖动导致 CLS | Lighthouse CLS 审计 | 固定尺寸占位、字体预加载 |
| 大量 DOM 操作 | Performance timeline | 虚拟列表、减少重排、requestAnimationFrame |
| 第三方脚本阻塞 | Network + Coverage | 延迟加载、异步加载、移除不必要的三方脚本 |

---

## 后端性能分析

### 3.1 API 响应时间度量

```bash
# 简单测量（单次）
time curl -s -o /dev/null -w "%{time_total}" <api-url>

# 并发测试（如 wrk 可用）
wrk -t4 -c100 -d30s <api-url>

# 或用 Node.js 脚本测量
node -e "
const start = Date.now();
fetch('<api-url>').then(() => console.log(Date.now() - start + 'ms'));
"
```

记录关键指标：
- **p50 / p95 / p99 响应时间**
- **吞吐量（req/s）**
- **错误率**

### 3.2 数据库查询分析

```sql
-- MySQL/PostgreSQL 查询分析
EXPLAIN ANALYZE <your-query>;
```

```javascript
// Node.js ORM 慢查询日志
// Prisma: 在 PrismaClient 初始化时开启
const prisma = new PrismaClient({ log: ['query', 'warn', 'error'] });

// Sequelize: 开启 benchmark
const sequelize = new Sequelize({ benchmark: true, logging: console.log });
```

关注点：
- 全表扫描（缺索引）
- N+1 查询
- 未使用的索引
- 慢查询（>100ms）

### 3.3 Node.js / Python Profiling

**Node.js**：
```bash
# CPU profiling
node --prof app.js
node --prof-process isolate-xxx.log > processed.txt

# 内存快照
node --inspect app.js
# 然后在 Chrome DevTools 中 Take Heap Snapshot
```

**Python**：
```bash
# cProfile
python -m cProfile -s cumtime app.py

# memory_profiler
pip install memory_profiler
python -m memory_profiler app.py
```

### 3.4 后端常见瓶颈与优化方向

| 瓶颈 | 诊断方式 | 优化方向 |
|------|---------|---------|
| 数据库查询慢 | EXPLAIN ANALYZE | 加索引、优化查询、减少 N+1 |
| 序列化/反序列化开销 | profiling | 减少响应字段、分页、缓存 |
| 外部 API 调用阻塞 | timing 日志 | 并行调用、缓存、超时控制 |
| 内存泄漏 | 内存快照对比 | 排查未释放的引用、闭包 |
| CPU 密集计算 | CPU profiling | Worker 线程、缓存计算结果 |
| 连接池耗尽 | 连接池监控 | 调整池大小、检查连接泄漏 |

---

## 第四步：优化与对比

### 4.1 优化前记录基线

在做任何改动之前，**必须记录当前性能数据**：

```markdown
## 性能基线（优化前）

| 指标 | 值 | 测量条件 |
|------|-----|---------|
| LCP | 3.8s | 首页，Chrome，4G 模拟 |
| API /users 响应 | p95: 450ms | 100 并发，30s |
| 数据库查询 | 320ms | users 表 10 万行 |
```

### 4.2 优化后对比

每次优化后，用**相同条件**重新测量，对比前后：

```markdown
## 优化效果对比

| 指标 | 优化前 | 优化后 | 改善 |
|------|--------|--------|------|
| LCP | 3.8s | 1.9s | -50% ✅ |
| API /users p95 | 450ms | 120ms | -73% ✅ |
| Bundle 大小 | 2.1MB | 890KB | -58% ✅ |
```

### 4.3 输出性能报告

完整性能分析后，输出报告到 `docs/specs/` 或直接在对话中给出：

```markdown
# 性能分析报告：<模块/页面>

## 问题描述
用户反馈/指标异常的具体描述

## 分析结论
瓶颈在哪，为什么慢

## 优化措施
| # | 措施 | 预期效果 | 实际效果 |
|---|------|---------|---------|

## 性能对比
基线 vs 优化后

## 后续建议
还可以进一步优化的方向
```

---

## 分析准则

- **数据驱动**：不凭直觉优化。先度量，找到瓶颈，再优化，再度量
- **优先级**：先优化影响最大的瓶颈（80/20 法则）
- **工具按项目选**：不强制某个工具，项目里有什么用什么，缺什么建议安装什么
- **不过度优化**：达到目标就停。从 3s 优化到 2s 和从 2s 优化到 1.5s 的成本完全不同
- **回归保护**：性能优化不能破坏功能。优化后必须跑测试确认功能正常

---

## 与其他 skill 的关系

```
task-execute 执行中发现性能问题 → perf-profiling（分析定位）
refactoring 重构后 → perf-profiling（回归验证，确认性能没退化）
release 发版前 → perf-profiling（性能相关需求的验收）
```
