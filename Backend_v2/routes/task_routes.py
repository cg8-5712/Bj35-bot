from quart import jsonify, request
from quart_jwt_extended import jwt_required

from utils import yunji_api
from utils import error_handler

from settings import settings

URI_PREFIX = settings.URI_PREFIX

def register_routes(app):
    """注册任务相关路由"""

    @app.route(URI_PREFIX + '/school-tasks/<pagesize>/<currentpage>',
               methods=['GET'])
    @jwt_required
    @error_handler
    async def fetch_school_tasks(pagesize, currentpage):
        """获取学校任务"""
        school_tasks = await yunji_api.get_school_tasks(pagesize, currentpage)
        no = 1
        for task in school_tasks.get('data', []):
            task['no'] = no
            no += 1
        return jsonify(school_tasks)

    @app.route(URI_PREFIX + '/running-task', methods=['GET'])
    @jwt_required
    @error_handler
    async def fetch_running_task():
        """获取正在运行的任务"""
        running_task = await yunji_api.get_running_task()
        return jsonify(running_task)

    @app.route(URI_PREFIX +
               '/task/move-lift-down/<device_id>/<docking_marker>/<target>', methods=['POST'])
    @jwt_required
    @error_handler
    async def task_move_and_lift(device_id, docking_marker, target):
        """创建移动和升降任务"""
        result = await yunji_api.make_task_flow_move_and_lift_down(device_id, docking_marker, target)
        return jsonify(result)

    @app.route(URI_PREFIX +
               '/task/docking-cabin-move/<device_id>/<target>', methods=['POST'])
    @jwt_required
    @error_handler
    async def task_dock_and_move(device_id, target):
        """创建对接机柜和移动任务"""
        result = await yunji_api.make_task_flow_docking_cabin_and_move_target(device_id, target)
        return jsonify(result)

    @app.route(URI_PREFIX +
               '/task/docking-cabin-move/<device_id>/<target>', methods=['POST'])
    @jwt_required
    @error_handler
    async def task_dock_and_back(device_id, target):
        """创建back任务"""
        result = await yunji_api.make_task_flow_dock_cabin_and_move_target_with_wait_action(device_id, target, False)
        return jsonify(result)

    @app.route(URI_PREFIX + '/goto-charge/<device_id>', methods=['POST'])
    @jwt_required
    @error_handler
    async def goto_charge(device_id):
        """让机器人去充电"""
        result = await yunji_api.goto_charge(device_id)
        return jsonify(result)
    
    @app.route(URI_PREFIX + '/run-task/<device_id>', methods=['POST'])
    @jwt_required
    @error_handler
    async def run_task(device_id):
        """执行任务流"""
        data = await request.json
        locations = data.get('locations', [])

        # 调用RUN函数
        run_result = await yunji_api.RUN(locations, device_id)

        # 根据执行结果返回响应
        return jsonify(run_result)

    @app.route(URI_PREFIX + '/target-list', methods=['GET'])
    @jwt_required
    @error_handler
    async def fetch_target_list():
        target_list = settings.TARGET_LIST
        return target_list
