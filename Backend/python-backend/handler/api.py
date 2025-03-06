from urllib import response

from .config import Config
import aiohttp
import asyncio
import uuid
import time
import json

access_token = Config.accessToken()
# print(access_token)

def create_headers():
    signatureNonce = str(uuid.uuid4())
    headers = {'signatureNonce': signatureNonce,
               'timestamp': str(time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.gmtime())),
               'accessKeyId': str(Config.accessKeyId()),
               'token': str(access_token)}
    return headers

async def get_device_list():
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/device/list?accessToken%3D{access_token}') as response:
            return json.loads(await response.text())

async def get_device_status(device_id):
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/robot/{device_id}/status?accessToken%3D{access_token}') as response:
            return json.loads(await response.text())

async def get_device_task(device_id):
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/robots/{device_id}/tasks') as response:
            return json.loads(await response.text())

async def get_school_tasks():
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        params = {'storeIds': Config.store_Id(),
                  'pageSize': '20',
                  'current': '1'}
        async with session.get(f'https://open-api.yunjiai.cn/v3/rcs/task/list', params=params) as response:
            return json.loads(await response.text())

async def get_cabin_position(device_id):
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/robot/{device_id}/position') as response:
            return json.loads(await response.text())

async def reset_cabin_position(device_id, position):
    headers = create_headers()
    data = {"marker": position}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.put(f'https://open-api.yunjiai.cn/v3/robot/up/cabin/{device_id}/reset-position', json=data) as response:
            return json.loads(await response.text())

async def get_running_task():
    headers = create_headers()
    storeId = Config.store_Id()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/rcs/task/running-task/list', json={'storeId': storeId}) as response:
            return json.loads(await response.text())

# async def get_running_task_list(storeId):
#     headers = create_headers()
#     async with aiohttp.ClientSession(headers=headers) as session:
#         async with session.get(f'https://open-api.yunjiai.cn/v3/rcs/task/running-task/list', json={'storeId': storeId}) as response:
#             return json.loads(await response.text())

async def make_task_flow_move_target_and_lift_down(device_id, target):
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
    headers = create_headers()
    data = {
              "outTaskId": str(uuid.uuid4()),
              "templateId": "docking_cabin_and_move_target",
              "storeId": Config.store_Id(),
              "params": {
                "dockCabinId": device_id,
                "chassisId": "3949399854845849594854",
                "target": target
              }
            }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f'https://open-api.yunjiai.cn/v3/rcs/task/flow/execute', json=data) as response:
            return json.loads(await response.text())

async def make_task_flow_move_and_lift_down(device_id,dockingMarker, target):
    headers = create_headers()
    data = {
              "outTaskId": str(uuid.uuid4()),
              "templateId": "dock_cabin_to_move_and_lift_down",
              "storeId": Config.store_Id(),
              "params": {
                "dockCabinId": device_id,
                "dockingCabinMarker": dockingMarker,
                "target": target
              }
}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f'https://open-api.yunjiai.cn/v3/rcs/task/flow/execute', json=data) as response:
            return json.loads(await response.text())

async def goto_charge(device_id):
    headers = create_headers()
    data = {"chargeId": ""}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f'https://open-api.yunjiai.cn/v3/robot/{device_id}/goto-charge', json=data) as response:
            return json.loads(await response.text())

if __name__ == '__main__':
    device_bot1_cabin = 1309143264909201408

    # print(device_bot1_cabin)
    # res = asyncio.run(get_cabin_position(device_bot1_cabin))
    # print(res)
    # res = asyncio.run(get_device_list())
    # print(res)
    # print(asyncio.run(get_school_tasks()))
    # print(asyncio.run(reset_cabin_position(device_bot1_cabin)))
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