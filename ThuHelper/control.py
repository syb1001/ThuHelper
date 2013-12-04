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
        content = message['Content']
        fromUser = message['FromUserName']
        toUser = message['ToUserName']
        if u'文图' in content or u'人文馆' in content:
            # 用户查询人文图书馆座位信息
            response = getLibrarySeatText()
            return makeTextMessage(fromUser, toUser, response)
        elif content in ['?', 'help', u'？', u'帮助']:
            # 帮助信息
            articles = getHelpInfoArticles()
            return makeNewsMessage(fromUser, toUser, articles)
        elif u'教' in content:
            # 查询教室排课信息
            articles = getClassroomInfoArticles(content)
            return makeNewsMessage(fromUser, toUser, articles)
        elif 'test' in content:
            # 测试通道
            articles = getLibrarySeatNews()
            return makeNewsMessage(fromUser, toUser, articles)
        else:
            # 文字消息原样返回
            response = content
            return makeTextMessage(fromUser, toUser, response)
    else:
        # 其他类型的消息不支持
        response = u'暂不支持非文字消息'
        return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
