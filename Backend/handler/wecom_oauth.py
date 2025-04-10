import requests
import logging
from urllib.parse import quote

from utils.config import Config

class WeComOAuth:
    """企业微信 OAuth 认证处理类"""

    @classmethod
    def get_oauth_url(cls):
        """获取企业微信 OAuth 授权 URL"""
        corp_id = Config.corp_id()
        redirect_uri = quote(Config.redirect_uri(), safe='')
        agent_id = Config.agent_id()

        # 构建授权URL
        # 参考文档: https://developer.work.weixin.qq.com/document/path/96440
        oauth_url = (
            f"https://open.work.weixin.qq.com/wwopen/sso/qrConnect"
            f"?appid={corp_id}"
            f"&agentid={agent_id}"
            f"&redirect_uri={redirect_uri}"
            f"&state=STATE"  # 可以使用随机字符串防止CSRF攻击
        )

        return oauth_url

    @classmethod
    async def get_user_info(cls, code):
        """通过授权码获取用户信息"""
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

            # 3. 获取用户详细信息
            user_detail = await cls.get_user_detail(access_token, user_info.get('userid'))
            return user_detail

        except Exception as e:
            logging.error(f"Error getting user info: {e}")
            return None

    @classmethod
    async def get_access_token(cls):
        """获取企业微信访问令牌"""
        corp_id = Config.corp_id()
        corp_secret = Config.corp_secret()

        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={corp_secret}"

        try:
            response = requests.get(url)
            data = response.json()

            if data.get('errcode') == 0:
                return data.get('access_token')
            else:
                logging.error(f"Failed to get access token: {data}")
                return None
        except Exception as e:
            logging.error(f"Error getting access token: {e}")
            return None

    @classmethod
    async def get_user_id(cls, access_token, code):
        """通过授权码获取用户ID"""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token={access_token}&code={code}"

        try:
            response = requests.get(url)
            data = response.json()

            if data.get('errcode') == 0:
                return {
                    'userid': data.get('userid'),
                    'openid': data.get('openid'),
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
        """获取用户详细信息"""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={access_token}&userid={userid}"

        try:
            response = requests.get(url)
            data = response.json()

            if data.get('errcode') == 0:
                return {
                    'userid': data.get('userid'),
                    'name': data.get('name'),
                    'department': data.get('department'),
                    'position': data.get('position'),
                    'mobile': data.get('mobile'),
                    'email': data.get('email'),
                    'avatar': data.get('avatar'),
                    'wecom': data.get('alias', '')
                }
            else:
                logging.error(f"Failed to get user detail: {data}")
                return None
        except Exception as e:
            logging.error(f"Error getting user detail: {e}")
            return None
