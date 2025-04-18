"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-04-19
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547

本文件定义了JWT错误处理器的配置函数。
"""

from quart import jsonify

def configure_jwt_handlers(jwt):
    """配置JWT错误处理器"""

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        del jwt_header, jwt_payload
        return jsonify({
            'code': 401,
            'message': '令牌已过期，请重新登录'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        del error_string
        return jsonify({
            'code': 401,
            'message': '无效的令牌'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        del error_string
        return jsonify({
            'code': 401,
            'message': '未提供令牌，请先登录'
        }), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        del jwt_header, jwt_payload
        return jsonify({
            'code': 401,
            'message': '需要新的令牌，请重新登录'
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        del jwt_header, jwt_payload
        return jsonify({
            'code': 401,
            'message': '令牌已被撤销'
        }), 401
