#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: https://github.com/cg8-5712
Date: 2025-02-19
Copyright (c) 2025 Dong Zhicheng G2-13
All rights reserved.

This file is part of Bj35-Robot-Project.

This software is licensed under the GNU Affero General Public License, version 3 (AGPL-3.0).
You may not use this file except in compliance with the License.
You may obtain a copy of the License at:

    https://www.gnu.org/licenses/agpl-3.0.html

The software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions and
limitations under the License.

If you modify and use this software to provide a service over a network, you must make the source
code of your modified version available to the users of that service.

"""

import hashlib
import hmac
import base64
import time
import uuid
import aiohttp
import asyncio
from urllib.parse import urlencode


# Function to generate the signature
async def generate_signature_async(params, access_key_secret):
    # Sort the request parameters in dictionary order
    sorted_params = sorted(params.items())

    # Construct normalized request string
    canonical_string = urlencode(sorted_params)

    # Construct HMAC signature
    message = canonical_string.encode('utf-8')
    key = (access_key_secret + "&").encode('utf-8')
    signature = hmac.new(key, message, hashlib.sha1).digest()

    # Base64 encode the signature
    return base64.b64encode(signature).decode('utf-8')


# Method to get the accessToken
async def get_access_token_async(access_key_id, access_key_secret):
    # Current timestamp
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.gmtime())

    # Unique signatureNonce
    signature_nonce = str(uuid.uuid4())

    print(signature_nonce)

    # Request parameters
    params = {
        "accessKeyId": access_key_id,
        "timestamp": timestamp,
        "signatureNonce": signature_nonce,
    }

    # Generate the signature
    signature = await generate_signature_async(params, access_key_secret)

    # Add the signature to the request parameters
    params["signature"] = signature

    # Send request to get accessToken
    url = "https://open-api.yunjiai.cn/v3/auth/accessToken"

    # Parse the response
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=params) as response:
            response_data = await response.json()
            if response_data["code"] == 0:
                return response_data["data"]["accessToken"]
            raise Exception(f"Error: {response_data['message']}")


# Example usage
access_key_id = "6DkfdbFN1lrz1I1c"
access_key_secret = "keH70VXm8Es1o3krnSsblpJu646FfciD"

def get_access_token(access_key_id, access_key_secret):
    return asyncio.run(get_access_token_async(access_key_id, access_key_secret))

try:
    access_token = get_access_token(access_key_id, access_key_secret)
    print(f"Retrieved accessToken: {access_token}")
except Exception as e:
    print(f"Failed to retrieve accessToken: {e}")

