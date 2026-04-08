# 开发指南模板

> 存放路径：`docs/guides/<主题>.md`
> 步骤可直接照做，命令可直接复制执行。

---

## 前置条件

- 环境要求（Node.js 版本、Python 版本等）
- 需要安装的工具
- 需要的权限/账号

## 环境搭建

### 第一步：克隆项目

```bash
git clone <repo-url>
cd <project>
```

### 第二步：安装依赖

```bash
npm install  # 或 pip install -r requirements.txt
```

### 第三步：配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入以下配置：
# DATABASE_URL=...
# API_KEY=...
```

### 第四步：启动服务

```bash
npm run dev
# 访问 http://localhost:3000
```

## 核心概念

对项目中重要的概念、模式、约定做简要说明，帮助新人建立心智模型。

## 目录结构

```
src/
├── api/        # API 路由
├── services/   # 业务逻辑
├── models/     # 数据模型
└── utils/      # 工具函数
```

## 开发约定

- 代码风格、命名规范
- Git 分支策略
- 提交规范

## 常见问题

### Q: <问题描述>

**原因**：...
**解决方式**：

```bash
<修复命令>
```
