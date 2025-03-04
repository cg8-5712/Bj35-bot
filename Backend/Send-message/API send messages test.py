import base64
import hashlib
import random
import string
import time
from urllib.parse import urlencode
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


class WXWorkMessageSimulator:
    def __init__(self, token, encoding_aes_key):
        """
        初始化参数
        :param token: 企业微信后台配置的 Token
        :param encoding_aes_key: 企业微信后台配置的 EncodingAESKey（43 位字符串）
        """
        self.token = token
        self.encoding_aes_key = encoding_aes_key
        self.aes_key = base64.b64decode(encoding_aes_key + "=")  # 补齐 44 位并解码

    def _generate_random_str(self, length=16):
        """生成指定长度的随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def _encrypt(self, plaintext):
        """
        AES 加密（CBC 模式，PKCS#7 填充）
        :param plaintext: 待加密的明文
        :return: 加密后的 base64 字符串
        """
        # 生成 16 字节随机字符串
        random_str = self._generate_random_str(16)
        byte_plaintext = plaintext.encode("utf-8")
        byte_random_str = random_str.encode("utf-8")

        # 拼接明文： [16字节随机字符串] + [4字节消息长度] + [明文] + [企业CorpID]
        msg_len = len(byte_plaintext).to_bytes(4, byteorder="big")
        full_plaintext = byte_random_str + msg_len + byte_plaintext + b"wwf7b517dadde6fcc6"  # CorpID 可留空或填写测试值
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=self.aes_key[:16])
        ciphertext = cipher.encrypt(pad(full_plaintext, AES.block_size))
        return base64.b64encode(ciphertext).decode("utf-8")

    def generate_verify_request(self, plaintext="Though the path be broken and uncertain, claim your place as Elden Lord"):
        """
        生成模拟企业微信验证服务器的 GET 请求参数
        :param plaintext: 明文 echostr（默认值可自定义）
        :return: 包含签名参数的字典
        """
        # 生成参数
        timestamp = str(int(time.time()))
        nonce = self._generate_random_str(8)
        encrypted_echostr = self._encrypt(plaintext)

        # 计算签名
        signature_list = sorted([self.token, timestamp, nonce, encrypted_echostr])
        signature_str = "".join(signature_list)
        signature = hashlib.sha1(signature_str.encode("utf-8")).hexdigest()

        return {
            "msg_signature": signature,
            "timestamp": timestamp,
            "nonce": nonce,
            "echostr": encrypted_echostr
        }


if __name__ == "__main__":
    # ------------------ 配置参数 ------------------
    TOKEN = "Bj35"  # 替换为企业微信后台配置的 Token
    ENCODING_AES_KEY = "7DYzzFxM4kIDoVYFTQL5n75LxNIvSgRBNALzWyxgaVF"  # 替换为 43 位的 EncodingAESKey

    # ------------------ 测试示例 ------------------
    simulator = WXWorkMessageSimulator(TOKEN, ENCODING_AES_KEY)
    params = simulator.generate_verify_request()

    # 发送模拟请求到你的本地服务器（替换为你的回调 URL）
    callback_url = "http://42.51.43.6:5000/hook_path"
    response = requests.get(callback_url, params=params)

    print("模拟请求参数:", params)
    print("服务器响应状态码:", response.status_code)
    print("服务器响应内容:", response.text)