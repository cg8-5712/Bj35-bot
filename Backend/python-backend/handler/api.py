from urllib import response

from config import Config
import aiohttp
import asyncio
import uuid
import time
import json

access_token = Config.accessToken()
# print(access_token)

def create_headers():
    # 创建请求头，包含签名随机数、时间戳、访问密钥ID和访问令牌
    signatureNonce = str(uuid.uuid4())
    headers = {'signatureNonce': signatureNonce,
               'timestamp': str(time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.gmtime())),
               'accessKeyId': str(Config.accessKeyId()),
               'token': str(access_token)}
    return headers

async def get_device_list():
    # 异步获取设备列表
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/device/list?accessToken%3D{access_token}') as response:
            return json.loads(await response.text())

async def get_device_status(device_id):
    # 异步获取指定设备的状态
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/robot/{device_id}/status?accessToken%3D{access_token}') as response:
            return json.loads(await response.text())

async def get_device_task(device_id):
    # 异步获取指定设备的任务列表
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/robots/{device_id}/tasks') as response:
            return json.loads(await response.text())

async def get_school_tasks(pageSize, current):
    # 异步获取学校任务列表，支持分页
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        params = {'storeIds': Config.store_Id(),
                  'pageSize': pageSize,
                  'current': current}
        async with session.get(f'https://open-api.yunjiai.cn/v3/rcs/task/list', params=params) as response:
            return json.loads(await response.text())

async def get_cabin_position(device_id):
    # 异步获取指定设备的仓位位置
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/robot/{device_id}/position') as response:
            return json.loads(await response.text())

async def reset_cabin_position(device_id, position):
    # 异步重置指定设备的仓位位置
    headers = create_headers()
    data = {"marker": position}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.put(f'https://open-api.yunjiai.cn/v3/robot/up/cabin/{device_id}/reset-position', json=data) as response:
            return json.loads(await response.text())

async def get_running_task():
    # 异步获取正在运行的任务列表
    headers = create_headers()
    storeId = Config.store_Id()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/rcs/task/running-task/list', json={'storeId': storeId}) as response:
            return json.loads(await response.text())

# async def get_running_task_list(storeId):
#     # 异步获取指定storeId的正在运行的任务列表
#     headers = create_headers()
#     async with aiohttp.ClientSession(headers=headers) as session:
#         async with session.get(f'https://open-api.yunjiai.cn/v3/rcs/task/running-task/list', json={'storeId': storeId}) as response:
#             return json.loads(await response.text())

async def make_task_flow_move_target_and_lift_down(device_id, target):
    # 异步创建任务流，移动到指定目标并放下货柜
    headers = create_headers()
    data = {
          "outTaskId": str(uuid.uuid4()),
          "templateId": "dock_cabin_and_move_target_and_lift_down",
          "storeId": Config.store_Id(),
          "params": {
            "dockCabinId": device_id,
            "target": target
  }
}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f'https://open-api.yunjiai.cn/v3/rcs/task/flow/execute', json=data) as response:
            return json.loads(await response.text())

async def make_task_flow_docking_cabin_and_move_target(device_id,target):
    # 异步创建任务流，对接货柜并移动到指定目标
    headers = create_headers()
    data = {
              "outTaskId": str(uuid.uuid4()),
              "templateId": "docking_cabin_and_move_target",
              "storeId": Config.store_Id(),
              "params": {
                "dockCabinId": device_id,
                # "chassisId": "3949399854845849594854",
                "target": target
              }
            }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f'https://open-api.yunjiai.cn/v3/rcs/task/flow/execute', json=data) as response:
            return json.loads(await response.text())

async def make_task_flow_dock_cabin_and_move_target_with_wait_action(device_id,target):
    # 异步创建任务流，对接货柜并移动到指定目标，支持等待操作
    headers = create_headers()
    data = {
              "outTaskId": str(uuid.uuid4()),
              "templateId": "dock_cabin_and_move_target_with_wait_action",
              "storeId": Config.store_Id(),
              "params": {
                "dockCabinId": device_id,
                # "chassisId": "3949399854845849594854",
                "target": target,
                "overtime": 200,
                "overtimeEvent": "back"
              }
            }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f'https://open-api.yunjiai.cn/v3/rcs/task/flow/execute', json=data) as response:
            return json.loads(await response.text())

async def make_task_flow_move_and_lift_down(device_id,dockingMarker, target):
    # 异步创建任务流，移动到指定目标并放下货柜
    headers = create_headers()
    data = {
              "outTaskId": str(uuid.uuid4()),
              "templateId": "dock_cabin_to_move_and_lift_down",
              "storeId": Config.store_Id(),
              "params": {
              "dockCabinId": device_id,
              "target": target
              }
}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f'https://open-api.yunjiai.cn/v3/rcs/task/flow/execute', json=data) as response:
            return json.loads(await response.text())

async def goto_charge(device_id):
    # 异步发送指令使设备移动到充电站
    headers = create_headers()
    data = {"chargeId": ""}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f'https://open-api.yunjiai.cn/v3/robot/{device_id}/goto-charge', json=data) as response:
            return json.loads(await response.text())

async def sleep(time):
    # 异步休眠指定时间
    await asyncio.sleep(time)

if __name__ == '__main__':
    device_bot1_cabin = 1309143264909201408
    res = asyncio.run(make_task_flow_dock_cabin_and_move_target_with_wait_action(device_bot1_cabin, "Y103"))
    print(res)
    for i in range(10):
        asyncio.run(sleep(5))
        res1 = asyncio.run(get_cabin_position(device_bot1_cabin))
        print("\n", res1)
        # res1 = asyncio.run(make_task_flow_dock_cabin_and_move_target_with_wait_action(device_bot1_cabin, "Y102"))
        # print(res1)
        res1 = asyncio.run(get_device_status(device_bot1_cabin))
        print("\nstatus:\n", res1)
        res1 = asyncio.run(get_device_task(device_bot1_cabin))
        print("\ntask:\n", res1)

    # print(asyncio.run(get_running_task()))
    # res = asyncio.run(make_task_flow_docking_cabin_and_move_target(device_bot1_cabin, "charge_point_1F_40300716"))
    # print(res)
    # print(device_bot1_cabin)
    # res = asyncio.run(get_cabin_position(device_bot1_cabin))
    # print(res)
    # res = asyncio.run(get_device_list())
    # print(res)
    # print(asyncio.run(get_school_tasks()))
    # print(asyncio.run(reset_cabin_position(device_bot1_cabin, "charge_point_1F_40300716")))
    # res = asyncio.run(make_task_flow())
    # print(res)
    # res = asyncio.run(make_task_flow())
    # print(res)
    # print(Config.store_Id())
    # res = asyncio.run(make_task_flow_move_target_with_wait_action(device_bot1_cabin, "Y103"))
    # print(res)
    # res = asyncio.run(get_device_status(device_bot1_cabin))
    # print(res)
    # res = asyncio.run(make_task_flow_docking_cabin_and_move_target(device_bot1_cabin, ""))
    # print(res)
    # print(asyncio.run(goto_charge(device_bot1_cabin)))
    # print(asyncio.run(make_task_flow_move_and_lift_down(device_bot1_cabin, "")))
