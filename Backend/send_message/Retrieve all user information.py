import requests
import time

CORP_ID = "ww8e4628d565c6588f"
CORP_SECRET = "f03d8WfJfKpgX3NG84pXMZOaZ0E_xW9NuaP68ImWtUE"

def get_access_token(corpid, corpsecret):
    """获取企业微信的access_token"""
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
    response = requests.get(url)
    data = response.json()
    if data.get('errcode') == 0:
        return data['access_token']
    else:
        raise Exception(f"获取access_token失败: {data}")

def get_simplelist(access_token, department_id):
    """获取企业微信的成员信息"""
    url = f"https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token={access_token}&department_id={department_id}"
    response = requests.get(url)
    data = response.json()
    if data.get('errcode') == 0:
        return data['userlist']
    else:
        raise Exception(f"获取成员信息失败: {data}")

if __name__ == '__main__':
    access_token = get_access_token(CORP_ID, CORP_SECRET)
    userlist=get_simplelist(access_token, department_id=1)
    for user in userlist:
        print(user)