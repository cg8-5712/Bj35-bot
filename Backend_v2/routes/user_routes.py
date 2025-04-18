from quart import jsonify, request
from quart_jwt_extended import jwt_required

from utils import error_handler

from services import UserService

from settings import settings

URI_PREFIX = settings.URI_PREFIX

def register_routes(app):
    """注册用户信息相关路由"""

    @app.route(URI_PREFIX + '/get_user_profile', methods=['GET'])
    @jwt_required
    # @error_handler
    async def get_user_profile():
        username = request.args.get('username')
        print(f"username: {username}")
        info = await UserService.get_userinfo_by_username(username, 'name')

        print(f'info: {info}')
        print(type(info))
        return jsonify(info), 200

    @app.route(URI_PREFIX + '/post_user_profile', methods=['POST'])
    @jwt_required
    @error_handler
    async def post_user_profile():
        data = await request.json

        # # 验证邮箱地址，如果需要
        # if key.lower() == "email address":
        #     if not validate_email(value):
        #         return jsonify({'success': False, 'message': 'Invalid email address.'}), 400
        #     print(f"A verification email has been sent to {value}.")

        # 调用update_user_profile方法并传入编辑后的字段和值
        update_response = await UserService.update_userinfo(data)
        # update_response = {"success": True}

        # 根据API返回的数据进行处理
        if update_response['success']:
            print("Profile updated successfully!")
            return jsonify(
                {'success': True, 'message': 'Profile updated successfully!'}), 200

        else:
            return jsonify(
                {'success': False, 'message': update_response['message']}), 400

    @app.route(URI_PREFIX + '/post_user_avatar', methods=['POST'])
    @error_handler
    @jwt_required
    async def post_user_avatar():
        data = await request.json
        print(data)
        update_response = {"success": True}

        # 根据API返回的数据进行处理
        if update_response['success']:
            print("Profile updated successfully!")
            return jsonify(
                {'success': True, 'message': 'Profile updated successfully!'}), 200

        else:
            return jsonify(
                {'success': False, 'message': update_response['message']}), 400
