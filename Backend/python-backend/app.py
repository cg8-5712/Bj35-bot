from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import datetime
import hashlib
import logging
from functools import wraps
from send_message.main import send_message
from handler import api
from handler.config import Config

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

def get_robot_name(robot_id):
    """根据机器人ID获取友好名称"""
    prefix = robot_id[:7] if len(robot_id) >= 7 else robot_id
    return ROBOT_LOCATION_MAPPING.get(prefix, f"Robot-{prefix}")

def get_user(username, password):
    """验证用户凭据"""
    expected_hash = hashlib.sha256("password".encode()).hexdigest()
    return username if username == "admin" and password == expected_hash else None

def create_app():
    """应用工厂函数，创建并配置Flask应用"""
    app = Flask(__name__)

    # 配置CORS和JWT
    CORS(app)
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
            return await func(*args, **kwargs)
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
    def login():
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        remember_me = request.json.get('rememberMe', False)

        if not username or not password:
            return jsonify(code=1, message="Missing username or password"), 422

        user = get_user(username, password)

        if user:
            # 创建访问令牌，可选择添加更多声明
            expires_delta = JWT_EXPIRY_REMEMBER if remember_me else JWT_EXPIRY_DEFAULT
            access_token = create_access_token(
                identity=user, 
                expires_delta=expires_delta,
                additional_claims={
                    'username': username,
                    'role': 'admin'  # 在实际应用中，角色应从数据库获取
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

    @app.route(URI_PREFIX + '/reset-cabin-position/<device_id>/<position>', methods=['PUT'])
    @jwt_required()
    @error_handler
    async def reset_cabin_position(device_id, position):
        """重置机柜位置"""
        result = await api.reset_cabin_position(device_id, position)
        return jsonify(result)
    
    # 任务相关路由
    @app.route(URI_PREFIX + '/school-tasks/<pagesize>/<currentpage>', methods=['GET'])
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

    @app.route(URI_PREFIX + '/task/move-lift-down/<device_id>/<docking_marker>/<target>', methods=['POST'])
    @jwt_required()
    @error_handler
    async def task_move_and_lift(device_id, docking_marker, target):
        """创建移动和升降任务"""
        result = await api.make_task_flow_move_and_lift_down(device_id, docking_marker, target)
        return jsonify(result)

    @app.route(URI_PREFIX + '/task/docking-cabin-move/<device_id>/<target>', methods=['POST'])
    @jwt_required()
    @error_handler
    async def task_dock_and_move(device_id, target):
        """创建对接机柜和移动任务"""
        result = await api.make_task_flow_docking_cabin_and_move_target(device_id, target)
        return jsonify(result)
    
    @app.route(URI_PREFIX + '/task/docking-cabin-move/<device_id>/<target>', methods=['POST'])
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
    async def send():
        data = request.json
        message = data.get('message')
        user_id = data.get('userId')
        await send_message(user_id, message)

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

# 辅助函数
async def process_robot_devices(device_list):
    """处理机器人设备列表"""
    # 分类设备
    cabin_devices = [device for device in device_list if device.get('deviceType') == 'CABIN']
    robot_devices = [device for device in device_list if device.get('deviceType') != 'CABIN']
    
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
            'id': robot_id,
            'name': get_robot_name(robot_id),
            'imageUrl': 'https://tailwindcss.com/plus-assets/img/logos/48x48/tuple.svg',
            'cabinId': cabin_id,
            'status': {
                'isOnline': not device_status.get('isOffline', True),
                'power': device_status.get('powerPercent', 0),
                'isCharging' : device_status.get('isCharging', False),
                'message': data.get('message', '无信息'),
                'status': '空闲' if device_status.get('isIdle', False) else '执行任务中',
                'location': device_status.get('currentPositionMarker', '未知位置')
            }
        }
        
        robot_list.append(robot_data)
    
    return robot_list

# 创建应用实例
app = create_app()

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=8080, debug=True)
