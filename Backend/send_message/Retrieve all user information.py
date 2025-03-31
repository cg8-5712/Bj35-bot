import requests
import csv

# 配置参数 - 需替换为实际值
CORP_ID = "wwf7b517dadde6fcc6"  # 企业ID
CONTACT_SYNC_SECRET = "7KcKcZOGvpfczfC7Lg260fr8WV2kolVi0qDQryw5pNM"  # 通讯录同步Secret
OUTPUT_FILENAME = "wecom_users.csv"  # 输出文件名


def get_access_token(corpid, secret):
    """获取企业微信API访问令牌"""
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={secret}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        result = response.json()
        if result.get("errcode") == 0:
            return result.get("access_token")
        print(f"获取Token失败：{result.get('errmsg')}")
        return None
    except Exception as e:
        print(f"Token获取异常：{str(e)}")
        return None


def get_all_userids(token):
    """获取所有成员UserID列表（支持分页）"""
    user_ids = set()
    cursor = ""
    retry_count = 0

    while retry_count < 3:  # 失败重试机制
        try:
            while True:
                url = "https://qyapi.weixin.qq.com/cgi-bin/user/list_id"
                params = {"access_token": token}
                data = {"cursor": cursor, "limit": 10000}

                response = requests.post(
                    url,
                    params=params,
                    json=data,
                    timeout=15
                )
                result = response.json()

                if result.get("errcode") != 0:
                    print(f"获取UserID失败：{result.get('errmsg')}")
                    return None

                # 收集UserID
                for item in result.get("dept_user", []):
                    user_ids.add(item["userid"])

                # 检查分页
                next_cursor = result.get("next_cursor")
                if not next_cursor:
                    return list(user_ids)

                cursor = next_cursor

        except requests.exceptions.RequestException as e:
            retry_count += 1
            print(f"网络错误，正在重试({retry_count}/3)...")

    print("获取UserID重试次数超限")
    return None


def get_user_details(token, userid):
    """获取用户详细信息"""
    url = "https://qyapi.weixin.qq.com/cgi-bin/user/get"
    params = {
        "access_token": token,
        "userid": userid
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        result = response.json()

        if result.get("errcode") == 0:
            return {
                "userid": userid,
                "name": result.get("name", "N/A"),
                "alias": result.get("alias", "N/A"),
                "department": ",".join(map(str, result.get("department", []))),
                "status": result.get("status", 0)
            }
        print(f"获取用户[{userid}]详情失败：{result.get('errmsg')}")
        return None

    except Exception as e:
        print(f"获取用户[{userid}]详情异常：{str(e)}")
        return None


def export_to_csv(data, filename=OUTPUT_FILENAME):
    """导出数据到CSV文件"""
    if not data:
        print("无有效数据可导出")
        return False

    try:
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["昵称", "Userid", "别名", "部门", "状态"])
            writer.writeheader()

            for item in data:
                writer.writerow({
                    "昵称": item.get("name"),
                    "Userid": item.get("userid"),
                    "别名": item.get("alias"),
                    "部门": item.get("department"),
                    "状态": {
                        1: "已激活",
                        2: "已禁用",
                        4: "未激活"
                    }.get(item.get("status"), "未知状态")
                })
        return True
    except Exception as e:
        print(f"导出文件失败：{str(e)}")
        return False


def main():
    # 获取访问令牌
    access_token = get_access_token(CORP_ID, CONTACT_SYNC_SECRET)
    if not access_token:
        return

    # 获取所有UserID
    print("正在获取成员列表...")
    userids = get_all_userids(access_token)
    if not userids:
        print("未获取到有效UserID列表")
        return

    # 获取详细信息
    print(f"开始获取{len(userids)}位成员详情...")
    user_details = []
    for index, uid in enumerate(userids, 1):
        detail = get_user_details(access_token, uid)
        if detail:
            user_details.append(detail)
        # 打印进度（每50人更新一次）
        if index % 50 == 0 or index == len(userids):
            print(f"进度：{index}/{len(userids)} ({index / len(userids):.1%})")

    # 导出数据
    if export_to_csv(user_details):
        print(f"数据已成功导出到 {OUTPUT_FILENAME}")
    else:
        print("数据导出失败")


if __name__ == "__main__":
    main()