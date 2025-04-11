import logging
import random
from urllib.parse import quote

import aiohttp
from utils.config import Config

class WeComOAuth:
    """企业微信 OAuth 认证处理类"""

    state = []

    @classmethod
    def get_oauth_url(cls):
        """获取企业微信 OAuth 授权 URL"""
        corp_id = Config.corp_id()
        redirect_uri = quote(Config.redirect_uri(), safe='')
        agent_id = Config.agent_id()

        # 生成随机字符串作为 state 参数
        state = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))
        cls.state.append(state)

        # 构建授权URL
        # 参考文档: https://developer.work.weixin.qq.com/document/path/98174
        oauth_url = (
            f"https://open.weixin.qq.com/connect/oauth2/authorize"
            f"?appid={corp_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
            f"&scope=snsapi_userinfo"
            f"&state={state}"
            f"#wechat_redirect"
        )

        return oauth_url

    @classmethod
    async def get_user_info(cls, code: str, state: str):
        """通过授权码获取用户信息"""
        if state not in cls.state:
            logging.error("State mismatch")
            return None
        cls.state.remove(state)

        try:
            # 1. 获取访问令牌
            access_token = await cls.get_access_token()
            if not access_token:
                logging.error("Failed to get access token")
                return None

            # 2. 使用授权码获取用户身份
            user_info = await cls.get_user_id(access_token, code)
            if not user_info:
                logging.error("Failed to get user ID")
                return None

            # 3. 获取用户基本信息
            user_detail = await cls.get_user_detail(access_token, user_info.get('userid'))
            if not user_detail:
                return None

            # 4. 如果有user_ticket，获取敏感信息
            if user_info.get('user_ticket'):
                sensitive_info = await cls.get_sensitive_info(access_token, user_info.get('user_ticket'))
                if sensitive_info:
                    user_detail.update(sensitive_info)

            return user_detail

        except Exception as e:
            logging.error(f"Error getting user info: {e}")
            return None

    @classmethod
    async def get_access_token(cls):
        """获取企业微信访问令牌"""
        return Config.accessToken()

    @classmethod
    async def get_user_id(cls, access_token, code):
        """通过授权码获取用户ID"""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/auth/getuserinfo?access_token={access_token}&code={code}"

        try:
            response = await aiohttp.ClientSession().get(url)
            data = await response.json()

            if data is not None and data.get('errcode') == 0:
                return {
                    'userid': data.get('userid'),
                    'user_ticket': data.get('user_ticket')
                }
            else:
                logging.error(f"Failed to get user ID: {data}")
                return None
        except Exception as e:
            logging.error(f"Error getting user ID: {e}")
            return None

    @classmethod
    async def get_user_detail(cls, access_token, userid):
        """获取用户基本信息"""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={access_token}&userid={userid}"

        try:
            response = await aiohttp.ClientSession().get(url)
            data = await response.json()

            if data.get('errcode') == 0:
                return {
                    'userid': data.get('userid'),
                    'name': data.get('name'),
                    'department': data.get('department'),
                    'position': data.get('position'),
                    'wecom': data.get('alias', '')
                }
            else:
                logging.error(f"Failed to get user detail: {data}")
                return None
        except Exception as e:
            logging.error(f"Error getting user detail: {e}")
            return None

    @classmethod
    async def get_sensitive_info(cls, access_token, user_ticket):
        """获取用户敏感信息"""
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/getuserdetail?access_token={access_token}"
        data = {"user_ticket": user_ticket}

        try:
            response = await aiohttp.ClientSession().post(url, json=data)
            data = await response.json()

            if data.get('errcode') == 0:
                return {
                    'mobile': data.get('mobile'),
                    'email': data.get('email'),
                    'avatar': data.get('avatar')
                }
            else:
                logging.error(f"Failed to get sensitive info: {data}")
                return None
        except Exception as e:
            logging.error(f"Error getting sensitive info: {e}")
            return None
