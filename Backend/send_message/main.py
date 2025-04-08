import aiohttp
import asyncio
import json

corp_id = "ww8e4628d565c6588f"  # 企业ID
secret = "f03d8WfJfKpgX3NG84pXMaN7a6G1xOY2QummZNZh_Xg"  # 应用Secret
agent_id = "1000166"  # 应用AgentId
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

    """
        send_message/main.py send()(无assessToken)->send_message()(有assessToken)
        
    """

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


async def get_userid_by_mobile(mobile):
    # 通过手机号获取企业微信用户ID
    async with aiohttp.ClientSession() as session:
        # 获取access_token
        token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={secret}"
        async with session.get(token_url) as token_resp:
            token_data = await token_resp.json()
            if token_data.get('errcode') != 0:
                return None
            access_token = token_data['access_token']
            # 查询UserID
            userid_url = f"https://qyapi.weixin.qq.com/cgi-bin/user/getuserid?access_token={access_token}"
            async with session.post(userid_url, json={"mobile": mobile}) as user_resp:
                user_data = await user_resp.json()
                return user_data.get('userid')

async def get_userid_by_email(email):
    # 通过邮箱获取企业微信用户ID
    async with aiohttp.ClientSession() as session:
        token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={secret}"
        async with session.get(token_url) as token_response:
            token_res = await token_response.json()

            if token_res.get("errcode") != 0:
                raise Exception(f"获取access_token失败: {token_res.get('errmsg')}")

            access_token = token_res["access_token"]
            params = {
                "access_token": access_token
            }
            payload = {
                "email": email,
                "email_type":2 # 邮箱类型，1：企业邮箱，2：个人邮箱
            }
            async with session.post("https://qyapi.weixin.qq.com/cgi-bin/user/get_userid_by_email", params=params, json=payload) as user_response:
                user_res = await user_response.json()
                if user_res.get("errcode") == 0:
                    return user_res.get("userid")
                else:
                    raise Exception(f"查询失败: {user_res.get('errmsg')}")

# 主函数
async def send(user_id, message_content):
    access_token = await get_access_token(corp_id, secret)
    await send_message(access_token, user_id, message_content)

# # 运行主函数
if __name__ == "__main__":
    mobile=input("mobile:")
    user_id=asyncio.run(get_userid_by_mobile(mobile))
    #email=input("email:")
    #user_id=asyncio.run(get_userid_by_email(email))
    print(f"user_id:{user_id}")
    asyncio.run(send(user_id, "你的作业送到了，请注意查收"))
