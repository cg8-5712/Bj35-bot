import requests
import hashlib
import time
from urllib.parse import urlencode
import random
import string

# 配置参数（必须与企业微信后台一致）
token = "Bj35"  # 替换为企业后台配置的Token
encoding_aes_key = "uUlW6riwCinyk5fo0iucDLTMGrhB6dq1BPSQo8pZVzA"  # 43位字符（可选，测试基础验证时可暂不填）
corp_id = "wwf7b517dadde6fcc6"  # 企业微信官网获取


# 生成测试用参数
def generate_test_params():
    # 生成随机参数
    timestamp = str(int(time.time()))
    nonce = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    echostr = "hello world"  # 实际企业微信发送的是加密字符串

    # 生成签名（关键步骤）
    params = sorted([token, timestamp, nonce, echostr])
    param_str = ''.join(params)
    signature = hashlib.sha1(param_str.encode()).hexdigest()

    return {
        "msg_signature": signature,
        "timestamp": timestamp,
        "nonce": nonce,
        "echostr": echostr
    }


# 发送模拟请求
def send_validation_request(url):
    params = generate_test_params()

    response = requests.get(
        url=url,
        params=params,
        headers={"User-Agent": "WeCom-Server"}  # 模拟企业微信服务器UA
    )

    print(f"发送参数: {params}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")


if __name__ == "__main__":
    # 替换为你的服务器地址
    server_url = "http://127.0.0.1:5000/send_message"  # 根据实际路由修改
    send_validation_request(server_url)