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

import time
from typing import Dict, List, Any, ClassVar
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Pydantic 类型检查和验证"""

    ENV: str = Field(default="production")

    URI_PREFIX: ClassVar[str] = '/api/v1'

    # 数据库配置
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_NAME: str = Field(default="userdata")
    DB_USER: str = Field(default="postgres")
    DB_PASSWORD: str = Field(default="password")
    DB_POOL_MIN_SIZE: int = Field(default=5)
    DB_POOL_MAX_SIZE: int = Field(default=10)
    DB_SSL: bool = Field(default=False)

    # 接口认证相关
    AUTH_ACCESS_TOKEN: str = Field(default="access_token")
    AUTH_ACCESS_KEY_ID: str = Field(default="access_key_id")
    AUTH_STORE_ID: str = Field(default="store_id")
    AUTH_SECRET_KEY: str = Field(default="secret_key")
    AUTH_JWT_SECRET_KEY: str = Field(default="jwt_secret_key")
    AUTH_EXPIRE_TIME: str = Field(default="1900-01-01T00:00:00+08:00")

    # 企业微信相关配置
    WECOM_CORP_ID: str = Field(default="corp_id")
    WECOM_SECRET: str = Field(default="secret")
    WECOM_AGENT_ID: str = Field(default="agent_id")
    WECOM_REDIRECT_URI: str = Field(default="http://localhost:8000/api/v1/auth/wechat")
    WECOM_FRONTEND_URL: str = Field(default="http://localhost:5173")

    # 机器人相关配置
    CABINS: Dict[str, str] = Field(default=dict())
    CHASSIS: Dict[str, str] = Field(default=dict())

    class Config:           # pylint: disable=too-few-public-methods
        """Pydantic 配置"""
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

class Config:
    """Config 兼容之前方法"""

    _targets_list: ClassVar[List[Dict[str, str]]] = [
        {"value": "B101", "label": "B101"},
        {"value": "B102", "label": "B102"},
        {"value": "B103", "label": "B103"},
        {"value": "B104", "label": "B104"},
        {"value": "B105", "label": "B105"},
        {"value": "B201", "label": "B201"},
        {"value": "B202", "label": "B202"},
        {"value": "B203", "label": "B203"},
        {"value": "B204", "label": "B204"},
        {"value": "B205", "label": "B205"},
        {"value": "B206", "label": "B206"},
        {"value": "B207", "label": "B207"},
        {"value": "B208", "label": "B208"},
        {"value": "B209", "label": "B209"},
        {"value": "B210", "label": "B210"},
        {"value": "B211", "label": "B211"},
        {"value": "B212", "label": "B212"},
        {"value": "B213", "label": "B213"},
        {"value": "B214", "label": "B214"},
        {"value": "B215", "label": "B215"},
        {"value": "B216", "label": "B216"},
        {"value": "B217", "label": "B217"},
        {"value": "B218", "label": "B218"},
        {"value": "B219", "label": "B219"},
        {"value": "B220", "label": "B220"},
        {"value": "B301", "label": "B301"},
        {"value": "B302", "label": "B302"},
        {"value": "B303", "label": "B303"},
        {"value": "B304", "label": "B304"},
        {"value": "B305", "label": "B305"},
        {"value": "B308", "label": "B308"},
        {"value": "B309", "label": "B309"},
        {"value": "B310", "label": "B310"},
        {"value": "B311", "label": "B311"},
        {"value": "B312", "label": "B312"},
        {"value": "B313", "label": "B313"},
        {"value": "B314", "label": "B314"},
        {"value": "B315", "label": "B315"},
        {"value": "B401", "label": "B401"},
        {"value": "B402", "label": "B402"},
        {"value": "B403", "label": "B403"},
        {"value": "C101", "label": "C101"},
        {"value": "C102", "label": "C102"},
        {"value": "C103", "label": "C103"},
        {"value": "C104", "label": "C104"},
        {"value": "C201", "label": "C201"},
        {"value": "C202", "label": "C202"},
        {"value": "C203", "label": "C203"},
        {"value": "C204", "label": "C204"},
        {"value": "C205", "label": "C205"},
        {"value": "C206", "label": "C206"},
        {"value": "C301", "label": "C301"},
        {"value": "C302", "label": "C302"},
        {"value": "C303", "label": "C303"},
        {"value": "C304", "label": "C304"},
        {"value": "C305", "label": "C305"},
        {"value": "C306", "label": "C306"},
        {"value": "Y101", "label": "Y101"},
        {"value": "Y102", "label": "Y102"},
        {"value": "Y103", "label": "Y103"},
        {"value": "Y201", "label": "Y201"},
        {"value": "Y202", "label": "Y202"},
        {"value": "Y203", "label": "Y203"},
        {"value": "Y204", "label": "Y204"},
        {"value": "Y301", "label": "Y301"},
        {"value": "Y302", "label": "Y302"},
        {"value": "Y303", "label": "Y303"},
        {"value": "Y401", "label": "Y401"},
        {"value": "Y402", "label": "Y402"},
        {"value": "Q101", "label": "Q101"},
        {"value": "Q103", "label": "Q103"},
        {"value": "Q201", "label": "Q201"},
        {"value": "Q202", "label": "Q202"},
        {"value": "Q203", "label": "Q203"},
        {"value": "Q205", "label": "Q205"},
        {"value": "Q301", "label": "Q301"},
        {"value": "Q302", "label": "Q302"},
        {"value": "Q304", "label": "Q304"},
        {"value": "Q401", "label": "Q401"},
        {"value": "S101", "label": "S101"},
        {"value": "S201", "label": "S201"},
        {"value": "S202", "label": "S202"},
        {"value": "S203", "label": "S203"},
        {"value": "S204", "label": "S204"},
        {"value": "S205", "label": "S205"},
        {"value": "S206", "label": "S206"},
        {"value": "S207", "label": "S207"},
        {"value": "S301", "label": "S301"},
        {"value": "S302", "label": "S302"},
        {"value": "S303", "label": "S303"},
        {"value": "S304", "label": "S304"},
        {"value": "S305", "label": "S305"},
        {"value": "S306", "label": "S306"},
        {"value": "S307", "label": "S307"},
        {"value": "S308", "label": "S308"},
        {"value": "S309", "label": "S309"},
        {"value": "S401", "label": "S401"},
        {"value": "S402", "label": "S402"},
        {"value": "S403", "label": "S403"},
        {"value": "S404", "label": "S404"},
        {"value": "S405", "label": "S405"},
        {"value": "S406", "label": "S406"},
        {"value": "S407", "label": "S407"},
        {"value": "S408", "label": "S408"},
        {"value": "S409", "label": "S409"},
        {"value": "一楼作业柜", "label": "一楼作业柜"},
        {"value": "二楼作业柜", "label": "二楼作业柜"},
        {"value": "三楼作业柜", "label": "三楼作业柜"}
    ]

    @classmethod
    def get_env(cls) -> str:
        """环境变量"""
        return settings.ENV

    @classmethod
    def uri_prefix(cls) -> str:
        """URI前缀"""
        return settings.URI_PREFIX

    @classmethod
    def database_config(cls) -> Dict[str, Any]:
        """返回数据库配置字典"""
        return {
            'host': settings.DB_HOST,
            'port': settings.DB_PORT,
            'database': settings.DB_NAME,
            'user': settings.DB_USER,
            'password': settings.DB_PASSWORD,
            'min_size': settings.DB_POOL_MIN_SIZE,
            'max_size': settings.DB_POOL_MAX_SIZE,
            'ssl': settings.DB_SSL
        }

    @classmethod
    def accessToken(cls) -> str:
        """access Token"""
        return settings.AUTH_ACCESS_TOKEN

    @classmethod
    def accessKeyId(cls) -> str:
        """access key id"""
        return settings.AUTH_ACCESS_KEY_ID

    @classmethod
    def store_Id(cls) -> str:
        """store id"""
        return settings.AUTH_STORE_ID

    @classmethod
    def SECRET_KEY(cls) -> str:
        """secret key"""
        return settings.AUTH_SECRET_KEY

    @classmethod
    def jwt_secret_key(cls) -> str:
        """jwt secret key"""
        return settings.AUTH_JWT_SECRET_KEY

    @classmethod
    def expire_time(cls) -> int:
        """expire time as timestamp"""
        if not settings.AUTH_EXPIRE_TIME:
            return 0
        return int(time.mktime(time.strptime(settings.AUTH_EXPIRE_TIME, '%Y-%m-%dT%H:%M:%S+08:00')))

    @classmethod
    def corp_id(cls) -> str:
        """corp id"""
        return settings.WECOM_CORP_ID

    @classmethod
    def secret(cls) -> str:
        """secret key"""
        return settings.WECOM_SECRET

    @classmethod
    def agent_id(cls) -> str:
        """agent id"""
        return settings.WECOM_AGENT_ID

    @classmethod
    def app_id(cls) -> str:
        """app id (same as agent id)"""
        return settings.WECOM_AGENT_ID

    @classmethod
    def redirect_uri(cls) -> str:
        """企业微信 OAuth 重定向 URI"""
        return settings.WECOM_REDIRECT_URI

    @classmethod
    def frontend_url(cls) -> str:
        """前端 URL"""
        return settings.WECOM_FRONTEND_URL

    @classmethod
    def target_list(cls) -> List[Dict[str, str]]:
        """
        返回教室位置
        B101~B105、201~220、301~305、308~315、401~403
        C101~C104、201~206、301~206
        Y101~Y103、201~204、301~303、401~402
        Q101、103、201~203、205、301、302、304、401
        S101、201~207、301~309、401~409
        一楼作业柜、二楼作业柜、三楼作业柜
        up to date on 2025-03-05 08:24:40.871318+00:00
        """
        return cls._targets_list

    @classmethod
    def cabins(cls) -> Dict[str, str]:
        return settings.CABINS

    @classmethod
    def chassis(cls) -> Dict[str, str]:
        return settings.CHASSIS
