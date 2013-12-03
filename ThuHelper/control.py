# coding=utf-8

# control.py
# 消息处理的逻辑
# 判断用户发送消息的用途
# 返回用户不同类型不同内容的消息

from message import *
from library import getLibrarySeatText, getLibrarySeatNews
from helpInfo import getHelpInfoArticles

def processMessage(message):
    # 根据用户发来的消息返回对应的消息
    if message['MsgType'] == 'text':
        if u'文图' in message['Content'] or u'人文馆' in message['Content']:
            # 用户查询人文图书馆座位信息
            response = getLibrarySeatText()
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
        elif message['Content'] in ['?', 'help', u'？', u'帮助']:
            # 帮助信息
            articles = getHelpInfoArticles()
            return makeNewsMessage(message['FromUserName'], message['ToUserName'], articles)
        elif 'test' in message['Content']:
            # 测试通道
            articles = getLibrarySeatNews()
            return makeNewsMessage(message['FromUserName'], message['ToUserName'], articles)
        else:
            # 文字消息原样返回
            response = message['Content']
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
    else:
        # 其他类型的消息不支持
        response = u'暂不支持非文字消息'
        return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
