---
name: env-troubleshoot
version: 1.0.0
last_updated: 2026-04-08
repository: https://github.com/312362115/claude
description: >
  环境排障技能：结构化排查开发环境问题。
  覆盖 Node.js/Python/Docker 环境、依赖安装失败、端口冲突、权限问题等。
  触发词：装不上、跑不起来、报错了、环境问题、npm install 失败、Docker 起不来、端口被占。
  触发场景：依赖安装失败、服务启动报错、Docker 构建失败、环境变量缺失、版本冲突。
  即使用户没有说"环境问题"，只要是开发环境配置/启动相关的报错，都应触发此技能。
---

# 环境排障（Env Troubleshoot）

> 环境问题的特点：每个人遇到的都不一样，但解决思路是一样的。
> 核心方法：读错误信息 → 定位问题类别 → 对症处理。

---

## 排障流程

```
环境报错
  │
  ├─ 1. 读错误信息（完整读，不跳过）
  ├─ 2. 分类问题
  ├─ 3. 按类别排查
  ├─ 4. 修复并验证
  └─ 5. 记录（如果是常见问题，建议加到项目 docs/guides/）
```

---

## 问题分类与排查

### 类别 1：依赖安装失败

**常见错误**：

| 错误特征 | 可能原因 | 排查步骤 |
|---------|---------|---------|
| `ERESOLVE unable to resolve` | npm 依赖版本冲突 | 1. 读冲突详情 2. `npm ls <冲突包>` 3. 确定哪个依赖要求了不兼容版本 |
| `node-gyp rebuild FAILED` | 原生模块编译失败 | 1. 检查 node 版本 2. 检查 Python/build-tools 3. `xcode-select --install`(macOS) |
| `EACCES permission denied` | 权限不足 | 1. 不要用 sudo 装 npm 2. 检查 npm 全局目录权限 3. 用 nvm 管理 node |
| `network timeout` | 网络问题 | 1. 检查代理设置 2. 切换镜像源 `npm config set registry` |
| `ModuleNotFoundError` (Python) | 包未安装或虚拟环境未激活 | 1. `which python` 确认解释器 2. 检查 venv 是否激活 3. `pip install -r requirements.txt` |

### 类别 2：服务启动失败

| 错误特征 | 可能原因 | 排查步骤 |
|---------|---------|---------|
| `EADDRINUSE :::3000` | 端口被占用 | `lsof -i :3000` 找到占用进程，kill 或换端口 |
| `Error: Cannot find module` | 模块缺失 | 1. `rm -rf node_modules && npm install` 2. 检查路径拼写 |
| `ECONNREFUSED 127.0.0.1:5432` | 依赖服务未启动 | 检查 DB/Redis/等依赖服务是否运行 |
| 环境变量相关错误 | .env 缺失或变量缺失 | 1. `cp .env.example .env` 2. 对照检查必填变量 |
| `SyntaxError: Unexpected token` | Node/TS 版本不匹配 | 检查 `node -v` 和 `engines` 字段，检查 tsconfig |

### 类别 3：Docker 问题

| 错误特征 | 可能原因 | 排查步骤 |
|---------|---------|---------|
| `Cannot connect to Docker daemon` | Docker 未启动 | 启动 Docker Desktop 或 `systemctl start docker` |
| `no space left on device` | 磁盘/Docker 空间不足 | `docker system prune` 清理无用镜像和容器 |
| `COPY failed: file not found` | Dockerfile 路径错误 | 检查 COPY 源路径相对于 build context |
| 构建卡在某一层 | 网络问题或依赖下载慢 | 检查 Docker 镜像源配置 |
| 容器启动后立即退出 | 启动命令出错 | `docker logs <container>` 看日志 |

### 类别 4：版本冲突

| 场景 | 排查步骤 |
|------|---------|
| Node.js 版本不对 | 1. `node -v` 2. 检查 `.nvmrc` 或 `engines` 3. `nvm use` 切换 |
| Python 版本不对 | 1. `python --version` 2. 检查 `pyproject.toml` 3. 用 pyenv 切换 |
| TypeScript 编译错误 | 1. 检查 `tsconfig.json` target 2. `npx tsc --version` |
| 全局工具版本冲突 | `which <tool>` 确认用的哪个，必要时用 npx 跑项目本地版本 |

### 类别 5：权限问题

| 场景 | 排查步骤 |
|------|---------|
| macOS 文件权限 | `ls -la` 检查权限，`chmod` 修复 |
| Git hook 没有执行权限 | `chmod +x .git/hooks/*` 或 `chmod +x .husky/*` |
| SSH key 权限 | `chmod 600 ~/.ssh/id_*`，`chmod 700 ~/.ssh` |

---

## 排障原则

- **先读错误信息**：80% 的环境问题，错误信息本身就包含了答案。不要跳过错误信息直接猜
- **从最简单的可能性开始**：先检查服务是否启动、端口是否对、环境变量是否配了，再深入
- **重现优先**：如果用户描述的错误不完整，先复现问题再排查
- **不要盲目清理**：`rm -rf node_modules` 是最后手段，不是第一步。先理解为什么出错
- **记录解法**：如果是项目特有的环境问题，建议用户加到 `docs/guides/` 或 README

---

## 通用排查命令速查

```bash
# Node.js 环境
node -v && npm -v              # 版本检查
npm ls --depth=0               # 已安装依赖
npm cache clean --force        # 清理缓存
npx envinfo                    # 环境信息汇总

# Python 环境
python --version && pip --version
which python                   # 确认解释器路径
pip list                       # 已安装包
python -m venv .venv && source .venv/bin/activate  # 创建虚拟环境

# 端口/进程
lsof -i :3000                  # 查端口占用
kill -9 <PID>                  # 杀进程

# Docker
docker ps -a                   # 所有容器
docker logs <container>        # 容器日志
docker system df               # 磁盘占用
docker system prune            # 清理

# 通用
echo $PATH                     # PATH 检查
env | grep -i proxy            # 代理设置
```
