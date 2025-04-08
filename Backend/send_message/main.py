import requests
import time


def get_access_token(corpid, corpsecret):
    """获取企业微信的access_token"""
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
    response = requests.get(url)
    data = response.json()
    if data.get('errcode') == 0:
        return data['access_token']
    else:
        raise Exception(f"获取access_token失败: {data}")


def get_all_departments(access_token, root_id=1):
    """递归获取所有子部门信息（包含部门详情）"""

    def _recursive_get(dept_id):
        # 获取部门详情
        detail = get_department_detail(access_token, dept_id)
        departments.append(detail)

        # 获取子部门列表
        sub_depts = get_sub_departments(access_token, dept_id)
        for sub in sub_depts:
            _recursive_get(sub['id'])

    departments = []
    try:
        _recursive_get(root_id)
    except Exception as e:
        print(f"获取部门信息时出错: {e}")
    return departments


def get_sub_departments(access_token, department_id):
    """获取指定部门的直接子部门列表"""
    url = "https://qyapi.weixin.qq.com/cgi-bin/department/simplelist"
    params = {
        "access_token": access_token,
        "id": department_id
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get('errcode') != 0:
        raise Exception(f"获取子部门失败: {data}")
    return data.get('department_id_list', [])


def get_department_detail(access_token, department_id):
    """获取部门详细信息"""
    url = "https://qyapi.weixin.qq.com/cgi-bin/department/get"
    params = {
        "access_token": access_token,
        "id": department_id
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get('errcode') != 0:
        raise Exception(f"获取部门详情失败: {data}")
    return {
        "id": department_id,
        "name": data.get('name', ''),
        "parentid": data.get('parentid', 0),
        "order": data.get('order', 0)
    }


def get_users_in_department(access_token, department_id):
    """分页获取部门成员（不包含子部门）"""
    url = "https://qyapi.weixin.qq.com/cgi-bin/user/list"
    users = []
    page = 0
    page_size = 100  # 最大支持100

    while True:
        params = {
            "access_token": access_token,
            "department_id": department_id,
            "fetch_child": 0,
            "page": page,
            "page_size": page_size
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data.get('errcode') != 0:
            raise Exception(f"获取部门成员失败: {data}")

        users.extend(data.get('userlist', []))
        if len(data.get('userlist', [])) < page_size:
            break

        page += 1
        time.sleep(0.5)  # 控制请求频率

    return users


def get_user_detail(access_token, userid):
    """获取用户详细信息（精简版）"""
    url = "https://qyapi.weixin.qq.com/cgi-bin/user/get"
    params = {
        "access_token": access_token,
        "userid": userid
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data.get('errcode') != 0:
        raise Exception(f"查询用户失败: {data}")

    return {
        "name": data.get('name', ''),
        "userid": data.get('userid', ''),
        "mobile": data.get('mobile', ''),
        "email": data.get('email', '')
    }


# 配置信息
CORP_ID = "ww8e4628d565c6588f"
CORP_SECRET = "f03d8WfJfKpgX3NG84pXMZOaZ0E_xW9NuaP68ImWtUE"

try:
    # 获取访问凭证
    access_token = get_access_token(CORP_ID, CORP_SECRET)

    # 步骤1：获取全量部门信息
    print("开始获取组织架构...")
    all_departments = get_all_departments(access_token)
    print(f"获取到 {len(all_departments)} 个部门")

    # 步骤2：遍历所有部门获取成员
    print("\n开始收集成员信息...")
    all_users = []
    seen_userids = set()

    for dept in all_departments:
        try:
            dept_id = dept['id']
            users = get_users_in_department(access_token, dept_id)

            for user in users:
                uid = user['userid']
                if uid not in seen_userids:
                    seen_userids.add(uid)
                    all_users.append(user)

            print(f"部门 {dept['name']}({dept_id}) 处理完成，累计用户数：{len(seen_userids)}")
        except Exception as e:
            print(f"处理部门 {dept['name']}({dept_id}) 时出错: {e}")

    # 步骤3：获取详细信息
    print("\n开始获取详细信息...")
    results = []
    for idx, user in enumerate(all_users, 1):
        try:
            detail = get_user_detail(access_token, user['userid'])
            results.append(detail)
            print(f"进度：{idx}/{len(all_users)}", end='\r')
            time.sleep(0.3)  # 控制请求频率
        except Exception as e:
            print(f"获取用户 {user['userid']} 详情失败: {e}")

    # 输出结果
    print("\n\n最终结果：")
    print(f"成功获取 {len(results)} 个用户的完整信息")
    for user in results:
        print(f"{user['name']} | {user['userid']} | {user['mobile']} | {user['email']}")

except Exception as e:
    print(f"程序执行出错: {e}")