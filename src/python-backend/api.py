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

if __name__ == '__main__':
    device_bot1_cabin = Config().deviceId
    print(device_bot1_cabin)
    res = asyncio.run(get_device_status(device_bot1_cabin))
    # res = asyncio.run(get_device_list())
    print(res)
