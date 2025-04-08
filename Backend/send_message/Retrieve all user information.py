import requests


def get_access_token(corpid, corpsecret):
    """获取企业微信的access_token"""
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
    response = requests.get(url)
    data = response.json()
    if data.get('errcode') == 0:
        return data['access_token']
    else:
        raise Exception(f"获取access_token失败: {data}")


def get_all_users(access_token, department_id=1):
    """获取指定部门及其子部门的所有成员"""
    url = "https://qyapi.weixin.qq.com/cgi-bin/user/list"
    params = {
        "access_token": access_token,
        "department_id": department_id,
        "fetch_child": 1  # 递归获取子部门成员
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get('errcode') == 0:
        return data.get('userlist', [])
    else:
        raise Exception(f"获取成员列表失败: {data}")


# 配置信息（需要替换为实际值）
CORP_ID = "ww8e4628d565c6588f"  # 企业ID
CORP_SECRET = "f03d8WfJfKpgX3NG84pXMaN7a6G1xOY2QummZNZh_Xg"  # 应用的Secret

try:
    # 获取access_token
    access_token = get_access_token(CORP_ID, CORP_SECRET)
    print(f"access_token: {access_token}")
    # 获取所有成员信息（从根部门开始获取）
    all_users = get_all_users(access_token)

    # 提取所有userid
    userids = [user['userid'] for user in all_users]

    # 输出结果
    print(f"共获取到 {len(userids)} 个用户ID：")
    for uid in userids:
        print(uid)

except Exception as e:
    print(f"程序执行出错: {e}")