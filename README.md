# Bj35-bot

一个用于管理机器人的Web UI系统  

**请正确对待自己的代码，不要随意更改代码随意 Push 导致版本管理
**在正确对待自己代码的同时，也请关注别人的代码，在还未确定哪份代码有问题的时候请到群中询问、交流，请不要随意删改他人代码，谢谢！**

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
2. 进入 `Backend` 目录
3. 安装依赖：`pip install -r requirements.txt`
4. 启动服务：`python ./app.py`
5. 访问 `http://localhost:8080/api/v1`

## 相关文档

- [开发文档](docs/开发文档.md)
- [API文档](docs/api文档.txt)
- [集成接口文档](docs/云迹-UP机器人二次开发（集成）接口.pdf)
