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


def get_user_detail(access_token, userid):
    """根据userid获取成员详细信息（过滤后版本）"""
    url = "https://qyapi.weixin.qq.com/cgi-bin/user/get"
    params = {
        "access_token": access_token,
        "userid": userid
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data.get('errcode') != 0:
        raise Exception(f"查询用户失败: {data}")

    # 提取所需字段并返回新字典
    return {
        "name": data.get('name', ''),
        "userid": data.get('userid', ''),
        "mobile": data.get('mobile', ''),
        "email": data.get('email', '')
    }


# 配置信息（需要替换为实际值）
CORP_ID = "wwf7b517dadde6fcc6"
CORP_SECRET = "hPUCEvAKMm3o8X6pWNLtF89dKQyDkJhuktiGefpKyjo"

try:
    # 获取access_token
    access_token = get_access_token(CORP_ID, CORP_SECRET)

    # 示例用法：先获取所有userid
    all_users = get_all_users(access_token)
    userids = [user['userid'] for user in all_users]

    # 查询并打印第一个用户的详细信息
    if userids:
        first_user_detail = get_user_detail(access_token, userids[0])
        print("\n首个用户详细信息：")
        print(f"姓名：{first_user_detail['name']}")
        print(f"UserID：{first_user_detail['userid']}")
        print(f"手机号：{first_user_detail['mobile']}")
        print(f"邮箱：{first_user_detail['email']}")

    # 查询所有用户的详细信息（示例遍历）
    all_details = []
    for uid in userids:
        try:
            detail = get_user_detail(access_token, uid)
            all_details.append(detail)
        except Exception as e:
            print(f"查询用户 {uid} 失败: {str(e)}")

    # 打印统计信息
    print(f"\n成功获取 {len(all_details)}/{len(userids)} 个用户的详细信息")

except Exception as e:
    print(f"程序执行出错: {e}")