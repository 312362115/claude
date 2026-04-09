---
name: db-review
version: 1.0.0
last_updated: 2026-04-09
repository: https://github.com/312362115/claude
description: >
  数据库代码审查 + Migration 安全检查。
  代码审查：锁表风险、索引缺失、慢 SQL 模式、N+1 查询。
  Migration 审查：破坏性操作、Schema 漂移检测、回滚方案。
  适用于 SQL（MySQL/PostgreSQL/SQLite）和 ORM（Prisma/TypeORM/Sequelize/SQLAlchemy/Drizzle）。
  触发词：数据库检查、migration 检查、慢 SQL、索引、锁表、schema 漂移、db review。
  触发场景：新增/修改 migration 文件后、数据库相关代码 review、上线前检查、性能排查中发现 DB 瓶颈。
---

# 数据库审查（DB Review）

> 数据库问题的修复成本随阶段指数增长：代码审查 < migration 审查 < 上线后排查 < 数据修复。
> 尽早发现，尽早修复。

---

## 第一步：确定审查范围和模式

```
收到审查请求
  │
  ├─ 代码审查模式（改了数据库相关代码）
  │   └─ 检查 SQL 质量 + 查询性能 + 锁风险
  │
  ├─ Migration 审查模式（新增/修改 migration 文件）
  │   └─ 检查安全性 + Schema 漂移 + 回滚方案
  │
  └─ 全量审查（上线前 / 用户主动要求）
      └─ 代码审查 + Migration 审查 + Schema 一致性
```

### 技术栈识别

自动检测项目使用的数据库和 ORM：

| 检测目标 | 检测方式 |
|---------|---------|
| Prisma | `prisma/schema.prisma`、`@prisma/client` |
| TypeORM | `typeorm` 依赖、`@Entity()` 装饰器 |
| Sequelize | `sequelize` 依赖、`.define()` 调用 |
| Drizzle | `drizzle-orm` 依赖、`drizzle.config.ts` |
| SQLAlchemy | `sqlalchemy` 依赖、`Base.metadata` |
| 原生 SQL | `.sql` 文件、`query()` / `execute()` 调用 |
| 数据库类型 | 连接字符串、驱动依赖（`pg`/`mysql2`/`better-sqlite3`） |

---

## 第二步：代码审查 — SQL 质量与性能

### 检查维度 1：慢 SQL 模式

**逐条检查以下反模式**，对每个发现标注风险等级：

| 反模式 | 问题 | 正确做法 |
|--------|------|---------|
| `SELECT *` | 取了不需要的列，浪费 IO 和内存 | 明确列出需要的字段 |
| 无 WHERE 的全表查询 | 数据量大时直接拖垮 DB | 加条件过滤，分页查询 |
| WHERE 中对列使用函数 | `WHERE YEAR(created_at) = 2026` 无法走索引 | 改为范围查询 `WHERE created_at >= '2026-01-01'` |
| `LIKE '%keyword%'` | 前缀通配符无法走索引 | 考虑全文索引或搜索引擎 |
| `OR` 条件跨列 | 优化器难以使用索引 | 拆成 UNION 或调整索引策略 |
| 子查询在 WHERE 中 | `WHERE id IN (SELECT ...)` 可能逐行执行 | 改为 JOIN |
| `ORDER BY` 无索引支撑 | 大表排序触发 filesort | 确保排序字段有索引 |
| `DISTINCT` 掩盖重复 | 通常是 JOIN 写错的信号 | 检查 JOIN 条件是否正确 |

**审查方法**：
1. 搜索所有 SQL 语句（原生查询、ORM 的 raw query、query builder）
2. 对每条 SQL 判断是否命中上述反模式
3. ORM 调用也要检查——`findAll()` 没加条件等价于 `SELECT *` 全表扫描

### 检查维度 2：N+1 查询

**这是 ORM 项目最常见的性能杀手。**

```
# 反模式：循环中查询
users = User.findAll()
for user in users:
    orders = Order.findAll({ where: { userId: user.id } })  # N 次查询

# 正确：预加载/JOIN
users = User.findAll({ include: [Order] })  # 1 次查询
```

**检查方法**：
1. 搜索循环体内的数据库调用（`for`/`forEach`/`map` 中的 `find`/`query`/`select`）
2. 检查 ORM 的关联查询是否使用了 eager loading（`include`/`joinedload`/`with`）
3. 检查 GraphQL resolver 中的数据加载是否使用了 DataLoader

### 检查维度 3：锁表风险

**以下操作在大表上可能导致长时间锁表**：

| 操作 | MySQL 风险 | PostgreSQL 风险 | 安全替代 |
|------|-----------|----------------|---------|
| `ALTER TABLE ADD COLUMN` (有默认值) | 锁表重写（MySQL < 8.0） | 8.0+ 大多即时 | MySQL < 8.0 用 pt-online-schema-change |
| `ALTER TABLE ADD INDEX` | 锁表 | 支持 `CONCURRENTLY` | PG: `CREATE INDEX CONCURRENTLY` |
| `ALTER TABLE MODIFY COLUMN` 改类型 | 锁表重写 | 可能锁表 | 分步迁移：新列 → 同步数据 → 切换 |
| `UPDATE` 无 WHERE 大批量 | 行锁升级为表锁 | 大量行锁 | 分批更新（每批 1000-5000 行） |
| `DELETE` 大批量 | 同上 | 同上 | 分批删除 + 短暂 sleep |
| 长事务中的 DDL | 锁等待、死锁 | 锁等待 | DDL 独立事务、短事务 |

**审查方法**：
1. 检查 migration 文件中的 ALTER TABLE 操作
2. 评估目标表的数据量（如果能拿到）
3. 大表（>10 万行）的 DDL 操作标记为**高风险**

### 检查维度 4：索引审查

| 检查项 | 问题信号 |
|--------|---------|
| 缺失索引 | WHERE/JOIN/ORDER BY 中的列没有索引 |
| 冗余索引 | `INDEX(a)` 和 `INDEX(a, b)` 并存（前者被后者包含） |
| 过多索引 | 单表 >6 个索引，影响写入性能 |
| 索引列顺序 | 复合索引列顺序不符合查询模式（最左前缀原则） |
| 低选择性索引 | 在布尔/状态等低基数列上建索引（通常无效） |
| 未使用索引 | 有索引但查询没走到（函数包裹、类型不匹配） |

**审查方法**：
1. 读取 schema/migration 中的索引定义
2. 对照查询语句的 WHERE/JOIN/ORDER BY 检查索引覆盖
3. ORM 的 `@Index()`/`index: true` 也要检查

### 检查维度 5：事务与并发

| 检查项 | 关注点 |
|--------|--------|
| 事务范围 | 事务是否过大？包含了不必要的操作？ |
| 死锁风险 | 多个事务是否以不同顺序操作同一组表？ |
| 隔离级别 | 是否使用了过高的隔离级别（SERIALIZABLE）？ |
| 连接泄漏 | 事务/连接是否在异常路径中正确释放？ |
| 乐观锁 | 并发更新场景是否有版本号/乐观锁保护？ |

---

## 第三步：Migration 审查 — 安全性与一致性

### 3.1 破坏性操作检查

**以下操作不可逆或有数据丢失风险**，必须标记为高风险：

| 操作 | 风险 | 安全做法 |
|------|------|---------|
| `DROP TABLE` | 数据永久丢失 | 先备份、确认无引用、保留回滚窗口 |
| `DROP COLUMN` | 列数据丢失 | 确认代码已移除引用后再删列 |
| `RENAME TABLE/COLUMN` | 代码引用断裂 | 分步：新建 → 同步 → 切换 → 清理旧的 |
| `TRUNCATE` | 数据清空 | 不应出现在 migration 中 |
| `ALTER COLUMN` 收窄类型 | 数据截断 | 先检查现有数据是否溢出 |
| `NOT NULL` 约束（已有数据列） | 空值行报错 | 先填充默认值再加约束 |

**审查方法**：
1. 逐行读 migration 文件，标记所有 DROP/RENAME/ALTER 操作
2. 每个破坏性操作必须有对应的**回滚方案**（down migration）
3. 检查 down migration 是否真的能回滚（不是空函数）

### 3.2 Schema 漂移检测

> **这是你反复踩坑的问题：本地和服务端 schema 不一致、缺字段。**

**漂移来源**：

```
1. 手动改了数据库但没写 migration（最常见）
2. migration 执行顺序不一致（分支合并后）
3. migration 只跑了一半（报错后手动修了但没记录）
4. ORM 的 model 定义和 migration 不同步
5. 多人开发时 migration 文件冲突
```

**检查流程**：

```
Step 1: 收集当前 Schema 定义来源
  ├─ ORM model/entity 定义（代码中的"应该是什么"）
  ├─ Migration 文件链（"变更历史"）
  └─ 数据库实际状态（如果能连接）

Step 2: 交叉比对
  ├─ Model vs Migration：model 里的字段/类型/约束是否都有对应的 migration？
  ├─ Migration 完整性：migration 链是否连续？有没有遗漏？
  └─ 新增字段检查：最近加的字段有 migration 吗？默认值/可空设置对吗？

Step 3: 输出不一致清单
  每条记录：字段名、model 中的定义、migration 中的定义、差异描述
```

**具体检查项**：

| 检查项 | 方法 |
|--------|------|
| **Model 和 Migration 字段一致** | 遍历 model 所有字段，确认每个字段在 migration 链中有对应的 CREATE/ALTER |
| **类型一致** | model 中的类型（`String`/`Int`/`DateTime`）和 migration 中的 SQL 类型匹配 |
| **可空性一致** | model 标记 `optional`/`nullable` 的字段，migration 中没加 `NOT NULL` |
| **默认值一致** | model 中有 `@default()` 的字段，migration 中有 `DEFAULT` |
| **索引一致** | model 中 `@index`/`@unique` 的字段，migration 中有对应的 INDEX |
| **关联关系一致** | model 中的外键关系，migration 中有对应的 FOREIGN KEY |
| **migration 时间线连续** | 按时间戳排序，检查有没有跳跃或冲突 |

### 3.3 回滚方案检查

每个 migration 必须有可执行的回滚方案：

| 检查项 | 要求 |
|--------|------|
| down/rollback 函数存在 | 不能是空函数或 `throw new Error('not implemented')` |
| down 函数逻辑正确 | `up` 中加的列，`down` 中要删；`up` 中改的类型，`down` 中要改回 |
| 数据恢复 | 破坏性操作的 down 需要说明数据恢复策略（即使无法完全自动恢复） |

### 3.4 Migration 最佳实践

| 实践 | 要求 |
|------|------|
| 单一职责 | 一个 migration 只做一件事（加表、加列、加索引分开） |
| 可重复执行 | migration 应该幂等，重复运行不报错（`IF NOT EXISTS`） |
| 数据迁移分离 | schema 变更和数据填充放在不同的 migration 中 |
| 命名规范 | 文件名能反映操作内容（`add_email_to_users` 而非 `migration_042`） |

---

## 第四步：风险分级与输出

### 风险等级

| 等级 | 标准 | 处理要求 |
|------|------|---------|
| **高危** | 数据丢失、锁表超 30s、schema 漂移（已知不一致）、无回滚方案 | **必须修复**，给出具体方案 |
| **中危** | 性能隐患（N+1、缺索引）、回滚方案不完整、潜在的并发问题 | **建议修复**，给出方向 |
| **低危** | 最佳实践缺失（命名、注释、冗余索引）、小表操作 | **记录**，不阻断 |

### 输出格式

**快速审查**（终端输出）：

```
## DB Review 结果

🔴 高危 x N | 🟡 中危 x N | 🟢 低危 x N

### 高危
1. [锁表风险] migrations/20260409_add_index.sql:15 — 大表加索引未用 CONCURRENTLY
   → 修复：`CREATE INDEX CONCURRENTLY idx_users_email ON users(email);`

### 中危
1. [N+1] src/services/order.ts:42 — 循环内查询用户信息
   → 修复：使用 include/joinedload 预加载

### Schema 漂移
- ⚠️ User.phone: model 中存在(String, optional)，但无对应 migration
- ⚠️ Order.discount: model 类型 Decimal，migration 中为 Float
```

**完整审查**时，生成报告到 `docs/audits/YYYY-MM-DD-db-review.md`。

---

## 与其他 skill 的衔接

```
代码开发中
  │
  ├─ 改了数据库代码？→ task-finish 自检时提示跑 db-review（代码审查模式）
  ├─ 新增 migration？→ 提交前跑 db-review（migration 审查模式）
  │
  ↓ 上线前
  ├─ security-audit 审查注入防护（SQL 注入维度）
  └─ db-review 全量审查（Schema 漂移 + 锁表 + 性能）
```

- **perf-profiling**：发现 DB 慢查询后，交给 db-review 做 SQL 层面的深度分析
- **security-audit**：SQL 注入是安全问题，由 security-audit 负责；查询性能是 db-review 负责
- **task-finish**：改动涉及 migration 文件时，提示跑 db-review

---

## 注意事项

- **先理解业务再审查**：脱离业务的索引建议是无意义的。先搞清楚查询频率和数据量
- **小表不教条**：几百行的配置表不需要纠结索引优化
- **ORM 不是借口**：ORM 生成的 SQL 也可能很烂，必要时看生成的实际 SQL
- **环境差异**：本地 SQLite + 生产 PostgreSQL 时，migration 语法差异是漂移的常见来源
- **不替代 DBA**：复杂的分库分表、主从延迟等架构级问题需要 DBA 介入
