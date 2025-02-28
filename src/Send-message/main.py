import requests
import json

# 企业微信API配置
corp_id = "wwf7b517dadde6fcc6"  # 企业ID
secret = "hPUCEvAKMm3o8X6pWNLtF89dKQyDkJhuktiGefpKyjo"  # 应用Secret
agent_id = "1000002"  # 应用AgentId
user_id = "ChengYuHe"  # 接收消息的用户ID

# 获取access_token
def get_access_token(corp_id, secret):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={secret}"
    response = requests.get(url).json()
    if response.get("errcode") == 0:
        print("获取access_token成功！")
        print(f"access_token: {response.get('access_token')}")
        return response.get("access_token")
    else:
        raise Exception(f"获取access_token失败: {response}")



def send_message(access_token, user_id, message_content):
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
    response = requests.post(url,headers=headers , data=json.dumps(data))
    result = response.json()
    if result.get("errcode") == 0:
        print("消息发送成功！")
    else:
        print(f"消息发送失败: {result}")


# 主函数
if __name__ == "__main__":
    # 获取access_token
    access_token = get_access_token(corp_id, secret)

    # 发送消息
    message_content = "您的作业送到了，请注意查收！"  # 替换为你要发送的消息内容
    send_message(access_token, user_id, message_content)