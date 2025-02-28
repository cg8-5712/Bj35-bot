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


import hashlib
import hmac
import base64
import time
import uuid
import aiohttp
import asyncio

# Function to generate signature asynchronously
async def generate_signature_async(params, access_key_secret):
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
async def get_access_token_async(access_key_id, access_key_secret):
    # Current timestamp
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.gmtime())

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
    signature = await generate_signature_async(params, access_key_secret)

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
            response_data = await response.json()
            print(response_data)
            raise Exception(f"Error: {response_data['message']}")


access_key_id = "6DkfdbFN1lrz1I1c"
access_key_secret = "keH70VXm8Es1o3krnSsblpJu646FfciD"

def get_access_token(access_key_id, access_key_secret):
    return asyncio.run(get_access_token_async(access_key_id, access_key_secret))

try:
    access_token = get_access_token(access_key_id, access_key_secret)
    print(f"Obtained accessToken: {access_token}")
except Exception as e:
    print(f"Failed to obtain accessToken: {e}")
