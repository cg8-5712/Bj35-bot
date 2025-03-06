from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import datetime

from handler import api
from handler.config import Config

def get_user(username, password):
    # 这里应该是实际的用户验证逻辑
    return username if username == "admin" and password == "password" else None

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = Config.jwt_secret_key()
jwt = JWTManager(app)

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


def robot_name_mapping(robot_id):
    mapping = {
        "1309143": "主教学楼一楼",
        "1309097": "办公楼三楼",
    }

    return mapping.get(robot_id[:7], "未知名称")


URI_PREFIX = '/api/v1'

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>API Server</title>
    </head>
    <body>
        <h1>Welcome to API Server</h1>
        <p>For more information, please visit <a href="https://github.com/cg8-5712/Bj35-bot/blob/main/Backend/python-backend/api/readme.md">Readme.md</a></p>
    </body>
    </html>
    """

@app.route(URI_PREFIX + '/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    rememberMe = request.json.get('rememberMe', False)

    if not username or not password:
        return jsonify(code=1, message="Missing username or password"), 422

    user = get_user(username, password)

    if user:
        if rememberMe:
            access_token = create_access_token(identity=user, expires_delta=datetime.timedelta(weeks=1))
        else:
            access_token = create_access_token(identity=user, expires_delta=datetime.timedelta(days=1))
        app.logger.info(f"User {username} logged in successfully")
        return jsonify(code=0, access_token=access_token)
    else:
        app.logger.error(f"User {username} login failed")
        return jsonify(code=1, message="Invalid username or password")

@app.route(URI_PREFIX + '/robot_list', methods=['GET'])
@jwt_required()
async def fetch_robot_list():
    try:
        # 获取所有设备
        device_list_response = await api.get_device_list()
        
        if device_list_response.get('code') != 0:
            return jsonify({'code': 1, 'message': device_list_response.get('message', 'Failed to get device list'), 'data': []})
        
        device_list = device_list_response.get('data', [])

        # 分类设备
        cabin_devices = []
        robot_devices = []

        for device in device_list:
            if device.get('deviceType') == 'CABIN':
                cabin_devices.append(device)
            else:
                robot_devices.append(device)

        # 创建机柜ID映射表
        cabin_map = {}
        for cabin in cabin_devices:
            cabin_id = cabin.get('deviceId')
            if cabin_id:
                # 假设机柜ID和机器人ID的前7位相匹配
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

            robot_data = {
                'id': robot_id,
                'name': robot_name_mapping(robot_id),
                'imageUrl': 'https://tailwindcss.com/plus-assets/img/logos/48x48/tuple.svg',  # 可以放一个默认图标路径
                'cabinId': cabin_id,
                'status': {
                    'isOnline': not device_status.get('isOffline', True),
                    'power': device_status.get('powerPercent', 0),
                    'message': data.get('message', '无信息'),
                    'status': '空闲' if device_status.get('isIdle', False) else '执行任务中',
                    'location': device_status.get('currentPositionMarker', '未知位置')
                }
            }

            robot_list.append(robot_data)

        return jsonify({
            'code': 0, 
            'message': 'Success', 
            'data': robot_list
        })

    except Exception as e:
        app.logger.error(f"Error fetching robot list: {str(e)}")
        return jsonify({'code': 1, 'message': str(e), 'data': []})

@app.route(URI_PREFIX + '/device_status/<int:device_id>', methods=['GET'])
@jwt_required()
async def fetch_device_status(device_id):
    device_status = await api.get_device_status(device_id)
    return jsonify(device_status)

@app.route(URI_PREFIX + '/device_task/<int:device_id>', methods=['GET'])
@jwt_required()
async def fetch_device_task(device_id):
    device_task = await api.get_device_task(device_id)
    return jsonify(device_task)

@app.route(URI_PREFIX + '/school-tasks', methods=['GET'])
@jwt_required()
async def fetch_school_tasks():
    school_tasks = await api.get_school_tasks()
    return jsonify(school_tasks)

@app.route(URI_PREFIX + '/cabin-position/<int:device_id>', methods=['GET'])
@jwt_required()
async def fetch_cabin_position(device_id):
    cabin_position = await api.get_cabin_position(device_id)
    return jsonify(cabin_position)

@app.route(URI_PREFIX + '/reset-cabin-position/<int:device_id>/<position>', methods=['PUT'])
@jwt_required()
async def reset_cabin_position(device_id, position):
    result = await api.reset_cabin_position(device_id, position)
    return jsonify(result)

@app.route(URI_PREFIX + '/running-task', methods=['GET'])
@jwt_required()
async def fetch_running_task():
    running_task = await api.get_running_task()
    return jsonify(running_task)

@app.route(URI_PREFIX + '/task/move-lift-down/<int:device_id>/<docking_marker>/<target>', methods=['POST'])
@jwt_required()
async def task_move_and_lift(device_id, docking_marker, target):
    result = await api.make_task_flow_move_and_lift_down(device_id, docking_marker, target)
    return jsonify(result)

@app.route(URI_PREFIX + '/task/docking-cabin-move/<int:device_id>/<target>', methods=['POST'])
@jwt_required()
async def task_dock_and_move(device_id, target):
    result = await api.make_task_flow_docking_cabin_and_move_target(device_id, target)
    return jsonify(result)

@app.route(URI_PREFIX + '/goto-charge/<int:device_id>', methods=['POST'])
@jwt_required()
async def goto_charge(device_id):
    result = await api.goto_charge(device_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
