import requests
import time
import json

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

def get_child_department(access_token, department_id=1):
    """获取子部门列表"""
    url = f"https://qyapi.weixin.qq.com/cgi-bin/department/simplelist?access_token={access_token}&id={department_id}"
    response = requests.get(url)
    data = response.json()
    if data.get('errcode') == 0:
        return data['department_id']
    else:
        raise Exception(f"获取子部门列表失败: {data}")

def get_department_uesr_list(access_token, department_id):
    """获取企业微信的成员信息"""
    url=f"https://qyapi.weixin.qq.com/cgi-bin/user/list?access_token={access_token}&department_id={department_id}"
    response = requests.get(url)
    data = response.json()
    if data.get('errcode') == 0:
        return data['userlist']
    else:
        raise Exception(f"获取成员信息失败: {data}")

def get_user_all_info(access_token, user_id):
    """获取企业微信的成员信息"""
    url=f"https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={access_token}&userid={user_id}"
    response = requests.get(url)
    data = response.json()
    if data.get('errcode') == 0:
        return data
    else:
        raise Exception(f"获取成员信息失败: {data}")


def write():
    get_access_token(CORP_ID, CORP_SECRET)
    child_department_id_list = get_child_department(access_token, department_id=1)
    if child_department_id_list:
        for department_id in child_department_id_list:
            id=department_id['id']
            user_list = get_department_uesr_list(access_token, id)
            if user_list:
                for user in user_list:
                    # print(f"name:{user['name']} userid:{user['userid']}")
                    user_info = get_user_all_info(access_token, user)
                    all_users_info.append(user_info)
    else:
        return
    all_users_json = json.dumps(all_users_info, ensure_ascii=False, indent=4)
    with open('all_users_info.json', 'w', encoding='utf-8') as f:
        f.write(all_users_json)


all_users_info = []

if __name__ == '__main__':
    access_token = get_access_token(CORP_ID, CORP_SECRET)
    write()

