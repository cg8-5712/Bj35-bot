"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-04-19
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547

本文件是 Bj35 Bot v2 的路由模块的初始化文件。
"""

from . import index, auth_routes, robot_routes, task_routes, user_routes, message_routes

def register_all_routes(app):
    """注册所有路由到应用实例"""
    index.register_routes(app)
    auth_routes.register_routes(app)
    robot_routes.register_routes(app)
    task_routes.register_routes(app)
    user_routes.register_routes(app)
    message_routes.register_routes(app)
