# API Usage Documentation

## 1. Overview
This API is built using Flask and provides endpoints to access device information and statuses. All requests require authentication via a valid Token. Without a valid token, access to the API will be denied.

## 2. Authentication
To authenticate your requests, include the Token in the HTTP request header as shown below:

```http
Token: <Your Authentication Token>
```
If the Token is missing, invalid, or expired, the API will return an HTTP 403 (Forbidden) error, indicating that the request is unauthorized.

## 3. API Endpoints

### 1. Get Access Token
**URL:** `/api/v1/accessToken`  
**Request Method:** `GET`  
**Request Header:**
```http
Token: <Your Authentication Token>
```
**Description:** This endpoint returns a new accessToken that can be used for further requests within the session.

**Response Format:**
```json
{
  "accessToken": "<access_token>"
}
```
This `accessToken` should be included in the headers of subsequent API requests to access protected endpoints.

### 2. Get Device Information
**URL:** `/api/v1/deviceInfo`  
**Request Method:** `GET`  
**Request Header:**
```http
Token: <Your Authentication Token>
```
**Description:** This endpoint retrieves a list of devices registered in the system, including their device ID, name, and current status (e.g., online or offline).

**Response Format:**
```json
[
  {
    "device_id": 1,
    "name": "Device 1",
    "status": "online"
  },
  {
    "device_id": 2,
    "name": "Device 2",
    "status": "offline"
  }
]
```
The response provides an array of devices, where each device includes its `device_id`, `name`, and `status`.

### 3. Get Device Status
**URL:** `/api/v1/device_status/<device_id>`  
**Request Method:** `GET`  
**Request Header:**
```http
Token: <Your Authentication Token>
```
**Description:** This endpoint retrieves the status of a specific device identified by its `device_id`. It provides the current status and the last time the device was active.

**URL Parameters:**
- `device_id`: The ID of the device you want to query.

**Response Format:**
```json
{
  "device_id": 1,
  "status": "online",
  "last_active": "2025-03-04 12:00:00"
}
```
The response includes the device's `device_id`, its `status` (e.g., online or offline), and the `last_active` timestamp, indicating the most recent activity.

### 4. Get Device Task Information
**URL:** `/api/v1/device_task/<device_id>`  
**Request Method:** `GET`  
**Request Header:**
```http
Token: <Your Authentication Token>
```
**Description:** This endpoint retrieves the task details for a specific device, including the task ID, status, and the time the task was started.

**URL Parameters:**
- `device_id`: The ID of the device whose task information you want to retrieve.

**Response Format:**
```json
{
  "device_id": 1,
  "tasks": [
    {
      "task_id": 101,
      "status": "running",
      "start_time": "2025-01-01"
    }
  ]
}
```
The response includes a `tasks` array containing the details of each task assigned to the device. Each task contains:
- `task_id`: Unique identifier for the task.
- `status`: Current status of the task (e.g., running, completed).
- `start_time`: Timestamp when the task started.

## 4. Error Codes
The API may return the following HTTP status codes:

- **403 Forbidden:** The request was made with a missing or invalid Token. The Token must be provided in the request header and must be valid.
- **404 Not Found:** The requested resource (e.g., a device or task) could not be found on the server.
- **500 Internal Server Error:** An error occurred on the server while processing the request.

