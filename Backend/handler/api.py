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

async def make_task_flow_dock_cabin_and_move_target_with_wait_action(device_id,target,overtime):
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
                "overtime": overtime,
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

async def get_device_by_id(device_id):
    """根据设备ID获取设备对象"""
     # 实现略，可从数据库或设备管理服务获取
    return {"id": device_id, "type": "robot"}

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

async def check(device_id):
    res=await get_device_status(device_id)
    status=[res["data"]["deviceStatus"]["lockers"][0]["status"], res["data"]["deviceStatus"]["lockers"][1]["status"]]
    if "OPEN" in status:
        return "open"
    elif status==["CLOSE", "CLOSE"]:
        return "close"

async def RUN(locations, device_id):
    """执行任务流

    Args:
        locations: 位置列表，包含机器人需要到达的目标位置
        device_id: 需要执行任务的机器人设备ID

    Returns:
        dict: 包含执行结果的状态码和消息
    """
    import logging
    logger = logging.getLogger(__name__)

    try:
        if not locations:
            return {'code': 1, 'message': '位置列表不能为空'}

        logger.info(f'开始执行任务流，设备ID: {device_id}, 位置列表: {locations}')

        # 执行每个位置的任务
        task_results = []
        for idx, location in enumerate(locations):
            logger.info(f'执行第 {idx + 1} 个任务，目标位置: {location}')

            try:
                # 获取设备对象
                device = await get_device_by_id(device_id)
                if not device:
                    raise ValueError(f"找不到设备ID: {device_id}")

                # 执行任务
                res = await make_task_flow_dock_cabin_and_move_target_with_wait_action(device_id, location, 300)

                flag = False  # 标记是否完成一次开门关门 关门为 False 开门为 True
                task_results.append(res)
                logger.info(f'位置 {location} 任务执行结果: {res}')
                while True:
                    res = await check(device_id)
                    if res == "open":
                        flag = True

                    if res == "close" and flag == True:
                        return {'code': 0, 'message': f'任务流执行成功，设备ID: {device_id}, 位置列表: {locations}'}
                    await asyncio.sleep(1)



            except Exception as e:
                logger.error(f'位置 {location} 任务执行失败: {str(e)}')
                return {'code': 1, 'message': f'任务执行失败: {str(e)}'}

    except Exception as e:
        logger.error(f'任务流执行失败: {str(e)}')
        return {'code': 1, 'message': f'任务流执行失败: {str(e)}'}


if __name__ == '__main__':
    device_bot1_cabin = 1309143264909201408
    print(asyncio.run(get_device_list()))
    # print("位置在:\n",asyncio.run(get_cabin_position(device_bot1_cabin)))
    # res = asyncio.run(make_task_flow_dock_cabin_and_move_target_with_wait_action(device_bot1_cabin, "Y103", 200))
    # print("请求结果:\n",res)
    # time.sleep(20)
    #
    # # print("位置在:\n", asyncio.run(get_cabin_position(device_bot1_cabin)))
    # res=asyncio.run(make_task_flow_dock_cabin_and_move_target_with_wait_action(device_bot1_cabin, "Y102",200))
    # print("请求结果:\n",res)
    # time.sleep(20)
    #
    # # print("位置在:\n", asyncio.run(get_cabin_position(device_bot1_cabin)))
    # res = asyncio.run(make_task_flow_dock_cabin_and_move_target_with_wait_action(device_bot1_cabin, "Q103",5))
    # print("请求结果:\n", res)
    # # time.sleep(60)
    # asyncio.run(make_task_flow_dock_cabin_and_move_target_with_wait_action(device_bot1_cabin, "一层作业柜", 5))
    # list = []
    # while True:
    #     s=input("请输入目标位置:")
    #     if s=="exit":
    #         break
    #     list.append(s)
    # asyncio.run(RUN(list))
    # print("查询任务:\n",asyncio.run(get_school_tasks(3,1)))

    # for i in range(10):
    #     asyncio.run(sleep(5))
    #     res1 = asyncio.run(get_cabin_position(device_bot1_cabin))
    #     print("\n", res1)
    #     # res1 = asyncio.run(make_task_flow_dock_cabin_and_move_target_with_wait_action(device_bot1_cabin, "Y102"))
    #     # print(res1)
    #     res1 = asyncio.run(get_device_status(device_bot1_cabin))
    #     print("\nstatus:\n", res1)
    #     res1 = asyncio.run(get_device_task(device_bot1_cabin))
    #     print("\ntask:\n", res1)

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