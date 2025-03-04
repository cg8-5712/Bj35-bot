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

"""
This file is used to store the configuration of the project.
User can get some necessary params from this file.
"""
import os, time
from dotenv import load_dotenv

# 加载.env文件，指定文件位置
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', '.env'))

class Config:
    @property
    def accessToken(self):
        """
        access Token
        with no params
        :return: access token -> str
        """
        # print(os.getenv("accessToken"))
        return os.getenv("accessToken")  # 返回accessToken


    @property
    def expiration(self):
        """
        expiration time
        with no params
        :return: the expiration time timestamp -> int
        """
        expiration_str = os.getenv("expiration")  # 获取过期时间字符串
        print(expiration_str)
        # 将时间字符串转换为时间戳
        return int(time.mktime(time.strptime(expiration_str, '%Y-%m-%dT%H:%M:%S+08:00')))

    @property
    def accessKeyId(self):
        """
        access key id
        :return: int
        """
        return str(os.getenv("accessKeyId"))  # 返回accessKeyId

    @property
    def deviceId(self):
        """
        device id
        :return: list
        """
        divice_id = os.getenv("device_bot1_cabin")
        return divice_id

    @property
    def inside_token(self):
        """
        device name
        :return: str
        """
        return os.getenv("inside_token")

    @property
    def store_Id(self):
        """
        store id
        :return: str
        """
        return os.getenv("store_Id")

    @property
    def SECRET_KEY(self):
        """
        secret key
        :return: str
        """
        return os.getenv("SECRET_KEY")
