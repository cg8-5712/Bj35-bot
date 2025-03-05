from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from flask import Flask, jsonify
from flask_cors import CORS
from functools import wraps
from flask import request
import datetime
import logging
# import jwt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
URI_PREFIX = "/api/v1"

import config, api
cfg = config

app = Flask(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
app.config['JWT_SECRET_KEY'] = "cfg.SECRET_KEY"

jwt_manager = JWTManager(app)
CORS(app)

# def token_required(f):
#     @wraps(f)
#     async def decorated(*args, **kwargs):
#         token = request.headers.get('Authorization')
#         if not token:
#             return jsonify({'message': 'Token is missing!'}), 403
#         try:
#             # 去掉Bearer前缀，只保留token本身
#             token = token.split(" ")[1]
#             # 解码JWT
#             data = jwt.decode(token, cfg.SECRET_KEY, algorithms=["HS256"])
#         except jwt.ExpiredSignatureError:
#             return jsonify({'message': 'Token has expired!'}), 403
#         except jwt.InvalidTokenError:
#             return jsonify({'message': 'Token is invalid!'}), 403
#         return await f(*args, **kwargs)
#
#     return decorated

def get_user(username, password):
    if username == "test" and password == "test":
        return {username: password}
    else:
        return False

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
@jwt_required()
def get_device_list():
    device_list = api.get_device_list()
    return jsonify(device_list)

@app.route(URI_PREFIX + '/device_status/<int:device_id>', methods=['GET'])
@jwt_required()
async def get_device_status(device_id):
    device_status = await api.get_device_status(device_id)
    return jsonify(device_status)

@app.route(URI_PREFIX + '/device_task/<int:device_id>')
@jwt_required()
async def get_device_task(device_id):
    data = {
        'start': "2025-01-01"
    }
    device_task = await api.get_device_task(device_id, data)
    return jsonify(device_task)

@app.route(URI_PREFIX + '/school-tasks', methods=['GET'])
@jwt_required()
async def get_school_tasks():
    school_tasks = await api.get_school_tasks()
    return jsonify(school_tasks)

@app.route(URI_PREFIX + '/cabin-position/<int:task_id>', methods=['GET'])
@jwt_required()
async def get_cabin_position(task_id):
    cabin_position = await api.get_cabin_position(task_id)
    return jsonify(cabin_position)

@app.route(URI_PREFIX + '/running-task', methods=['GET'])
@jwt_required()
async def get_running_task():
    running_task = await api.get_running_task()
    return jsonify(running_task)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
