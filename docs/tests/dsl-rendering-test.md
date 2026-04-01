# DSL 渲染测试 — Mermaid + Graphviz

> 覆盖全部 12 种结构图的 DSL 渲染，验证 preview-md 的 mermaid.js 和 viz.js 集成。

---

## 一、Mermaid 图表（11 种）

### 1. Flowchart 流程图

```mermaid
flowchart TD
    A[用户访问] --> B{已登录?}
    B -->|是| C[进入首页]
    B -->|否| D[登录页]
    D --> E[输入凭证]
    E --> F{验证通过?}
    F -->|是| C
    F -->|否| G[提示错误]
    G --> E
```

### 2. Sequence 时序图

```mermaid
sequenceDiagram
    participant C as 客户端
    participant S as 服务端
    participant DB as 数据库
    participant Cache as Redis

    C->>S: POST /api/login
    S->>Cache: 查询限流计数
    Cache-->>S: 返回计数
    alt 未超限
        S->>DB: 查询用户
        DB-->>S: 用户数据
        S->>S: 验证密码
        S-->>C: 200 + Token
    else 超过限制
        S-->>C: 429 Too Many Requests
    end
```

### 3. Class 类图

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound() void
    }
    class Dog {
        +String breed
        +fetch() void
    }
    class Cat {
        +bool indoor
        +purr() void
    }
    Animal <|-- Dog
    Animal <|-- Cat
    Dog --> "1" Animal : belongs to
```

### 4. State 状态图

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Reviewing : 提交审核
    Reviewing --> Approved : 审核通过
    Reviewing --> Rejected : 审核拒绝
    Rejected --> Draft : 重新编辑
    Approved --> Published : 发布
    Published --> Archived : 归档
    Archived --> [*]
```

### 5. ER 图

```mermaid
erDiagram
    USER ||--o{ POST : writes
    USER ||--o{ COMMENT : writes
    POST ||--o{ COMMENT : has
    POST }o--|| CATEGORY : belongs_to

    USER {
        int id PK
        string name
        string email
    }
    POST {
        int id PK
        int user_id FK
        string title
        text content
    }
    COMMENT {
        int id PK
        int post_id FK
        int user_id FK
        text body
    }
    CATEGORY {
        int id PK
        string name
    }
```

### 6. Gantt 甘特图

```mermaid
gantt
    title 产品开发排期
    dateFormat YYYY-MM-DD
    section 设计阶段
        需求分析      :done, a1, 2026-04-01, 5d
        UI 设计       :done, a2, after a1, 4d
        方案评审      :milestone, a3, after a2, 0d
    section 开发阶段
        后端开发      :active, b1, after a3, 10d
        前端开发      :b2, after a3, 8d
        联调测试      :b3, after b1, 5d
    section 发布阶段
        灰度上线      :c1, after b3, 3d
        全量发布      :milestone, c2, after c1, 0d
```

### 7. Mindmap 思维导图

```mermaid
mindmap
  root((跨境电商))
    选品
      市场调研
      竞品分析
      供应链对接
    运营
      Listing 优化
      广告投放
      客服管理
    物流
      头程物流
      海外仓
      末端配送
    合规
      平台政策
      知识产权
      税务合规
```

### 8. Timeline 时间线

```mermaid
timeline
    title 技术演进路线
    2024 Q1 : MVP 上线
             : 核心功能验证
    2024 Q2 : 用户增长
             : A/B 测试框架
    2024 Q3 : 国际化
             : 多语言支持
    2024 Q4 : AI 集成
             : 智能推荐引擎
```

### 9. C4 架构图

```mermaid
C4Context
    title 电商系统 — 系统上下文图

    Person(customer, "买家", "浏览商品、下单购买")
    Person(seller, "卖家", "管理商品、处理订单")

    System(ecommerce, "电商平台", "核心交易系统")
    System_Ext(payment, "支付网关", "处理支付交易")
    System_Ext(logistics, "物流系统", "物流跟踪与配送")

    Rel(customer, ecommerce, "浏览/下单")
    Rel(seller, ecommerce, "管理商品/订单")
    Rel(ecommerce, payment, "发起支付")
    Rel(ecommerce, logistics, "创建物流单")
```

### 10. Sankey 桑基图

```mermaid
sankey-beta

Homepage,Browse,500
Homepage,Search,300
Homepage,Leave,200
Browse,AddToCart,200
Browse,Leave2,300
Search,AddToCart,150
Search,Leave3,150
AddToCart,Order,250
AddToCart,Abandon,100
Order,PaySuccess,200
Order,PayFail,50
```

### 11. Journey 旅程图

```mermaid
journey
    title 用户购物旅程
    section 发现商品
      搜索商品: 5: 买家
      浏览列表: 4: 买家
      查看详情: 4: 买家
    section 下单购买
      加入购物车: 3: 买家
      填写地址: 2: 买家
      支付: 3: 买家, 系统
    section 收货体验
      等待发货: 2: 买家
      物流跟踪: 3: 买家, 系统
      确认收货: 5: 买家
      评价: 4: 买家
```

---

## 二、Graphviz 图表（6 种）

### 11. Architecture 架构图

```dot
digraph architecture {
    rankdir=TB;
    compound=true;
    node [shape=box, style="rounded,filled", fontname="PingFang SC", fontsize=12];
    edge [color="#94A3B8", fontsize=10, fontname="PingFang SC"];

    subgraph cluster_client {
        label="客户端"; style="dashed,rounded"; color="#3b82f6"; fontname="PingFang SC";
        web [label="Web App\nReact", fillcolor="#EFF6FF"];
        mobile [label="Mobile App\nFlutter", fillcolor="#EFF6FF"];
    }

    subgraph cluster_gateway {
        label="网关层"; style="dashed,rounded"; color="#8b5cf6"; fontname="PingFang SC";
        nginx [label="Nginx\n负载均衡", fillcolor="#FAF5FF"];
        api_gw [label="API Gateway\n鉴权/限流", fillcolor="#FAF5FF"];
    }

    subgraph cluster_services {
        label="微服务层"; style="dashed,rounded"; color="#10b981"; fontname="PingFang SC";
        user_svc [label="用户服务", fillcolor="#F0FDF4"];
        order_svc [label="订单服务", fillcolor="#F0FDF4"];
        product_svc [label="商品服务", fillcolor="#F0FDF4"];
        pay_svc [label="支付服务", fillcolor="#F0FDF4"];
    }

    subgraph cluster_data {
        label="数据层"; style="dashed,rounded"; color="#f59e0b"; fontname="PingFang SC";
        mysql [label="MySQL\n主从集群", fillcolor="#FFFBEB"];
        redis [label="Redis\n缓存集群", fillcolor="#FFFBEB"];
        es [label="Elasticsearch\n搜索引擎", fillcolor="#FFFBEB"];
        mq [label="RabbitMQ\n消息队列", fillcolor="#FFFBEB"];
    }

    web -> nginx;
    mobile -> nginx;
    nginx -> api_gw;
    api_gw -> user_svc;
    api_gw -> order_svc;
    api_gw -> product_svc;
    api_gw -> pay_svc;
    user_svc -> mysql;
    order_svc -> mysql;
    order_svc -> mq [label="异步"];
    product_svc -> es;
    product_svc -> redis;
    pay_svc -> mysql;
}
```

### 12. Swimlane 泳道图（用 subgraph 模拟）

```dot
digraph swimlane {
    rankdir=LR;
    node [shape=box, style="rounded,filled", fontname="PingFang SC", fontsize=11];
    edge [fontname="PingFang SC", fontsize=10];

    subgraph cluster_customer {
        label="买家"; style="filled"; color="#EFF6FF"; fontname="PingFang SC";
        c1 [label="提交订单", fillcolor="#DBEAFE"];
        c2 [label="确认收货", fillcolor="#DBEAFE"];
    }

    subgraph cluster_system {
        label="系统"; style="filled"; color="#F0FDF4"; fontname="PingFang SC";
        s1 [label="创建订单", fillcolor="#D1FAE5"];
        s2 [label="扣减库存", fillcolor="#D1FAE5"];
        s3 [label="发送通知", fillcolor="#D1FAE5"];
    }

    subgraph cluster_warehouse {
        label="仓库"; style="filled"; color="#FFFBEB"; fontname="PingFang SC";
        w1 [label="拣货打包", fillcolor="#FEF3C7"];
        w2 [label="发货", fillcolor="#FEF3C7"];
    }

    c1 -> s1 -> s2 -> w1 -> w2 -> s3 -> c2;
}
```

### 14. Network 网络图

```dot
digraph network {
    rankdir=TB;
    node [shape=box, style="rounded,filled", fontname="PingFang SC", fontsize=11];
    edge [color="#94A3B8"];

    subgraph cluster_public {
        label="公网"; style="dashed"; color="#ef4444"; fontname="PingFang SC";
        cdn [label="CDN\n内容分发", fillcolor="#FEF2F2"];
        dns [label="DNS\n域名解析", fillcolor="#FEF2F2"];
    }

    subgraph cluster_dmz {
        label="DMZ 区"; style="dashed"; color="#f59e0b"; fontname="PingFang SC";
        fw [label="防火墙", fillcolor="#FFFBEB", shape=diamond];
        lb [label="负载均衡\nF5", fillcolor="#FFFBEB"];
    }

    subgraph cluster_internal {
        label="内网"; style="dashed"; color="#10b981"; fontname="PingFang SC";
        app1 [label="应用服务器 1", fillcolor="#F0FDF4"];
        app2 [label="应用服务器 2", fillcolor="#F0FDF4"];
        db_master [label="DB Master", fillcolor="#F0FDF4"];
        db_slave [label="DB Slave", fillcolor="#F0FDF4"];
    }

    dns -> cdn -> fw;
    fw -> lb;
    lb -> app1;
    lb -> app2;
    app1 -> db_master;
    app2 -> db_master;
    db_master -> db_slave [label="主从复制", style=dashed];
}
```

### 15. Decision Tree 决策树

```dot
digraph decision_tree {
    rankdir=TB;
    node [fontname="PingFang SC", fontsize=11];
    edge [fontname="PingFang SC", fontsize=10, color="#64748b"];

    start [label="订单金额\n> 1000元?", shape=diamond, style="filled", fillcolor="#EFF6FF"];
    vip [label="VIP 客户?", shape=diamond, style="filled", fillcolor="#EFF6FF"];
    risk [label="风控评分\n> 80?", shape=diamond, style="filled", fillcolor="#EFF6FF"];

    auto [label="自动审批\n即时放行", shape=box, style="rounded,filled", fillcolor="#D1FAE5"];
    manual [label="人工审核\n1-2 工作日", shape=box, style="rounded,filled", fillcolor="#FFFBEB"];
    reject [label="拒绝\n通知客户", shape=box, style="rounded,filled", fillcolor="#FEF2F2"];
    senior [label="高级审批\n总监签字", shape=box, style="rounded,filled", fillcolor="#FAF5FF"];

    start -> vip [label="是"];
    start -> risk [label="否"];
    vip -> auto [label="是"];
    vip -> manual [label="否"];
    risk -> manual [label="是"];
    risk -> reject [label="否"];
    manual -> senior [label="金额>5000", style=dashed];
}
```

### 16. Dataflow 数据流图

```dot
digraph dataflow {
    rankdir=LR;
    node [shape=box, style="rounded,filled", fontname="PingFang SC", fontsize=11];
    edge [fontname="PingFang SC", fontsize=10, color="#64748b"];

    subgraph cluster_source {
        label="数据源"; style="dashed"; color="#3b82f6"; fontname="PingFang SC";
        mysql_src [label="MySQL\n业务库", fillcolor="#EFF6FF"];
        kafka [label="Kafka\n事件流", fillcolor="#EFF6FF"];
        api [label="外部 API\n第三方数据", fillcolor="#EFF6FF"];
    }

    subgraph cluster_process {
        label="数据处理"; style="dashed"; color="#8b5cf6"; fontname="PingFang SC";
        flink [label="Flink\n实时计算", fillcolor="#FAF5FF"];
        spark [label="Spark\n批处理", fillcolor="#FAF5FF"];
        etl [label="ETL\n数据清洗", fillcolor="#FAF5FF"];
    }

    subgraph cluster_storage {
        label="数据存储"; style="dashed"; color="#10b981"; fontname="PingFang SC";
        hive [label="Hive\n数据仓库", fillcolor="#F0FDF4"];
        es [label="Elasticsearch\n搜索索引", fillcolor="#F0FDF4"];
        redis [label="Redis\n实时缓存", fillcolor="#F0FDF4"];
    }

    subgraph cluster_output {
        label="数据应用"; style="dashed"; color="#f59e0b"; fontname="PingFang SC";
        bi [label="BI 报表", fillcolor="#FFFBEB"];
        recommend [label="推荐引擎", fillcolor="#FFFBEB"];
        monitor [label="监控告警", fillcolor="#FFFBEB"];
    }

    mysql_src -> etl;
    kafka -> flink;
    api -> etl;
    etl -> hive;
    etl -> spark;
    flink -> redis;
    flink -> es;
    spark -> hive;
    hive -> bi;
    es -> recommend;
    redis -> monitor;
}
```

### 17. Orgchart 组织结构图

```dot
digraph orgchart {
    rankdir=TB;
    node [shape=box, style="rounded,filled", fontname="PingFang SC", fontsize=11, fillcolor="#EFF6FF"];
    edge [color="#94A3B8"];

    ceo [label="CEO\n张三", fillcolor="#DBEAFE", penwidth=2];

    cto [label="CTO\n李四"];
    cpo [label="CPO\n王五"];
    cfo [label="CFO\n赵六"];

    fe_lead [label="前端负责人\n陈七", fillcolor="#F0FDF4"];
    be_lead [label="后端负责人\n周八", fillcolor="#F0FDF4"];
    pm [label="产品经理\n吴九", fillcolor="#FAF5FF"];
    designer [label="设计师\n郑十", fillcolor="#FAF5FF"];
    finance [label="财务\n孙一", fillcolor="#FFFBEB"];

    ceo -> cto;
    ceo -> cpo;
    ceo -> cfo;
    cto -> fe_lead;
    cto -> be_lead;
    cpo -> pm;
    cpo -> designer;
    cfo -> finance;
}
```

---

## 三、验证清单

| # | 图表类型 | DSL | 预期 |
|---|---------|-----|------|
| 1 | flowchart | Mermaid | 节点+箭头+判断分支正常 |
| 2 | sequence | Mermaid | 参与者+消息+alt块正常 |
| 3 | class | Mermaid | 类+属性+继承关系正常 |
| 4 | state | Mermaid | 状态+转换+起止符正常 |
| 5 | er | Mermaid | 实体+字段+关系线正常 |
| 6 | gantt | Mermaid | 时间轴+任务条+里程碑正常 |
| 7 | mindmap | Mermaid | 树形展开正常 |
| 8 | timeline | Mermaid | 时间点+事件正常 |
| 9 | c4 | Mermaid | 系统边界+关系正常 |
| 10 | sankey | Mermaid | 流带+标签正常 |
| 11 | journey | Mermaid | 阶段+评分+参与者正常 |
| 12 | architecture | Graphviz | 分层+分组+连线正常 |
| 13 | swimlane | Graphviz | 泳道分区+流程正常 |
| 14 | network | Graphviz | 拓扑分层+连线正常 |
| 15 | decision-tree | Graphviz | 判断节点+分支正常 |
| 16 | dataflow | Graphviz | 数据流向+分组正常 |
| 17 | orgchart | Graphviz | 树形层级+连线正常 |

**不支持 DSL 的图表**（继续走 PNG）：SWOT 图、鱼骨图、文氏图
