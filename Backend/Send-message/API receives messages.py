from flask import Flask, request, abort
import hashlib
import time
from Crypto.Cipher import AES
import base64
import xml.etree.ElementTree as ET

app = Flask(__name__)

# 企业微信后台配置的参数
CORP_ID = "wwf7b517dadde6fcc6"
TOKEN = "Bj35"  # 必须与后台配置一致
EncodingAESKey = "uUlW6riwCinyk5fo0iucDLTMGrhB6dq1BPSQo8pZVzA"  # 43位字符


class WXBizMsgCrypt:
    # 此处应实现企业微信官方提供的加解密类
    # 完整代码需从官方文档获取：https://developer.work.weixin.qq.com/document/path/90539
    pass


@app.route('/send_message', methods=['GET', 'POST'])
def wecom_callback():
    # 处理验证请求
    if request.method == 'GET':
        msg_signature = request.args.get('msg_signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        print("msg_signature: ",msg_signature)
        print("timestamp: ",timestamp)
        print("nonce: ",nonce)
        print("echostr: ",echostr)
        # # 验证签名
        # crypt = WXBizMsgCrypt(TOKEN, EncodingAESKey, CORP_ID)
        # ret, decrypt_echostr = crypt.VerifyURL(msg_signature, timestamp, nonce, echostr)
        #
        # if ret != 0:
        #     abort(403)
        # return decrypt_echostr  # 必须直接返回解密后的明文

    # 后续处理其他消息（POST请求）
    else:
        # 处理消息逻辑...
        return "success"


if __name__ == '__main__':
    app.run(debug=True)