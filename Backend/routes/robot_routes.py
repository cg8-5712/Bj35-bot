from quart import jsonify
from quart_jwt_extended import jwt_required

import handler.api as api
from handler.config import Config

from utils.decorators import error_handler

URI_PREFIX = Config.URI_PREFIX

def register_routes(app):
    """注册设备和机器人相关路由"""

    @app.route(URI_PREFIX + '/robot_list', methods=['GET'])
    @jwt_required
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
    @jwt_required
    @error_handler
    async def fetch_device_status(device_id):
        """获取单个设备的状态"""
        device_status = await api.get_device_status(device_id)
        return jsonify(device_status)

    @app.route(URI_PREFIX + '/device_task/<device_id>', methods=['GET'])
    @jwt_required
    @error_handler
    async def fetch_device_task(device_id):
        """获取单个设备的任务"""
        device_task = await api.get_device_task(device_id)
        return jsonify(device_task)

    @app.route(URI_PREFIX + '/cabin-position/<device_id>', methods=['GET'])
    @jwt_required
    @error_handler
    async def fetch_cabin_position(device_id):
        """获取机柜位置"""
        cabin_position = await api.get_cabin_position(device_id)
        return jsonify(cabin_position)

    @app.route(URI_PREFIX +
               '/reset-cabin-position/<device_id>/<position>', methods=['PUT'])
    @jwt_required
    @error_handler
    async def reset_cabin_position(device_id, position):
        """重置机柜位置"""
        result = await api.reset_cabin_position(device_id, position)
        return jsonify(result)

# 机器人位置名称映射
ROBOT_LOCATION_MAPPING = {
    "1309143": "主教学楼一楼",
    "1309097": "办公楼三楼",
}

def get_robot_name(robot_id):
    """根据机器人ID获取友好名称"""
    prefix = robot_id[:7] if len(robot_id) >= 7 else robot_id
    return ROBOT_LOCATION_MAPPING.get(prefix, f"Robot-{prefix}")

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