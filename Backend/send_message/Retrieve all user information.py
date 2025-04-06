import requests
import pandas as pd
from time import time

'''
35中企业：
企业ID：ww8e4628d565c6588f
应用Secret：f03d8WfJfKpgX3NG84pXMaN7a6G1xOY2QummZNZh_Xg
应用AgentId：1000166

我的企业：
企业ID：wwf7b517dadde6fcc6
应用Secret：hPUCEvAKMm3o8X6pWNLtF89dKQyDkJhuktiGefpKyjo
应用AgentId：1000002
'''


class WeComAPI:
    def __init__(self, corpid, corpsecret):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.token_expire = 0
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
                self.token_expire = time() + data["expires_in"] - 60
                return True
            else:
                print(f"获取access_token失败: {data}")
        except Exception as e:
            print(f"网络请求异常: {str(e)}")
        return False

    def get_all_users_basic(self):
        """获取所有成员基础信息"""
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

    def export_to_excel(self, filename="user_list.xlsx"):
        """导出用户名和userid到Excel"""
        users = self.get_all_users_basic()
        if not users:
            print("没有获取到用户数据")
            return False

        # 提取需要的字段
        data = []
        for user in users:
            data.append({
                "姓名": user.get("name", ""),
                "UserID": user.get("userid", "")
            })

        # 创建DataFrame并保存
        try:
            df = pd.DataFrame(data)
            df.to_excel(filename, index=False, engine="openpyxl")
            print(f"成功导出 {len(df)} 条数据到 {filename}")
            return True
        except Exception as e:
            print(f"导出Excel失败: {str(e)}")
            print("请确保已安装依赖库：pip install pandas openpyxl")
            return False


# 使用示例
if __name__ == "__main__":
    # 配置企业信息
    CORP_ID = "ww8e4628d565c6588f"
    CORP_SECRET = "f03d8WfJfKpgX3NG84pXMaN7a6G1xOY2QummZNZh_Xg"

    wecom = WeComAPI(CORP_ID, CORP_SECRET)

    # 导出到Excel
    if wecom.export_to_excel():
        print("导出成功！")
    else:
        print("导出失败")