import requests
import json

class WeComAPI:
    def __init__(self, corpid, corpsecret):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.access_token = None

    def get_access_token(self):
        """获取access_token"""
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            "corpid": self.corpid,
            "corpsecret": self.corpsecret
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("errcode") == 0:
            self.access_token = data["access_token"]
            return True
        else:
            print(f"获取access_token失败: {data}")
            return False

    def get_all_users(self):
        """获取所有成员信息"""
        if not self.access_token:
            if not self.get_access_token():
                return None

        url = "https://qyapi.weixin.qq.com/cgi-bin/user/list"
        params = {
            "access_token": self.access_token,
            "department_id": 1,  # 根部门ID
            "fetch_child": 1  # 递归获取子部门成员
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data.get("errcode") == 0:
            return data["userlist"]
        else:
            print(f"获取成员列表失败: {data}")
            return None

    def get_all_userids(self):
        """获取所有成员的userid列表"""
        users = self.get_all_users()
        if users:
            return [user["userid"] for user in users]
        return []


# 使用示例
if __name__ == "__main__":
    # 需要替换为你的企业信息
    CORP_ID = "wwf7b517dadde6fcc6"
    CORP_SECRET = "hPUCEvAKMm3o8X6pWNLtF89dKQyDkJhuktiGefpKyjo"

    wecom = WeComAPI(CORP_ID, CORP_SECRET)

    if wecom.get_access_token():
        userids = wecom.get_all_userids()
        if userids:
            print("成功获取所有成员userid：")
            for idx, userid in enumerate(userids, 1):
                print(f"{idx}. {userid}")
            print(f"\n总计成员数量：{len(userids)}")
        else:
            print("未能获取到成员列表")