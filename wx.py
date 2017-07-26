# coding=utf-8
from flask import Flask
import hashlib
from flask import request
from flask import make_response
import time
import xml.etree.ElementTree as ET
import re
import json
import requests

app = Flask(__name__)


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return "hello"


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
        xml_str = request.stream.read()
        xml = ET.fromstring(xml_str)
        toUserName = xml.find('ToUserName').text
        fromUserName = xml.find('FromUserName').text
        createTime = xml.find('CreateTime').text
        msgType = xml.find('MsgType').text
        reply_xml = '''
                        <xml>
                        <ToUserName><![CDATA[%s]]></ToUserName>
                        <FromUserName><![CDATA[%s]]></FromUserName>
                        <CreateTime>%s</CreateTime>
                        <MsgType><![CDATA[%s]]></MsgType>
                        <Content><![CDATA[%s]]></Content>
                        </xml>
                        '''
        if msgType == 'text':
            content = xml.find("Content").text
            re_result = re.match(u"(快递)(\d)*$", content)
            if content == 'help':
                reply = reply_xml % (
                    fromUserName,
                    toUserName,
                    createTime,
                    'text',
                    'Unknow Format, Please check out'
                )
                return reply
            elif content == 'Sam':
                reply = reply_xml % (
                    fromUserName,
                    toUserName,
                    createTime,
                    'text',
                    'Sam is fucking hot!'
                )
                return reply
            elif content == u'测试':
                reply = reply_xml % (
                    fromUserName,
                    toUserName,
                    createTime,
                    'text',
                    u'测试一下'
                )
                return reply
            elif re_result:
                reply = reply_xml % (
                    fromUserName,
                    toUserName,
                    createTime,
                    'text',
                    u'测试一下'
                )
            elif content == u'嘉兴天气':
                query_url = "http://tj.nineton.cn/Heart/index/all?city=CHZJ020000&language=&unit=&aqi=&alarm=&key="
                result = requests.get(query_url)
                result_text = result.text
                json_text = json.loads(result_text)
                now_weather = json_text['weather'][0]['now']
                future_weather = json_text['weather'][0]['future']
                a = u"今日天气: " + now_weather['text'] + "\n" + u"温度: " + now_weather['temperature'] + "\n" + u"体感温度: " + \
                    now_weather[
                        'feels_like'] + "\n" + u"湿度: " + \
                    now_weather['humidity'] + "\n" + u"pm2.5: " + now_weather['air_quality']['city'][
                        'pm25'] + "\n" + u"空气质量: " + \
                    now_weather['air_quality']['city']['quality'] + "\n\n\n"

                for i in future_weather:
                    date = i['date']
                    day = i['day']
                    text = i['text']
                    high = i['high']
                    low = i['low']
                    a = a + date + '\n' + day + ':' + text + '\n' + u"温度" + low + '-' + high + '\n\n'
                reply = reply_xml % (
                    fromUserName,
                    toUserName,
                    createTime,
                    'text',
                    a
                )
                return reply

            else:
                reply = reply_xml % (
                    fromUserName,
                    toUserName,
                    createTime,
                    'text',
                    'no nothing'
                )
                return reply

        if msgType == "event":
            mscontent = xml.find("Event").text
            if mscontent == "subscribe":
                reply_text = 'thx for subscribe'
                reply = reply_xml % (
                    fromUserName,
                    toUserName,
                    createTime,
                    'text',
                    reply_text
                )
                return reply
            if mscontent == "unsubscribe":
                reply_text = 'bye'
                reply = reply_xml % (
                    fromUserName,
                    toUserName,
                    createTime,
                    'text',
                    reply_text
                )
                return reply


if __name__ == '__main__':
    app.run()
