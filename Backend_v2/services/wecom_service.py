"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-04-19
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547

本文件定义了与企业微信相关的服务，包括获取access_token、发送消息等功能。
"""

import json
import aiohttp

from settings import settings


class WeComService:
    """企业微信服务类，处理与企业微信相关的所有业务逻辑"""

    @staticmethod
    async def get_access_token(corp_id, secret):
        """获取企业微信的access_token"""
        # TODO: 这里可以添加缓存机制，避免频繁请求
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={secret}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                result = await response.json()
                if result.get("errcode") == 0:
                    print("获取access_token成功！")
                    print(f"access_token: {result.get('access_token')}")
                    return result.get("access_token")

                raise Exception(f"获取access_token失败: {result}")

    # 发送消息
    @staticmethod
    async def send_message(access_token, user_id, message_content):
        """发送消息"""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        data = {
            "touser": user_id,  # 接收消息的用户ID
            "msgtype": "text",  # 消息类型为文本
            "agentid": settings.WECOM_AGENT_ID,  # 企业微信应用的AgentID
            "text": {
                "content": message_content  # 消息内容
            }
        }
        headers = {
            "Content-Type": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=json.dumps(data)) as response:
                result = await response.json()
                if result.get("errcode") == 0:
                    print("消息发送成功！")
                else:
                    print(f"消息发送失败: {result}")

    @staticmethod
    async def send(user_id, message_content):
        """发送消息"""
        access_token = await WeComService.get_access_token(settings.WECOM_CORP_ID, settings.WECOM_SECRET)
        await WeComService.send_message(access_token, user_id, message_content)
