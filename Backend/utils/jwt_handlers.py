from quart import jsonify

def configure_jwt_handlers(jwt):
    """配置JWT错误处理器"""

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'code': 401,
            'message': '令牌已过期，请重新登录'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return jsonify({
            'code': 401,
            'message': '无效的令牌'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        return jsonify({
            'code': 401,
            'message': '未提供令牌，请先登录'
        }), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({
            'code': 401,
            'message': '需要新的令牌，请重新登录'
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'code': 401,
            'message': '令牌已被撤销'
        }), 401