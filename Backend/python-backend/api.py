from urllib import response

from config import Config
import aiohttp
import asyncio
import uuid
import time
import json

access_token = Config().accessToken
# print(access_token)

def create_headers():
    signatureNonce = str(uuid.uuid4())
    headers = {'signatureNonce': signatureNonce,
               'timestamp': str(time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.gmtime())),
               'accessKeyId': str(Config().accessKeyId),
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

async def get_school_task():
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        params = {'storeIds': '202413110921092704037166339072',
                  'pageSize': '20',
                  'current': '1'}
        async with session.get(f'https://open-api.yunjiai.cn/v3/rcs/task/list', params=params) as response:
            return json.loads(await response.text())

async def get_device_position(device_id):
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/robot/{device_id}/position') as response:
            return json.loads(await response.text())

async def get_running_task(storeId):
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/rcs/task/running-task/list', json={'storeId': storeId}) as response:
            return json.loads(await response.text())

# async def get_running_task_list(storeId):
#     headers = create_headers()
#     async with aiohttp.ClientSession(headers=headers) as session:
#         async with session.get(f'https://open-api.yunjiai.cn/v3/rcs/task/running-task/list', json={'storeId': storeId}) as response:
#             return json.loads(await response.text())

async def make_task_flow(target):
    headers = create_headers()
    data = {
  # "outTaskId": "53c593e7-766d-4646-8b58-0b795ded0ed6",
  "templateId": "dock_cabin_and_move_target_with_wait_action",
  "storeId": "202413110921092704037166339072",
  "params": {
    "dockCabinId": "1309143264909201408",
    # "chassisId": "3949399854845849594854",
    "target": target,
    "overtime": 30,
    "overtimeEvent": "down",
    "startVoice": "",
    "endVoice": ""
  }
}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f'https://open-api.yunjiai.cn/v3/rcs/task/flow/execute', json=data) as response:
            return json.loads(await response.text())

async def make_task_flow_move_and_lift(target):
    headers = create_headers()
    data = {
  # "outTaskId": "53c593e7-766d-4646-8b58-0b795ded0ed6",
  "templateId": "dock_cabin_to_move_and_lift_down",
  "storeId": "202413110921092704037166339072",
  "params": {
    "dockCabinId": "1309143264909201408",
    # "chassisId": "3949399854845849594854",
    "target": target,
    "overtime": 30,
    "overtimeEvent": "down",
    "startVoice": "",
    "endVoice": ""
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
    # res = asyncio.run(get_device_position(device_bot1_cabin))
    # print(res)
    # print(asyncio.run(get_school_task()))
    # res = asyncio.run(make_task_flow())
    # print(res)
    res = asyncio.run(make_task_flow())
    print(res)