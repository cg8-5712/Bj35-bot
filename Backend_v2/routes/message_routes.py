from quart import jsonify, request
from quart_jwt_extended import jwt_required

from utils import error_handler

from services import UserService
from services.send_message import send

from settings import settings


URI_PREFIX = settings.URI_PREFIX

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
        user_info = await UserService.get_userinfo_by_username(username, 'name')

        if user_info and 'wecom_id' in user_info:
            user_id = user_info['wecom_id']  # 获取 wecom_id 作为 user_id
            await send(user_id, message)  # 发送消息
            return jsonify({'code': 0, 'message': '消息发送成功'}), 200

        return jsonify({'code': 1, 'message': '未找到用户或用户信息不完整'}), 404
