# -*- coding: utf-8-*-
# @Date    : 2018-02-08
# @Author  : yuhaifeng
# @Website :
# @Description1:  微信机器人
# @Tools-Required: itchat, requests
import itchat
import requests
from itchat.content import *
from coin.coinmarketcap import CoinData

coin = CoinData()


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    if firstReply(msg):
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
        if firstReply(msg):
            tuling(msg)


# 过滤虚拟货币回复
def firstReply(msg):
    symbol = msg.text.upper()
    if symbol in coin.coin:
        for i in coin.getCoinInfo(symbol):
            itchat.send('%s\n%s\n%s\n%s\n%s\n%s' % (
                u'名称: ' + isNone(i['name']), u'当前价格: ¥' + isNone(i['price_cny']),
                u'市值: ¥' + isNone(i['market_cap_cny']),
                u'流通总量: ' + isNone(i['total_supply']), u'24小时交易量: ' + isNone(i['24h_volume_cny']),
                u'近1小时波动: ' + isNone(i['percent_change_1h']) + '%',),
                        msg['FromUserName'])
        return False
    return True


def isNone(str):
    return '--' if str == None else str


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
        url = r.get('url')
        text = r.get('text')

        if url:
            itchat.send('%s\n%s' % (text, url), msg['FromUserName'])
        else:
            itchat.send('%s' % (text), msg['FromUserName'])
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
        # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return


itchat.auto_login(True)
itchat.run(True)
