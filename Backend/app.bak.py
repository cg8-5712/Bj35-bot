# -*- coding: utf-8 -*-
import asyncio
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import datetime
import hashlib
import logging
from functools import wraps
import time

from handler.PostgreSQLConnector import PostgreSQLConnector
from send_message.main import send
from handler import api
from handler.config import Config
from handler.PostgreSQLConnector import PostgreSQLConnector
from handler.accessToken import update_access_token

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 常量定义
URI_PREFIX = '/api/v1'
JWT_EXPIRY_REMEMBER = datetime.timedelta(weeks=1)
JWT_EXPIRY_DEFAULT = datetime.timedelta(days=1)

# 机器人位置名称映射
ROBOT_LOCATION_MAPPING = {
    "1309143": "主教学楼一楼",
    "1309097": "办公楼三楼",
}


def find_kind_by_username(string, values):
    for value, kind in values:
        if value == string:
            return string, kind
    return None


def get_robot_name(robot_id):
    """根据机器人ID获取友好名称"""
    prefix = robot_id[:7] if len(robot_id) >= 7 else robot_id
    return ROBOT_LOCATION_MAPPING.get(prefix, f"Robot-{prefix}")


async def get_user(username, password):
    """验证用户凭据"""
    return await PostgreSQLConnector.verify_user_credentials(username, password)

async def get_user_info(username, kind):
    return await PostgreSQLConnector.get_userinfo_by_username(username, kind)


def create_app():
    """应用工厂函数，创建并配置Flask应用"""
    app = Flask(__name__)

    # 配置CORS和JWT
    CORS(app, resources={
        r"/api/*": {"origins": ["http://localhost:5173"], "methods": ["GET", "POST", "PUT", "DELETE"]}
    })
    app.config["JWT_SECRET_KEY"] = Config.jwt_secret_key()
    jwt = JWTManager(app)

    # 配置JWT错误处理器
    configure_jwt_handlers(jwt)

    # 注册路由
    register_routes(app)

    return app


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


def error_handler(func):
    """异常处理装饰器"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            response = await func(*args, **kwargs)
            response_json = response.get_json()
            if response_json.get('code') == 11013:
                logging.error(f"Authentication failed in {func.__name__}: {response_json}")
                await update_access_token()
                return jsonify(response_json), response.status_code
            return response
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            return jsonify({'code': 1, 'message': str(e), 'data': []}), 500

    return wrapper


def register_routes(app):
    """注册所有API路由"""

    # 首页
    @app.route('/')
    def index():
        return """
        <html>
        <head>
            <title>BJ35-Bot API Server</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #333; border-bottom: 1px solid #eee; padding-bottom: 10px; }
                a { color: #0066cc; }
            </style>
        </head>
        <body>
            <h1>Welcome to BJ35-Bot API Server</h1>
            <p>This server provides APIs for controlling and monitoring robots.</p>
            <p>For more information, please visit
               <a href="https://github.com/cg8-5712/Bj35-bot/blob/main/Backend/python-backend/api/readme.md">
               Readme.md</a>
            </p>
        </body>
        </html>
        """

    # 认证相关路由
    @app.route(URI_PREFIX + '/login', methods=['POST'])
    async def login():
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        remember_me = request.json.get('rememberMe', False)

        if not username or not password:
            return jsonify(code=1, message="Missing username or password"), 422

        user = await get_user(username, password)
        print(user)
        if user:
            user_info = await get_user_info(user[0], user[1])
            # 创建访问令牌，可选择添加更多声明
            expires_delta = JWT_EXPIRY_REMEMBER if remember_me else JWT_EXPIRY_DEFAULT
            access_token = create_access_token(
                identity=user[0],
                expires_delta=expires_delta,
                additional_claims={
                    'username': user_info['name'],
                    'role': user_info['department'],  # 在实际应用中，角色应从数据库获取
                }
            )
            app.logger.info(f"User {username} logged in successfully")
            return jsonify(code=0, access_token=access_token)
        else:
            app.logger.error(f"User {username} login failed")
            return jsonify(code=1, message="Invalid username or password")

    # 设备和机器人相关路由
    @app.route(URI_PREFIX + '/robot_list', methods=['GET'])
    @jwt_required()
    @error_handler
    async def fetch_robot_list():
        """获取格式化的机器人列表及其状态"""
        # 获取所有设备
        device_list_response = await api.get_device_list()

        if device_list_response.get('code') != 0:
            return jsonify({
                'code': 1,
                'message': device_list_response.get('message', 'Failed to get device list'),
                'data': []
            })

        # 处理设备数据
        device_list = device_list_response.get('data', [])
        robot_list = await process_robot_devices(device_list)

        return jsonify({
            'code': 0,
            'message': 'Success',
            'data': robot_list
        })

    @app.route(URI_PREFIX + '/device_status/<device_id>', methods=['GET'])
    @jwt_required()
    @error_handler
    async def fetch_device_status(device_id):
        """获取单个设备的状态"""
        device_status = await api.get_device_status(device_id)
        return jsonify(device_status)

    @app.route(URI_PREFIX + '/device_task/<device_id>', methods=['GET'])
    @jwt_required()
    @error_handler
    async def fetch_device_task(device_id):
        """获取单个设备的任务"""
        device_task = await api.get_device_task(device_id)
        return jsonify(device_task)

    @app.route(URI_PREFIX + '/cabin-position/<device_id>', methods=['GET'])
    @jwt_required()
    @error_handler
    async def fetch_cabin_position(device_id):
        """获取机柜位置"""
        cabin_position = await api.get_cabin_position(device_id)
        return jsonify(cabin_position)

    @app.route(URI_PREFIX +
               '/reset-cabin-position/<device_id>/<position>', methods=['PUT'])
    @jwt_required()
    @error_handler
    async def reset_cabin_position(device_id, position):
        """重置机柜位置"""
        result = await api.reset_cabin_position(device_id, position)
        return jsonify(result)

    # 任务相关路由
    @app.route(URI_PREFIX + '/school-tasks/<pagesize>/<currentpage>',
               methods=['GET'])
    @jwt_required()
    @error_handler
    async def fetch_school_tasks(pagesize, currentpage):
        """获取学校任务"""
        school_tasks = await api.get_school_tasks(pagesize, currentpage)
        no = 100
        for task in school_tasks.get('data', []):
            task['no'] = no
            no -= 1
        return jsonify(school_tasks)

    @app.route(URI_PREFIX + '/running-task', methods=['GET'])
    @jwt_required()
    @error_handler
    async def fetch_running_task():
        """获取正在运行的任务"""
        running_task = await api.get_running_task()
        return jsonify(running_task)

    @app.route(URI_PREFIX +
               '/task/move-lift-down/<device_id>/<docking_marker>/<target>', methods=['POST'])
    @jwt_required()
    @error_handler
    async def task_move_and_lift(device_id, docking_marker, target):
        """创建移动和升降任务"""
        result = await api.make_task_flow_move_and_lift_down(device_id, docking_marker, target)
        return jsonify(result)

    @app.route(URI_PREFIX +
               '/task/docking-cabin-move/<device_id>/<target>', methods=['POST'])
    @jwt_required()
    @error_handler
    async def task_dock_and_move(device_id, target):
        """创建对接机柜和移动任务"""
        result = await api.make_task_flow_docking_cabin_and_move_target(device_id, target)
        return jsonify(result)

    @app.route(URI_PREFIX +
               '/task/docking-cabin-move/<device_id>/<target>', methods=['POST'])
    @jwt_required()
    @error_handler
    async def task_dock_and_back(device_id, target):
        """创建back任务"""
        result = await api.make_task_flow_dock_cabin_and_move_target_with_wait_action(device_id, target)
        return jsonify(result)

    @app.route(URI_PREFIX + '/goto-charge/<device_id>', methods=['POST'])
    @jwt_required()
    @error_handler
    async def goto_charge(device_id):
        """让机器人去充电"""
        result = await api.goto_charge(device_id)
        return jsonify(result)

    @app.route(URI_PREFIX + '/send-message', methods=['POST'])
    @jwt_required()
    @error_handler
    async def send_message():
        data = request.json
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

    @app.route(URI_PREFIX + '/run-task/<device_id>', methods=['POST'])
    @jwt_required()
    @error_handler
    async def run_task(device_id):
        """执行任务流"""
        data = request.json
        locations = data.get('locations', [])

        # 调用RUN函数
        run_result = await api.RUN(locations, device_id)

        # 根据执行结果返回响应
        return jsonify(run_result)

    @app.route(URI_PREFIX + '/target-list', methods=['GET'])
    @jwt_required()
    @error_handler
    async def fetch_target_list():
        target_list = Config.target_list()
        return target_list

    @app.route(URI_PREFIX + '/get_user_profile', methods=['GET'])
    @jwt_required()
    @error_handler
    async def get_user_profile():
        username = request.args.get('username')
        print(username)
        info = await PostgreSQLConnector.get_userinfo_by_username(username, 'name')
        print(info)
        print(type(info))
        return jsonify(info), 200

    @app.route(URI_PREFIX + '/send_message_to_user', methods=['POST'])
    @jwt_required()
    @error_handler
    async def send_message_to_user():
        data = request.json
        user = data.get('user')
        message = data.get('message')

    @app.route(URI_PREFIX + '/post_user_profile', methods=['POST'])
    @jwt_required()
    @error_handler
    async def post_user_profile():
        data = request.json

        # # 验证邮箱地址，如果需要
        # if key.lower() == "email address":
        #     if not validate_email(value):
        #         return jsonify({'success': False, 'message': 'Invalid email address.'}), 400
        #     print(f"A verification email has been sent to {value}.")

        # 调用update_user_profile方法并传入编辑后的字段和值
        update_response = await PostgreSQLConnector.update_userinfo(data)
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
    @jwt_required()
    @error_handler
    async def post_user_avatar():
        data = request.json
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


# 辅助函数
async def process_robot_devices(device_list):
    """处理机器人设备列表"""
    # 分类设备
    cabin_devices = [
        device for device in device_list if device.get('deviceType') == 'CABIN']
    robot_devices = [
        device for device in device_list if device.get('deviceType') != 'CABIN']

    # 创建机柜ID映射表
    cabin_map = {}
    for cabin in cabin_devices:
        cabin_id = cabin.get('deviceId')
        if cabin_id:
            prefix = cabin_id[:7] if len(cabin_id) >= 7 else cabin_id
            cabin_map[prefix] = cabin_id

    # 获取机器人状态并格式化数据
    robot_list = []

    for robot in robot_devices:
        robot_id = robot.get('deviceId')
        if not robot_id:
            continue

        # 获取机器人状态
        device_status_response = await api.get_device_status(robot_id)

        # 查找匹配的机柜ID
        cabin_id = None
        for prefix, cabinet_id in cabin_map.items():
            if robot_id.startswith(prefix):
                cabin_id = cabinet_id
                break

        # 提取相关数据并格式化
        data = device_status_response.get('data', {})
        device_status = data.get('deviceStatus', {})

        print(device_status)

        robot_data = {
            'deviceId': cabin_id,
            'name': get_robot_name(robot_id),
            'imageUrl': 'https://tailwindcss.com/plus-assets/img/logos/48x48/tuple.svg',
            'cabinId': cabin_id,
            'status': {
                'isOnline': not device_status.get('isOffline', True),
                'power': device_status.get('powerPercent', 0),
                'isCharging': device_status.get('isCharging', False),
                'message': data.get('message', '无信息'),
                'status': '空闲' if device_status.get('isIdle', False) else '执行任务中',
                'location': device_status.get('currentPositionMarker', '未知位置')
            }
        }

        robot_list.append(robot_data)

    return robot_list

async def check_token():
    """
    检查access token是否在当天过期，如果是则更新。
    """
    try:
        expiration_ts = float(Config.expire_time())
        expire_date = datetime.datetime.fromtimestamp(expiration_ts)
        today = datetime.datetime.now().date()
        if expire_date.date() == today:
            logging.info("Access token将在今天过期，开始生成新的access token。")
            result = await update_access_token()
            if result:
                logging.info("新的access token生成成功。")
            else:
                logging.error(f"生成新的access token失败：{result}")
    except Exception as e:
        logging.error(f"检查或更新access token时出错：{str(e)}")

def log_token_expiry():
    """启动时获取expiration并记录距离过期的天数"""
    try:
        expiration_ts = float(Config.expire_time())
        current_ts = time.time()
        days_remaining = (expiration_ts - current_ts) / (60 * 60 * 24)
        logging.info(f"Access token将在 {days_remaining:.0f} 天后过期。")
    except Exception as e:
        logging.error(f"获取token过期时间失败：{str(e)}")

# 创建应用实例
app = create_app()
loop = asyncio.get_event_loop()

async def init_db():
    try:
        await PostgreSQLConnector.initialize()
    except Exception as e:
        logging.critical(f"数据库初始化失败，应用将退出: {e}")
        exit(1)

loop.run_until_complete(init_db())

if __name__ == '__main__':
    log_token_expiry()

    # 启动时先执行一次检查任务
    loop.create_task(check_token())

    # 启动Web应用
    app.run(host='0.0.0.0', port=8080, debug=True)
