from flask import abort, request
from flask import Flask
from xml.dom.minidom import parseString
import _thread
import time
import os
import sys

sys.path.append("weworkapi/callback")
from WXBizMsgCrypt3 import WXBizMsgCrypt  # 对应接受消息回调模式中的EncodingAESKey 和 企业信息中的EncodingAESKey
app = Flask(__name__)


# 对应步骤4中接受消息回调模式中的URL，如域名是'www.example.com' 那么在步骤4中填入的url就为"http://www.example.com/hook_path"
@app.route('/hook_path', methods=['GET', 'POST'])
def douban():
    if request.method == 'GET':
        echo_str = signature(request, 0)
        return (echo_str)
    elif request.method == 'POST':
        echo_str = signature2(request, 0)
        return (echo_str)


qy_api = [
    WXBizMsgCrypt("Bj35", "7DYzzFxM4kIDoVYFTQL5n75LxNIvSgRBNALzWyxgaVF", "wwf7b517dadde6fcc6"),
]


# 开启消息接受模式时验证接口连通性
def signature(request, i):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    ret, sEchoStr = qy_api[i].VerifyURL(msg_signature, timestamp, nonce, echo_str)
    if (ret != 0):
        print("ERR: VerifyURL ret: " + str(ret))
        return ("failed")
    else:
        return (sEchoStr)


# 实际接受消息
def signature2(request, i):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    data = request.data.decode('utf-8')
    ret, sMsg = qy_api[i].DecryptMsg(data, msg_signature, timestamp, nonce)
    if (ret != 0):
        print("ERR: DecryptMsg ret: " + str(ret))
        return ("failed")
    else:
        with open("/var/log/qywx.log", 'a+') as f:  # 消息接收日志
            doc = parseString(sMsg)
            collection = doc.documentElement
            name_xml = collection.getElementsByTagName("FromUserName")
            msg_xml = collection.getElementsByTagName("Content")
            type_xml = collection.getElementsByTagName("MsgType")
            pic_xml = collection.getElementsByTagName("PicUrl")
            msg = ""
            name = ""
            msg_type = type_xml[0].childNodes[0].data
            if msg_type == "text":  # 文本消息
                name = name_xml[0].childNodes[0].data  # 发送者id
                msg = msg_xml[0].childNodes[0].data  # 发送的消息内容
                f.write(time.strftime('[%Y-%m-%d %H:%M:%S]') + "[ch%d] %s:%s\n" % (i, name, msg))
                _thread.start_new_thread(os.system, (
                "python3 command.py '%s' '%s' '%d' '%d'" % (name, msg, i, 0),))  # 此处将消息进行外部业务处理

            elif msg_type == "image":  # 图片消息
                name = name_xml[0].childNodes[0].data
                pic_url = pic_xml[0].childNodes[0].data
                f.write(time.strftime('[%Y-%m-%d %H:%M:%S]') + "[ch%d] %s:图片消息\n" % (i, name))
                _thread.start_new_thread(os.system, (
                "python3 command.py '%s' '%s' '%d' '%d'" % (name, pic_url, i, 1),))  # 此处将消息进行外部业务处理

            f.close()

        return ("ok")


if __name__ == '__main__':
    app.run("0.0.0.0", port=5000,debug=True)  # 本地监听端口,可自定义