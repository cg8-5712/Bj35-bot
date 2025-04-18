"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-04-19
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547

本文件定义了一些自定义异常类，用于处理不同的错误情况。
"""

class DatabaseConnectionError(Exception):
    """自定义异常类，用于处理数据库连接错误"""

class UpdateTokenError(Exception):
    """自定义异常类，用于处理更新token时的错误"""

