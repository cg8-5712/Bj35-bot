from flask import Flask, jsonify
from flask_cors import CORS
from functools import wraps
from flask import request
import jwt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config, api

app = Flask(__name__)
CORS(app)
cfg = config.Config()


from functools import wraps
from flask import request, jsonify

def token_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        token = request.headers.get('Token')
        # print(token)
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        if token != cfg.inside_token:
            return jsonify({'message': 'Token is invalid!'}), 403

        return await f(*args, **kwargs)

    return decorated


@app.route('/api/v1/accessToken')
@token_required
async def get_access_token():
    return jsonify({'accessToken': cfg.accessToken})

@app.route('/api/v1/deviceInfo')
@token_required
async def get_device_info():
    device_info = await api.get_device_list()
    # print(device_info)
    return jsonify(device_info)

@app.route('/api/v1/device_status/<int:device_id>')
@token_required
async def get_device_status(device_id):
    device_status = await api.get_device_status(device_id)
    return jsonify(device_status)

@app.route('/api/v1/device_task/<int:device_id>')
@token_required
async def get_device_task(device_id):
    data = {
        'start': "2025-01-01"
    }
    device_task = await api.get_device_task(device_id, data)
    return jsonify(device_task)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)