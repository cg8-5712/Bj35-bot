正在收集工作区信息# Bj35-Bot 后端系统文档

## 1. 系统架构概览

### 1.1 架构图

```
┌──────────────┐      ┌───────────────┐      ┌────────────────┐
│              │      │               │      │                │
│  前端应用    │━━━━━▶│  后端API服务  │━━━━━▶│  云迹机器人    │
│              │      │               │      │                │
└──────────────┘      └───────┬───────┘      └────────────────┘
                              │
                              ▼
                      ┌───────────────┐      ┌────────────────┐
                      │               │      │                │
                      │  数据持久层   │      │  企业微信服务  │
                      │               │      │                │
                      └───────────────┘      └────────────────┘
```

### 1.2 技术栈

- **Web框架**: Quart (异步Flask)
- **数据库**: PostgreSQL
- **认证**: JWT + 企业微信OAuth
- **运行时**: Python 3.11+
- **容器化**: Docker
- **任务调度**: APScheduler
- **第三方集成**: 云迹机器人API、企业微信API

## 2. 核心模块

### 2.1 模块结构

- **app.py**: 应用入口点和配置
- **routes/**: API路由定义
  - robot_routes.py: 机器人相关API
  - task_routes.py: 任务流程API
  - auth_routes.py: 认证相关API
  - message_routes.py: 消息通知API
  - user_routes.py: 用户管理API
- **services/**: 业务逻辑层
  - token_manager.py: 令牌管理
  - user_service.py: 用户服务
  - wecom_service.py: 企业微信服务
- **utils/**: 工具函数
  - yunji_api.py: 云迹API封装
  - decorators.py: 装饰器
  - exceptions.py: 自定义异常
  - jwt_handlers.py: JWT处理
- **settings.py**: 全局配置

### 2.2 关键函数

| 函数名 | 位置 | 功能描述 |
|--------|------|---------|
| `RUN` | yunji_api.py | 执行机器人任务流程的主函数，处理任务执行和状态循环检查 |
| `check` | yunji_api.py | 检查机器人状态，循环等待状态变化 |
| `make_task_flow_dock_cabin_and_move_target_with_wait_action` | yunji_api.py | 执行到舱-举升-到点位-等待任务流 |
| `process_robot_devices` | robot_routes.py | 处理机器人设备数据，格式化响应 |

## 3. API 参考

### 3.1 机器人操作 API

| 端点 | 方法 | 描述 | 参数 |
|------|-----|------|------|
| `/api/v1/robot_list` | GET | 获取所有机器人列表 | 无 |
| `/api/v1/device_status/{device_id}` | GET | 获取设备状态 | device_id: 设备ID |
| `/api/v1/cabin-position/{device_id}` | GET | 获取机柜位置 | device_id: 设备ID |
| `/api/v1/reset-cabin-position/{device_id}/{position}` | PUT | 重置机柜位置 | device_id: 设备ID, position: 新位置 |
| `/api/v1/run-task` | POST | 执行任务 | cabin_id: 舱ID, locations: 位置列表 |

### 3.2 响应格式

成功响应格式:
```json
{
  "code": 0,
  "message": "Success",
  "data": [...]
}
```

错误响应格式:
```json
{
  "code": 1,
  "message": "错误描述信息"
}
```

### 3.3 状态码

| 代码 | 描述 |
|------|------|
| 0 | 成功 |
| 1 | 一般错误 |
| 4001 | 参数错误 |
| 4003 | 权限不足 |
| 5001 | 服务器错误 |

## 4. 任务流实现

### 4.1 任务流类型

系统实现了以下云迹机器人任务流:

1. **到上舱-举升-到点位-放下** (`dock_cabin_to_move_and_lift_down`)
   - 调整底盘去某个上舱并移动到另外点位放下

2. **到上舱-举升-到点位** (`docking_cabin_and_move_target`)
   - 调整底盘移动上舱并移动到目标点

3. **到上舱-举升-到点位-等待** (`dock_cabin_and_move_target_with_wait_action`)
   - 让机器人到某舱到某个地点并等待

### 4.2 任务执行流程图

```
┌────────────┐     ┌────────────┐     ┌────────────┐
│            │     │            │     │            │
│  接收任务  │────▶│  执行任务  │────▶│ 状态循环检查│
│            │     │            │     │            │
└────────────┘     └────────────┘     └─────┬──────┘
                                            │
┌────────────┐     ┌────────────┐     ┌─────▼──────┐
│            │     │            │     │            │
│  返回结果  │◀────│ 处理下一任务│◀────│ 等待状态变化│
│            │     │            │     │            │
└────────────┘     └────────────┘     └────────────┘
```

### 4.3 机器人状态检查

任务执行过程中进行状态检查循环，检测"open"和"close"状态变化来确定任务完成。代码片段:

```python
flag = False  # 标记是否完成一次开门关门，关门为False，开门为True
while True:
    res = await check(cabin_id)
    if res == "open":
        flag = True
    if res == "close" and flag is True:
        break
    await asyncio.sleep(1)
```

## 5. 部署指南

### 5.1 环境要求

- Python 3.11+
- PostgreSQL
- Docker (可选)

### 5.2 配置文件 

从`.env.example`复制创建`.env`文件，包含:

```
ENV=development
URI_PREFIX=/api/v1
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=password
YUNJI_ACCESS_KEY_ID=your_access_key_id_here
YUNJI_STORE_ID=your_store_id_here
YUNJI_SECRET_KEY=your_secret_key_here
WECOM_CORP_ID=your_corp_id_here
WECOM_AGENT_ID=your_agent_id_here
WECOM_SECRET=your_secret_here
```

### 5.3 Docker部署

```bash
# 构建镜像
docker build -t bj35-bot-backend .

# 运行容器
docker run -d -p 8080:8080 --env-file .env --name bj35-backend bj35-bot-backend
```

### 5.4 直接部署

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行应用
hypercorn app:app --bind 0.0.0.0:8080
```

## 6. 安全措施

### 6.1 认证机制

- **JWT认证**: 所有API请求需要JWT令牌
- **企业微信认证**: 支持企业微信OAuth登录

### 6.2 数据安全

- **敏感数据加密**: 使用对称加密保护令牌和密钥
- **错误处理装饰器**: 统一异常处理和日志记录
- **参数验证**: 使用Pydantic进行输入验证

### 6.3 通信安全

- **HTTPS**: 生产环境必须使用HTTPS
- **签名验证**: 对云迹API的请求进行签名验证

## 7. 重构注意事项

当前版本为重构中的项目，主要需要改进的部分:

1. **代码优化**:
   - 减少`yunji_api.py`中的重复HTTP请求模式
   - 拆分`RUN`函数为更小的专注函数

2. **错误处理**:
   - 增加重试机制
   - 超时处理改进
   - 详细错误记录

3. **测试覆盖**:
   - 添加单元测试
   - 添加集成测试

4. **文档完善**:
   - 更新API文档
   - 添加每个函数的详细注释

5. **安全审查**:
   - 进行全面的安全审核
   - 实现更完善的日志系统

---

*文档版本: v0.9 (重构中)*
*最后更新: 2025-04-19*
