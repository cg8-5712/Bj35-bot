import pytest
from quart import Quart
from Backend.routes.task_routes import register_routes
from Backend.utils import yunji_api

@pytest.fixture
def app():
    app = Quart(__name__)
    register_routes(app)
    return app

@pytest.mark.asyncio
async def test_run_task_success(app):
    # 获取真实设备列表
    device_list = await yunji_api.get_device_list()
    if device_list.get('code') != 0:
        pytest.skip("无法获取设备列表，跳过测试")
    
    # 获取所有CABIN类型的设备
    cabin_devices = [
        device for device in device_list.get('data', []) 
        if device.get('deviceType') == 'CABIN'
    ]
    if not cabin_devices:
        pytest.skip("没有找到CABIN设备，跳过测试")

    # 创建测试客户端
    test_client = app.test_client()

    # 对每个CABIN设备执行测试
    for cabin in cabin_devices:
        test_device_id = cabin['deviceId']
        
        # 执行run_task请求
        response = await test_client.post(
            f'/api/run-task/{test_device_id}',
            json={"locations": ["Y103", "Y102"]}
        )
        
        # 验证响应状态码
        assert response.status_code == 200
        
        # 验证响应内容
        response_data = await response.get_json()
        assert response_data["code"] == 0
        
        # 验证fetch_school_tasks结果
        school_tasks = await yunji_api.get_school_tasks(10, 1)
        assert school_tasks.get("code") == 0
        for task in school_tasks.get("data", []):
            assert task.get("status") == "success"

@pytest.mark.asyncio
async def test_run_task_empty_locations(app):
    # 获取真实设备列表
    device_list = await yunji_api.get_device_list()
    if device_list.get('code') != 0:
        pytest.skip("无法获取设备列表，跳过测试")
    
    # 获取所有CABIN类型的设备
    cabin_devices = [
        device for device in device_list.get('data', []) 
        if device.get('deviceType') == 'CABIN'
    ]
    if not cabin_devices:
        pytest.skip("没有找到CABIN设备，跳过测试")

    # 创建测试客户端
    test_client = app.test_client()

    # 对每个CABIN设备执行测试
    for cabin in cabin_devices:
        test_device_id = cabin['deviceId']
        
        # 执行run_task请求，locations为空
        response = await test_client.post(
            f'/api/run-task/{test_device_id}',
            json={"locations": []}
        )
        
        # 验证响应状态码
        assert response.status_code == 200
        
        # 验证响应内容包含错误信息
        response_data = await response.get_json()
        assert response_data["code"] == 1
        assert "位置列表不能为空" in response_data["message"]