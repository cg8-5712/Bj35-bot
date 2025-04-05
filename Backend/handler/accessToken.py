#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: https://github.com/cg8-5712
Date: 2025-02-19
Copyright (c) 2025 Dong Zhicheng G2-13
All rights reserved.

This file is part of the Bj35-Robot-Project.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import re
import os
import hashlib
import hmac
import base64
import time
import uuid
import aiohttp
from dotenv import load_dotenv

from config import Config

# Function to generate signature asynchronously
async def generate_signature(params, access_key_secret):
    # Sort request parameters in dictionary order
    sorted_params = sorted(params.items())

    print(f"Sorted request parameters: {sorted_params}")

    # Construct canonical request string
    canonical_string = "&".join([f"{key}={value}" for key, value in sorted_params])
    print(f"Canonical request string: {canonical_string}")

    # Construct HMAC signature
    message = canonical_string.encode('utf-8')
    key = (access_key_secret + "&").encode('utf-8')
    signature = hmac.new(key, message, hashlib.sha1).digest()
    print(f"message: {message}")
    print(f"HMAC signature: {base64.b64encode(signature).decode('utf-8')}")

    # Base64 encode the signature
    return base64.b64encode(signature).decode('utf-8')


# Method to get accessToken
async def get_access_token(access_key_id, access_key_secret):
    # Current timestamp
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.localtime())

    print(f"Current timestamp: {timestamp}")

    # Unique signatureNonce
    signature_nonce = str(uuid.uuid4())

    print(signature_nonce)

    # Request parameters
    params = {
        # "signature": "",
        "signatureNonce": signature_nonce,
        "accessKeyId": access_key_id,
        "timestamp": timestamp,
    }

    # Generate signature
    signature = await generate_signature(params, access_key_secret)

    # Add signature to request parameters
    params["signature"] = signature

    params = {
        "signature": signature,
        "signatureNonce": signature_nonce,
        "accessKeyId": access_key_id,
        "timestamp": timestamp,
    }

    print(f"Request parameters: {params}")

    # Send request to get accessToken
    url = "https://open-api.yunjiai.cn/v3/auth/accessToken"

    # Parse response
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=params) as response:
            response_json = await response.json()
            if response_json["code"] == 0:
                return response_json
            else:
                raise Exception(f"Failed to obtain accessToken: {response_json['msg']}")




async def update_access_token():
    access_key_id = Config.accessKeyId()
    access_key_secret = Config.SECRET_KEY()
    data = await get_access_token(access_key_id, access_key_secret)
    if data["code"] == 0:
        access_token = data["data"]["accessToken"]
        expiration = data["data"]["expiration"]
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')

        # 读取原始文件内容
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"读取.env文件失败: {e}")
            return

        # 使用正则表达式更新accessToken和EXPIRE_TIME的值
        new_content = re.sub(
            r"(?i)^(accessToken\s*=\s*).*$",
            f"accessToken = {access_token}",
            content,
            flags=re.MULTILINE
        )
        new_content = re.sub(
            r"(?i)^(EXPIRE_TIME\s*=\s*).*$",
            f"EXPIRE_TIME = {expiration}",
            new_content,
            flags=re.MULTILINE
        )

        # 写回更新后的内容到.env文件
        try:
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
            return True
        except Exception as e:
            return e
