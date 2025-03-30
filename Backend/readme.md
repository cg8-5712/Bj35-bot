# API Documentation

## Overview
This API provides authentication and device management functionalities, allowing users to log in and interact with various devices through a set of endpoints.

## Base URL
```
http://ip:8080/api/v1
```

## Authentication
The API uses JSON Web Tokens (JWT) for authentication. To access protected routes, include the token in the `Authorization` header as follows:
```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication
#### Login
**Endpoint:**
```
POST /api/v1/login
```
**Request Body:**
```json
{
    "username": "admin",
    "password": "password",
    "rememberMe": true
}
```
**Response:**
```json
{
    "code": 0,
    "access_token": "your_jwt_token"
}
```

### Device Management
#### Get Device List
**Endpoint:**
```
GET /api/v1/devicelist
```
**Authorization:** JWT Required
**Response:**
```json
[
    {
      "requestId": "********-****-****-****-************",
      "code": 0,
      "message": "操作成功",
      "current": 1,
      "pageSize": 50,
      "total": 100,
      "data": [
        {
          "deviceId": "713074929695854592",
          "deviceName": "TEST100002",
          "deviceSerialNumber": "TEST100002",
          "deviceType": "RSASS",
          "productId": "713826588470415360",
          "productName": "Name"
    }
  ]
}
]
```

#### Get Device Status
**Endpoint:**
```
GET /api/v1/device_status/{device_id}
```
**Authorization:** JWT Required
**Response:**
```json
{
  "code": 0,
  "customerErrorMessage": null,
  "data": {
    "deviceInfo": {
      "deviceId": "",
      "deviceName": "",
      "deviceSerialNumber": "",
      "deviceType": "CABIN",
      "productId": "",
      "productName": "\u9001\u7269\u4e0a\u8231",
      "storeId": ""
    },
    "deviceStatus": {
      "accessories": null,
      "action": {
        "actionName": "",
        "actionType": "",
        "currentTarget": "",
        "name": "",
        "startTime": "",
        "taskChannel": "unknown",
        "taskId": "",
        "type": ""
      },
      "actuatorStatus": "non_support",
      "appVersion": "",
      "chargeId": "（（（（（（（（（（（（",
      "chargePileId": "4****",
      "chassisLiftState": "non_support_chassis_lift_state",
      "currentPositionMarker": "charge_point_3F_********",
      "deviceId": "*************",
      "distance": -1.0,
      "floor": "3",
      "isCharging": true,
      "isEmergentStop": false,
      "isExclusive": false,
      "isIdle": true,
      "isOffline": false,
      "isSoftEstop": false,
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
      "mapName": "zx",
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
      "orientation": {
        "w": 1.0,
        "x": 0.0,
        "y": 0.0,
        "z": 0.07
      },
      "planRoutes": [],
      "position": {
        "floor": "3",
        "orientation": {
          "w": 1.0,
          "x": 0.0,
          "y": 0.0,
          "z": 0.07
        },
        "pos": {
          "w": null,
          "x": 45.46,
          "y": 74.93,
          "z": 0.0
        }
      },
      "powerPercent": 100.0,
      "relevanceId": "******************",
      "relevanceKey": "*****************",
      "updated": "1741185720017"
    },
    "missionKey": null,
    "updated": 1741185720017
  },
  "message": "SUCCESS",
  "requestId": null
}
```

#### Get Device Task
**Endpoint:**
```
GET /api/v1/device_task/{device_id}
```
**Authorization:** JWT Required
**Response:**
(There may be some things going wrong.)
```json
{
  "code": 0,
  "current": 1,
  "customerErrorMessage": null,
  "data": [],
  "message": "SUCCESS",
  "pageSize": 50,
  "requestId": null,
  "total": 0
}
```

#### Get Cabin Position
**Endpoint:**
```
GET /api/v1/cabin_position/{device_id}
```
**Authorization:** JWT Required
**Response:**
```json
{
  "code": 200,
  "customerErrorMessage": null,
  "data": {
    "deviceId": "",
    "deviceName": "",
    "position": "charge_point_3F_4****96"
  },
  "message": null,
  "requestId": null
}
```
#### Reset Cabin Position
**Endpoint:**
```
POST /api/v1/reset_cabin_position/{device_id}
```
**Authorization:** JWT Required
**Response:**
```json
{
  "code": 0,
  "message": "SUCCESS"
}
```

### Task Management

#### Get School Task List
**Endpoint:**
```
GET /api/v1/school-tasks
```
**Authorization:** JWT Required
**Response:**
```json
{
  "code": 0,
  "message": "SUCCESS",
  "data": [
    {
      "taskId": "13492984781983409943",
      "createdAt": 1660492245810,
      "updatedAt": 1660492295810,
      "status": "SUCCESS",
      "taskType": "SENT_UP",
      "attach": "",
      "storeId": "******",
      "outTaskId": "13492984781983409943",
      "target": "101",
      "extra": {
        "phone": "13212341234",
        "goods": [
          {
            "goodsId": "***********",
            "outGoodsId": "out_goods_id_001",
            "goodsName": "******",
            "quantity": 1
          }
        ]
      }
    }
  ],
  "pageSize": 20,
  "current": 1
}
```

#### Move Lift and Down
**Endpoint:**
```
POST /api/v1/task/move-lift/{device_id}/{target}
```
**Authorization:** JWT Required
**Response:**
```json
{
  "code": 0,
  "message": "SUCCESS",
  "data": {
    "taskId": "2022919382839243943834",
    "createdAt": "2025-03-05T11:45:14Z"
  }
}
```

#### Docking cabin and Move
**Endpoint:**
```
POST /api/v1/task/dock-move/{device_id}/{dockingMarker}/{target}
```
**Authorization:** JWT Required
**Response:**
```json
{
  "code": 0,
  "message": "SUCCESS",
  "data": {
    "taskId": "2022919382839243943834",
    "createdAt": "2025-03-05T15:47:00Z"
  }
}
```

### Charging Management
#### Go to Charge
**Endpoint:**
```
POST /api/v1/goto-charge/{device_id}
```
**Authorization:** JWT Required (NEED TO BE REPAIRED)
**Response:**
```json
{
  "code": 0,
  "message": "SUCCESS"
}
```

## Error Handling
- `401 Unauthorized`: Invalid or missing JWT token.
- `422 Unprocessable Entity`: Missing required parameters.
- `500 Internal Server Error`: Unexpected server-side issues.

## Notes
- Replace `your_domain.com` with your actual API server domain.
- Ensure JWT tokens are refreshed before expiration if using `rememberMe=false`.

