from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import api
from config import Config

def get_user(username, password):
    # 这里应该是实际的用户验证逻辑
    return username if username == "admin" and password == "password" else None

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = "your_secret_key"  # 更改为安全的密钥
jwt = JWTManager(app)



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
        return jsonify(code=0, access_token=access_token), 200
    else:
        app.logger.error(f"User {username} login failed")
        return jsonify(code=1, message="Invalid username or password"), 401

@app.route(URI_PREFIX + '/devicelist', methods=['GET'])
#@jwt_required()
async def fetch_device_list():
    device_list = await api.get_device_list()
    return jsonify(device_list)

@app.route(URI_PREFIX + '/device_status/<int:device_id>', methods=['GET'])
#@jwt_required()
async def fetch_device_status(device_id):
    device_status = await api.get_device_status(device_id)
    return jsonify(device_status)

@app.route(URI_PREFIX + '/device_task/<int:device_id>', methods=['GET'])
#@jwt_required()
async def fetch_device_task(device_id):
    device_task = await api.get_device_task(device_id)
    return jsonify(device_task)

@app.route(URI_PREFIX + '/school-tasks', methods=['GET'])
#@jwt_required()
async def fetch_school_tasks():
    school_tasks = await api.get_school_tasks()
    return jsonify(school_tasks)

@app.route(URI_PREFIX + '/cabin-position/<int:device_id>', methods=['GET'])
#@jwt_required()
async def fetch_cabin_position(device_id):
    cabin_position = await api.get_cabin_position(device_id)
    return jsonify(cabin_position)

@app.route(URI_PREFIX + '/reset-cabin-position/<int:device_id>/<position>', methods=['PUT'])
#@jwt_required()
async def reset_cabin_position(device_id, position):
    result = await api.reset_cabin_position(device_id, position)
    return jsonify(result)

@app.route(URI_PREFIX + '/running-task', methods=['GET'])
#@jwt_required()
async def fetch_running_task():
    running_task = await api.get_running_task()
    return jsonify(running_task)

@app.route(URI_PREFIX + '/task/move-lift-down/<int:device_id>/<docking_marker>/<target>', methods=['POST'])
#@jwt_required()
async def task_move_and_lift(device_id, docking_marker, target):
    result = await api.make_task_flow_move_and_lift_down(device_id, docking_marker, target)
    return jsonify(result)

@app.route(URI_PREFIX + '/task/docking-cabin-move/<int:device_id>/<target>', methods=['POST'])
#@jwt_required()
async def task_dock_and_move(device_id, target):
    result = await api.make_task_flow_docking_cabin_and_move_target(device_id, target)
    return jsonify(result)

@app.route(URI_PREFIX + '/goto-charge/<int:device_id>', methods=['POST'])
#@jwt_required()
async def goto_charge(device_id):
    result = await api.goto_charge(device_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
