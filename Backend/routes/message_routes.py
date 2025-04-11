from quart import jsonify, request
from quart_jwt_extended import jwt_required

from handler.PostgreSQLConnector import PostgreSQLConnector
from utils.decorators import error_handler

from utils.config import Config

from send_message.main import send


URI_PREFIX = Config.uri_prefix()

def register_routes(app):
    """注册消息相关路由"""
    
    @app.route(URI_PREFIX + '/send-message', methods=['POST'])
    @jwt_required
    @error_handler
    async def send_message():
        data = await request.json
        message = data.get('message')
        username = data.get('username')  # 获取用户名

        # 从数据库中获取用户信息
        user_info = await PostgreSQLConnector.get_userinfo_by_username(username, 'name')

        if user_info and 'wecom_id' in user_info:
            user_id = user_info['wecom_id']  # 获取 wecom_id 作为 user_id
            await send(user_id, message)  # 发送消息
            return jsonify({'code': 0, 'message': '消息发送成功'}), 200
        else:
            return jsonify({'code': 1, 'message': '未找到用户或用户信息不完整'}), 404


    @app.route(URI_PREFIX + '/send_message_to_user', methods=['POST'])
    @jwt_required
    @error_handler
    async def send_message_to_user():
        data = await request.json
        user = data.get('user')
        message = data.get('message')