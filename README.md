# Bj35-bot

一个用于管理机器人的Web UI系统
看个乐呵，不一定对

## 项目背景
本项目旨在为Bj35机器人提供一个可视化的管理界面，方便用户配置和监控机器人状态。

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

1. 安装依赖：`yarn install`
2. 启动服务：`yarn dev`
3. 访问 `http://localhost:5173`

### 后端

1. 创建虚拟环境并激活：`python -m venv .venv && source .venv/bin/activate`
2. 安装依赖：`pip install -r requirements.txt`
3. 启动服务：`python src/python-backend/api/app.py`
4. 访问 `http://localhost:8080/api/v1`

## 相关文档
- [开发文档](docs/开发文档.md)
- [API文档](docs/api文档.txt)
- [集成接口文档](docs/云迹-UP机器人二次开发（集成）接口.pdf)
