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

This file is used to store the configuration of the project.
User can get some necessary params from this file.
"""

import os
import time
from dotenv import load_dotenv

# 加载.env文件，指定文件位置
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', '.env'))

class Config:
    @classmethod
    def accessToken(cls):
        """
        access Token
        with no params
        :return: access token -> str
        """
        # print(os.getenv("accessToken"))
        return os.getenv("accessToken")  # 返回accessToken


    @classmethod
    def expiration(cls):
        """
        expiration time
        with no params
        :return: the expiration time timestamp -> int
        """
        expiration_str = os.getenv("expiration")  # 获取过期时间字符串
        print(expiration_str)
        # 将时间字符串转换为时间戳
        return int(time.mktime(time.strptime(expiration_str, '%Y-%m-%dT%H:%M:%S+08:00')))

    @classmethod
    def accessKeyId(cls):
        """
        access key id
        :return: int
        """
        return str(os.getenv("accessKeyId"))  # 返回accessKeyId

    @classmethod
    def deviceId(cls):
        """
        device id
        :return: list
        """
        divice_id = os.getenv("device_bot1_cabin")
        return divice_id

    @classmethod
    def inside_token(cls):
        """
        device name
        :return: str
        """
        return os.getenv("inside_token")

    @classmethod
    def store_Id(cls):
        """
        store id
        :return: str
        """
        return os.getenv("store_Id")

    @classmethod
    def SECRET_KEY(cls):
        """
        secret key
        :return: str
        """
        return os.getenv("SECRET_KEY")
    
    @classmethod
    def jwt_secret_key(cls):
        """
        jwt secret key
        :return: str
        """
        return os.getenv("JWT_SECRET_KEY")

    @classmethod
    def target_get(cls, target):
        """
        返回教室位置
        B101~B105、201~220、301~305、308~315、401~403
        C101~C104、201~206、301~206
        Y101~Y103、201~204、301~303、401~402
        Q101、103、、201~203、205、301、302、304、401
        S101、201~207、301~309、401~409
        一楼作业柜、二楼作业柜、三楼作业柜
        up to date on 2025-03-05 08:24:40.871318+00:00
        """
        classes_list = {
            "B101": "B101",
            "B102": "B102",
            "B103": "B103",
            "B104": "B104",
            "B105": "B105",
            "B201": "B201",
            "B202": "B202",
            "B203": "B203",
            "B204": "B204",
            "B205": "B205",
            "B206": "B206",
            "B207": "B207",
            "B208": "B208",
            "B209": "B209",
            "B210": "B210",
            "B211": "B211",
            "B212": "B212",
            "B213": "B213",
            "B214": "B214",
            "B215": "B215",
            "B216": "B216",
            "B217": "B217",
            "B218": "B218",
            "B219": "B219",
            "B220": "B220",
            "B301": "B301",
            "B302": "B302",
            "B303": "B303",
            "B304": "B304",
            "B305": "B305",
            "B308": "B308",
            "B309": "B309",
            "B310": "B310",
            "B311": "B311",
            "B312": "B312",
            "B313": "B313",
            "B314": "B314",
            "B315": "B315",
            "B401": "B401",
            "B402": "B402",
            "B403": "B403",
            "C101": "C101",
            "C102": "C102",
            "C103": "C103",
            "C104": "C104",
            "C201": "C201",
            "C202": "C202",
            "C203": "C203",
            "C204": "C204",
            "C205": "C205",
            "C206": "C206",
            "C301": "C301",
            "C302": "C302",
            "C303": "C303",
            "C304": "C304",
            "C305": "C305",
            "C306": "C306",
            "Y101": "Y101",
            "Y102": "Y102",
            "Y103": "Y103",
            "Y201": "Y201",
            "Y202": "Y202",
            "Y203": "Y203",
            "Y204": "Y204",
            "Y301": "Y301",
            "Y302": "Y302",
            "Y303": "Y303",
            "Y401": "Y401",
            "Y402": "Y402",
            "Q101": "Q101",
            "Q103": "Q103",
            "Q201": "Q201",
            "Q202": "Q202",
            "Q203": "Q203",
            "Q205": "Q205",
            "Q301": "Q301",
            "Q302": "Q302",
            "Q304": "Q304",
            "Q401": "Q401",
            "S101": "S101",
            "S201": "S201",
            "S202": "S202",
            "S203": "S203",
            "S204": "S204",
            "S205": "S205",
            "S206": "S206",
            "S207": "S207",
            "S301": "S301",
            "S302": "S302",
            "S303": "S303",
            "S304": "S304",
            "S305": "S305",
            "S306": "S306",
            "S307": "S307",
            "S308": "S308",
            "S309": "S309",
            "S401": "S401",
            "S402": "S402",
            "S403": "S403",
            "S404": "S404",
            "S405": "S405",
            "S406": "S406",
            "S407": "S407",
            "S408": "S408",
            "S409": "S409",
            "一楼作业柜": "一楼作业柜",
            "二楼作业柜": "二楼作业柜",
            "三楼作业柜": "三楼作业柜",
        }
        return classes_list.get(target, "未知教室")
