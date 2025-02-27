#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
作者: https://github.com/cg8-5712
日期: 2025-02-19
版权 (c) 2025 董志成 G2-13
保留所有权利。

本文件是Bj35-Robot-Project项目的一部分。

本软件遵循GNU Affero通用公共许可证第3版(AGPL-3.0)。
除非遵守该许可证，否则不得使用本文件。
您可以在以下位置获取许可证副本：

    https://www.gnu.org/licenses/agpl-3.0.html

本软件按"原样"提供，不提供任何形式的担保或条件，
无论是明示的还是暗示的。请参阅许可证了解具体的权限和限制。

如果您修改并使用本软件通过网络提供服务，则必须向该服务的用户
提供您修改版本的源代码。
"""

import hashlib
import hmac
import base64
import time
import uuid
import aiohttp
import asyncio
from urllib.parse import urlencode


# 生成签名的函数
async def generate_signature_async(params, access_key_secret):
    # 按字典顺序排序请求参数
    sorted_params = sorted(params.items())

    # 构造规范化请求字符串
    canonical_string = urlencode(sorted_params)

    # 构造HMAC签名
    message = canonical_string.encode('utf-8')
    key = (access_key_secret + "&").encode('utf-8')
    signature = hmac.new(key, message, hashlib.sha1).digest()

    # 对签名进行Base64编码
    return base64.b64encode(signature).decode('utf-8')


# 获取accessToken的方法
async def get_access_token_async(access_key_id, access_key_secret):
    # 当前时间戳
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.gmtime())

    # 唯一的signatureNonce
    signature_nonce = str(uuid.uuid4())

    print(signature_nonce)

    # 请求参数
    params = {
        "accessKeyId": access_key_id,
        "timestamp": timestamp,
        "signatureNonce": signature_nonce,
    }

    # 生成签名
    signature = await generate_signature_async(params, access_key_secret)

    # 将签名添加到请求参数中
    params["signature"] = signature

    # 发送请求获取accessToken
    url = "https://open-api.yunjiai.cn/v3/auth/accessToken"

    # 解析响应
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=params) as response:
            response_data = await response.json()
            if response_data["code"] == 0:
                return response_data["data"]["accessToken"]
            raise Exception(f"错误: {response_data['message']}")


# 示例用法
access_key_id = "6DkfdbFN1lrz1I1c"
access_key_secret = "keH70VXm8Es1o3krnSsblpJu646FfciD"

def get_access_token(access_key_id, access_key_secret):
    return asyncio.run(get_access_token_async(access_key_id, access_key_secret))

try:
    access_token = get_access_token(access_key_id, access_key_secret)
    print(f"获取的accessToken: {access_token}")
except Exception as e:
    print(f"获取accessToken失败: {e}")

