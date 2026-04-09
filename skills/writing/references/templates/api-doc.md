# API 文档模板

> 存放路径：`docs/guides/<服务名>-api.md`
> 每个接口必须有可直接复制执行的请求示例。

---

## 概览

- **服务名称**：
- **Base URL**：`https://api.example.com/v1`
- **认证方式**：Bearer Token / API Key / Cookie
- **响应格式**：JSON
- **通用错误码**：

| 错误码 | 含义 | 处理方式 |
|--------|------|---------|
| 400 | 请求参数错误 | 检查参数格式 |
| 401 | 未认证 | 重新登录获取 token |
| 403 | 无权限 | 检查用户角色 |
| 429 | 请求过频 | 降低请求频率 |
| 500 | 服务端错误 | 联系开发团队 |

---

## 接口列表

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/users` | 获取用户列表 |
| POST | `/users` | 创建用户 |

---

## 接口详情

### GET /users — 获取用户列表

**参数**：

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| page | query | number | 否 | 页码，默认 1 |
| limit | query | number | 否 | 每页条数，默认 20 |
| status | query | string | 否 | 筛选状态：active / inactive |

**请求示例**：

```bash
curl -X GET 'https://api.example.com/v1/users?page=1&limit=20' \
  -H 'Authorization: Bearer <token>'
```

**成功响应**（200）：

```json
{
  "data": [
    {
      "id": "u_123",
      "name": "张三",
      "email": "zhangsan@example.com",
      "status": "active",
      "created_at": "2026-01-15T08:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 156
  }
}
```

**错误响应**：

| 场景 | 状态码 | 响应 |
|------|--------|------|
| token 过期 | 401 | `{"error": "token_expired", "message": "请重新登录"}` |
