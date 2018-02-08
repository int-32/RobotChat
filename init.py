# -*- coding: utf-8-*-
# @Date    : 2018-02-08
# @Author  : yuhaifeng
# @Website :
# @Description1:  微信机器人
# @Tools-Required: itchat, requests
import itchat
import requests
from itchat.content import *


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    return tuling(msg)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    return '@%s@%s' % (typeSymbol, msg.fileName)


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('Nice to meet you!')


# 处理群聊消息
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    print(msg['ActualNickName'] + ': ' + msg['Content'])
    if msg['IsAt']:
        itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])
    else:
        remsg = tuling(msg)
        itchat.send('%s' % (remsg), msg['FromUserName'])


# 连接图灵机器人
def tuling(msg):
    apiUrl = "http://www.tuling123.com/openapi/api"
    key = '214d91b4afb342c184566dced153a367'

    data = {'key': key,
            'info': msg.text,
            'loc': '',
            'userid': msg.user['UserName']}
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
        # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
        # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return


itchat.auto_login(True)
itchat.run(True)
