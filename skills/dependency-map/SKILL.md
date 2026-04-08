---
name: dependency-map
version: 1.0.0
last_updated: 2026-04-08
repository: https://github.com/312362115/claude
description: >
  依赖关系分析技能：回答"改这里会影响哪里"。
  追踪调用链、数据流、副作用，评估改动的影响面。
  和 code-walkthrough 的区别：walkthrough 关注"是什么"，dependency-map 关注"改了影响谁"。
  触发词：影响面、改这个会影响哪里、依赖关系、调用链、影响分析、谁在用这个。
  触发场景：改动前评估影响、重构前分析依赖、删代码前确认安全、API 变更前评估调用方。
  即使用户没有说"依赖分析"，只要意图是"评估改动的影响范围"，都应触发此技能。
---

# 依赖关系分析（Dependency Map）

> 代码改动最怕的不是改错，而是不知道改动波及到了哪里。
> 本 skill 的使命：在改动之前，画出影响面地图。

---

## 第一步：确定分析目标

用 `AskUserQuestion` 确认：
- **分析什么**：哪个函数/类/模块/文件？
- **为什么分析**：准备改什么？删什么？还是纯了解？
- **分析深度**：只看直接依赖，还是追踪到底？

```
分析请求
  │
  ├─ 改函数签名 → 追踪所有调用方
  ├─ 改数据结构 → 追踪数据的读写点
  ├─ 删文件/模块 → 追踪所有 import
  ├─ 改 API 接口 → 追踪前端调用 + 外部消费方
  └─ 改配置/环境变量 → 追踪所有引用点
```

---

## 第二步：静态依赖分析

### 2.1 Import/Require 分析

```bash
# 找到谁引用了目标文件
grep -r "import.*from.*'目标模块'" src/
grep -r "require('目标模块')" src/

# 或用 Grep 工具搜索
```

输出格式：
```markdown
## 引用关系

### 被谁引用（上游，改目标会影响他们）
- `src/api/auth.ts:3` — import { login } from './services/auth'
- `src/api/user.ts:5` — import { validateToken } from './services/auth'
- `tests/auth.test.ts:1` — import { login, logout } from '../services/auth'

### 引用了谁（下游，目标依赖他们）
- `src/models/user.ts` — UserModel
- `src/utils/jwt.ts` — signToken, verifyToken
- `bcrypt` — 外部依赖
```

### 2.2 函数/方法级调用链

对于函数级分析，追踪更精细的调用关系：

```bash
# 搜索函数名的所有调用
grep -rn "目标函数名(" src/ --include="*.ts" --include="*.js"
```

输出格式：
```markdown
## 调用链：validateToken()

定义：src/services/auth.ts:45

调用方：
├─ src/middleware/auth.ts:12 — authMiddleware() 每个请求都会调用
│   └─ 被 src/api/index.ts:8 的 app.use(authMiddleware) 注册为全局中间件
├─ src/api/user.ts:23 — getUserProfile() 手动调用做额外校验
└─ tests/auth.test.ts:34 — 测试用例

影响面评估：
- authMiddleware 是全局中间件 → 改签名会影响所有需要认证的接口
- 测试需要同步更新
```

---

## 第三步：数据流分析

当改动涉及数据结构时，追踪数据从哪来、到哪去：

### 3.1 数据结构变更

```markdown
## 数据流：User 类型

### 定义位置
`src/types/user.ts:5` — interface User { id, name, email, role }

### 创建点（写入）
- `src/services/user.ts:createUser()` — 注册时创建
- `src/services/auth.ts:oauthCallback()` — OAuth 登录时创建

### 读取点
- `src/api/user.ts:getUserProfile()` — 返回给前端
- `src/middleware/auth.ts:12` — 从 token 解析出 user
- `src/services/order.ts:45` — 创建订单时读取 user.id

### 持久化
- `src/models/user.ts` — 数据库 users 表
- `src/utils/cache.ts:getUserCache()` — Redis 缓存

### 影响评估
如果给 User 加字段：
- 数据库需要 migration
- 缓存的序列化/反序列化需要兼容
- API 响应自动包含（如果没有字段过滤的话）

如果删 User 字段：
- 检查所有读取点是否还在用
- 前端是否依赖这个字段
```

---

## 第四步：输出影响面评估

### 4.1 影响面清单

```markdown
## 影响面评估：<改动描述>

### 直接影响（必须改）
| 文件 | 行号 | 影响原因 | 改动类型 |
|------|------|---------|---------|
| src/api/auth.ts | 23 | 调用了要修改的函数 | 同步更新参数 |
| src/middleware/auth.ts | 12 | 依赖返回值结构 | 适配新结构 |

### 间接影响（需要验证）
| 文件 | 行号 | 风险点 | 验证方式 |
|------|------|--------|---------|
| src/api/user.ts | 45 | 使用了相同的类型 | 跑测试确认 |

### 不受影响（确认安全）
- src/services/order.ts — 虽然在同目录，但无依赖关系
- src/utils/format.ts — 纯工具函数，不涉及

### 测试影响
- tests/auth.test.ts — 需要更新测试用例
- tests/user.test.ts — 需要回归验证
```

### 4.2 风险等级

| 等级 | 判断标准 |
|------|---------|
| **低风险** | 只影响内部实现，公共接口不变，有测试覆盖 |
| **中风险** | 影响多个文件但不影响外部接口，有部分测试覆盖 |
| **高风险** | 影响公共接口/全局中间件/数据结构，测试覆盖不足 |

---

## 分析准则

- **宁多不漏**：不确定的归入"需要验证"，不要归入"不受影响"
- **标注行号**：每个影响点必须标注具体位置，方便定位
- **区分直接/间接**：直接影响必须改，间接影响需验证，不要混在一起
- **关注隐式依赖**：不只看 import，还要看运行时依赖（事件监听、全局状态、环境变量）
- **递归但有界**：追踪调用链要有深度限制，一般追 3 层足够。超过 3 层的间接影响可忽略

---

## 与其他 skill 的关系

```
code-walkthrough（理解代码）→ dependency-map（评估影响）→ refactoring（执行改动）
```

**dependency-map vs code-walkthrough**：
- walkthrough：**理解**代码。"这段代码是什么，怎么运转"
- dependency-map：**评估**影响。"改这里会动到哪里"
- 通常先 walkthrough 建立理解，再 dependency-map 评估改动
