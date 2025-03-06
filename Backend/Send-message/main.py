import aiohttp
import asyncio
import json

# 企业微信API配置
corp_id = "wwf7b517dadde6fcc6"  # 企业ID
secret = "hPUCEvAKMm3o8X6pWNLtF89dKQyDkJhuktiGefpKyjo"  # 应用Secret
agent_id = "1000002"  # 应用AgentId
user_id = ""  # 接收消息的用户ID

# 获取access_token
async def get_access_token(corp_id, secret):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={secret}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()
            if result.get("errcode") == 0:
                print("获取access_token成功！")
                print(f"access_token: {result.get('access_token')}")
                return result.get("access_token")
            else:
                raise Exception(f"获取access_token失败: {result}")

# 发送消息
async def send_message(access_token, user_id, message_content):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    data = {
        "touser": user_id,  # 接收消息的用户ID
        "msgtype": "text",  # 消息类型为文本
        "agentid": agent_id,  # 应用ID
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

# 主函数
async def main():
    access_token = await get_access_token(corp_id, secret)
    user_id=input("请输入接收消息的用户ID：")
    await send_message(access_token, user_id, "您的作业送到了,请注意查收！")

# 运行主函数
if __name__ == "__main__":
    asyncio.run(main())
