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


{
  "requestId": null,
  "code": 0,
  "message": "SUCCESS",
  "customerErrorMessage": null,
  "data": {
    "updated": 1740756570022,
    "missionKey": null,
    "deviceInfo": {
      "deviceId": "1309143264909201408",
      "deviceName": "SCSK08C0440100682",
      "deviceSerialNumber": "SCSK08C0440100682",
      "deviceType": "CABIN",
      "productId": "988138114524516352",
      "productName": "送物上舱",
      "storeId": "202413110921092704037166339072"
    },
    "deviceStatus": {
      "chargeId": "40300716",
      "isCharging": true,
      "isEmergentStop": false,
      "isIdle": true,
      "isOffline": false,
      "powerPercent": 100.0,
      "distance": -1.0,
      "relevanceId": "1309143200526635008",
      "relevanceKey": "WTHT08E03B0717090",
      "currentPositionMarker": "charge_point_1F_40300716",
      "deviceId": "1309143264909201408",
      "chargePileId": "40300716",
      "updated": "1740756570022",
      "floor": "1",
      "appVersion": "",
      "isExclusive": false,
      "mapName": "",
      "isSoftEstop": false,
      "actuatorStatus": "non_support",
      "chassisLiftState": "non_support_chassis_lift_state",
      "position": {
        "floor": "1",
        "orientation": {
          "w": 0.79,
          "x": 0.0,
          "y": 0.0,
          "z": -0.62
        },
        "pos": {
          "w": null,
          "x": 51.84,
          "y": -42.71,
          "z": 0.0
        }
      },
      "lockers": [
        {
          "id": "12",
          "status": "CLOSE"
        },
        {
          "id": "34",
          "status": "CLOSE"
        }
      ],
      "action": {
        "type": "",
        "name": "",
        "currentTarget": "",
        "taskId": "",
        "taskChannel": "unknown",
        "actionName": "",
        "actionType": "",
        "startTime": ""
      },
      "modules": [
        {
          "type": "chassis",
          "version": "1.1.50S"
        },
        {
          "type": "app",
          "version": ""
        },
        {
          "type": "executor",
          "version": "v1.8.7.9"
        }
      ],
      "planRoutes": [],
      "orientation": {
        "x": 0.0,
        "y": 0.0,
        "z": -0.62,
        "w": 0.79
      },
      "accessories": null
    }
  }
}
