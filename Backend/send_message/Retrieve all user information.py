import requests
import json
from time import time


class WeComAPI:
    def __init__(self, corpid, corpsecret):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.token_expire = 0  # token过期时间戳
        self.access_token = ""

    def _get_access_token(self):
        """获取并缓存access_token"""
        if time() < self.token_expire and self.access_token:
            return True

        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            "corpid": self.corpid,
            "corpsecret": self.corpsecret
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            if data.get("errcode") == 0:
                self.access_token = data["access_token"]
                self.token_expire = time() + data["expires_in"] - 60  # 提前60秒刷新
                return True
            else:
                print(f"获取access_token失败: {data}")
        except Exception as e:
            print(f"网络请求异常: {str(e)}")
        return False

    def get_all_users_basic(self):
        """获取所有成员基础信息（优化版本）"""
        if not self._get_access_token():
            return None

        url = "https://qyapi.weixin.qq.com/cgi-bin/user/list"
        params = {
            "access_token": self.access_token,
            "department_id": 1,
            "fetch_child": 1
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            if data.get("errcode") == 0:
                return data["userlist"]
            print(f"获取成员列表失败: {data}")
        except Exception as e:
            print(f"获取成员列表异常: {str(e)}")
        return None

    def get_user_detail(self, userid):
        """获取成员详细信息（包含手机号等敏感信息）"""
        if not self._get_access_token():
            return None

        url = "https://qyapi.weixin.qq.com/cgi-bin/user/get"
        params = {
            "access_token": self.access_token,
            "userid": userid
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            if data.get("errcode") == 0:
                return {
                    "userid": data["userid"],
                    "name": data.get("name", ""),
                    "mobile": data.get("mobile", ""),
                    "department": data.get("department", []),
                    "position": data.get("position", ""),
                    "gender": data.get("gender", 0),
                    "email": data.get("email", ""),
                    "status": data.get("status", 1)
                }
            print(f"获取用户 {userid} 详细信息失败: {data}")
        except Exception as e:
            print(f"获取用户 {userid} 信息异常: {str(e)}")
        return None

    def get_all_users_full_info(self):
        """获取所有成员的完整信息"""
        # 先获取基础用户列表
        basic_users = self.get_all_users_basic()
        if not basic_users:
            return None

        full_users = []
        success_count = 0
        total = len(basic_users)

        for idx, user in enumerate(basic_users, 1):
            print(f"正在获取 {user['userid']} 的详细信息 ({idx}/{total})...")
            detail = self.get_user_detail(user["userid"])
            if detail:
                # 合并基础信息和详细信息
                merged = {**user, **detail}
                full_users.append(merged)
                success_count += 1

        print(f"\n信息获取完成！成功获取 {success_count}/{total} 用户的信息")
        return full_users


# 使用示例
if __name__ == "__main__":
    # 配置企业信息
    CORP_ID = "wwf7b517dadde6fcc6"
    CORP_SECRET = "hPUCEvAKMm3o8X6pWNLtF89dKQyDkJhuktiGefpKyjo"

    wecom = WeComAPI(CORP_ID, CORP_SECRET)

    # 获取所有用户完整信息
    all_users = wecom.get_all_users_full_info()

    if all_users!= None:
        # 打印前5个用户信息示例
        print("\n用户信息示例：")
        for user in all_users:
            print(json.dumps(user, indent=2, ensure_ascii=False))

        # 可选：保存到文件
        # with open("wecom_users.json", "w", encoding="utf-8") as f:
        #     json.dump(all_users, f, indent=2, ensure_ascii=False)
        #     print("\n已保存完整数据到 wecom_users.json")
    else:
        print("未能获取用户信息")