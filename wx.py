from flask import Flask
import hashlib
from flask import request
from flask import make_response
import time
import xml.etree.ElementTree as ET

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        print('coming Get')
        data = request.args
        token = 'weixin'
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        my_list = [token, timestamp, nonce]
        my_list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, my_list)
        hashcode = sha1.hexdigest()
        # if hashcode == signature:
        #     return make_response(ecshostr)
        if hashcode == signature:
            return echostr
        else:
            return 'failed'
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        msgType = xml_rec.find("MsgType").text
        content = xml_rec.find('Content').text
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = make_response(xml_rep % (fromu, tou, str(int(time.time())), "text", "test123"))
        response.content_type = 'application/xml'
        return response


if __name__ == '__main__':
    app.run()
