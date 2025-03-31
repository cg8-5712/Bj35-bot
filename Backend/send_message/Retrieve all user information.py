import requests
import csv

# 配置参数
CORP_ID = "wwf7b517dadde6fcc6"
CONTACT_SYNC_SECRET = "hPUCEvAKMm3o8X6pWNLtF89dKQyDkJhuktiGefpKyjo"

def get_access_token(corpid, secret):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={secret}"
    response = requests.get(url)
    return response.json().get('access_token')


def get_departments(token):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token={token}"
    response = requests.get(url)
    departments = response.json().get('department', [])
    return [dept['id'] for dept in departments]


def get_department_members(token, department_id):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/user/list?access_token={token}&department_id={department_id}&fetch_child=1"
    response = requests.get(url)
    return response.json().get('userlist', [])


def export_to_csv(users, filename='wecom_contacts.csv'):
    if not users:
        print("没有可导出的数据")
        return

    # 获取所有可能的字段
    all_fields = set()
    for user in users:
        all_fields.update(user.keys())

    # 定义CSV列顺序（可根据需要调整）
    field_order = [
        'userid', 'name', 'mobile', 'email',
        'position', 'department', 'gender', 'status'
    ]

    # 写入文件
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=field_order + list(all_fields - set(field_order)))
        writer.writeheader()
        for user in users:
            # 处理部门字段（数组转字符串）
            user = user.copy()
            user['department'] = ','.join(map(str, user.get('department', [])))
            writer.writerow(user)


def main():
    # 获取访问令牌
    token = get_access_token(CORP_ID, CONTACT_SYNC_SECRET)
    if not token:
        print("获取access_token失败，请检查配置")
        return

    # 获取所有部门
    departments = get_departments(token)
    if not departments:
        print("未获取到部门信息")
        return

    # 获取所有成员
    all_users = []
    seen_userids = set()  # 用于去重

    for dept_id in departments:
        members = get_department_members(token, dept_id)
        for user in members:
            if user['userid'] not in seen_userids:
                all_users.append(user)
                seen_userids.add(user['userid'])

    # 导出到CSV
    if all_users:
        export_to_csv(all_users)
        print(f"成功导出{len(all_users)}条通讯录信息")
    else:
        print("未获取到成员信息")


if __name__ == "__main__":
    main()