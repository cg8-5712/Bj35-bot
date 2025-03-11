# Bj35-bot

![版本](https://img.shields.io/badge/版本-0.1.0--alpha-blue)
![Node.js](https://img.shields.io/badge/Node.js-v16+-green)
![开发状态](https://img.shields.io/badge/状态-开发中-yellow)

一个用于管理机器人的Web UI系统  
看个乐呵，不一定对

## 项目背景

本项目旨在为 Bj35 机器人提供一个可视化的管理界面，方便用户配置和监控机器人状态。

## 主要功能

- 机器人状态监控
- 消息发送管理
- 系统配置管理
- 访问令牌管理

## 技术栈

- 前端：Vite + Vue3
- 后端：Python Flask
- 数据库：SQLite

## 快速开始

### 前端

#### 前置条件

1. 安装 Node.js 22.0.0 或更高版本
2. 启用 Corepack: `corepack enable`
3. 确认 Yarn 已安装：`yarn --version`

#### 步骤

1. 安装依赖：`yarn install`
2. 复制 `.env.examples` 为 `.env.development`
3. 启动服务：`yarn dev`
4. 访问 `http://localhost:5173`

### 后端

1. 创建虚拟环境并激活：`python -m venv .venv && source .venv/bin/activate`
2. 安装依赖：`pip install -r requirements.txt`
3. 启动服务：`python Backend/python-backend/app.py`
4. 访问 `http://localhost:8080/api/v1`

### 项目结构
```
BJ35-BOT
├─Backend
│  ├─python-backend
│  │  │  .env
│  │  │  app.py
│  │  │  readme.md
│  │  │  
│  │  └─handler
│  │     │  accessToken.py
│  │     │  api.py
│  │     └─  config.py
│  │          
│  └─Send-message
│      │  API receives messages.py
│      │  API send messages test.py
│      │  main.py
│      │  
│      └─weworkapi_python
│              ierror.py
│              README.md
│              Readme.txt
│              WXBizJsonMsgCrypt.py
│              WXBizMsgCrypt.py
│              WXBizMsgCrypt3.py
│              
├─docs
│      api文档.txt
│      develop_project.md
│      云迹-UP机器人二次开发（集成）接口.pdf
│      代码逻辑.md
│      代码逻辑.png
│      任务流调度.md
│      前端要加的东西.md
│      开发文档.md
│      开发计划（白板）.jpg
│      
└─Frontend
    │  .env.development
    │  .gitignore
    │  index.html
    │  LICENSE
    │  package.json
    │  README.md
    │  vite.config.js
    │  yarn.lock
    │    
    ├─public
    │      vite.svg
    │      
    └─src
        │  App.vue
        │  main.js
        │  style.css
        │  
        ├─assets
        │      favicon.svg
        │      vue.svg
        │      
        ├─components
        │  ├─common
        │  │      LoadingSpinner.vue
        │  │      MessageInfo.vue
        │  │      
        │  └─dashboard
        │          Overview.vue
        │          RobotDetail.vue
        │          TaskBoard.vue
        │          TaskPublish.vue
        │          
        ├─router
        │      index.js
        │      
        ├─services
        │      ApiServices.js
        │      AuthService.js
        │      NotificationService.js
        │      
        └─views
                Dashboard.vue
                Login.vue
                NotFound.vue
```

## 相关文档

- [开发文档](docs/开发文档.md)
- [API文档](docs/api文档.txt)
- [集成接口文档](docs/云迹-UP机器人二次开发（集成）接口.pdf)
