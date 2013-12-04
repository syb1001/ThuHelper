# coding=utf-8

# control.py
# 消息处理的逻辑
# 判断用户发送消息的用途
# 返回用户不同类型不同内容的消息

from message import *
from library import getLibrarySeatText, getLibrarySeatNews
from helpInfo import getHelpInfoArticles
from music import getRandomMusic
from classroom import getClassroomInfoArticles, getClassroomInfoArticles_simple

def processMessage(message):
    # 根据用户发来的消息返回对应的消息
    if message['MsgType'] == 'text':
        if message['Content'] in ['?', 'help', u'？', u'帮助']:
            # 帮助信息
            articles = getHelpInfoArticles()
            return makeNewsMessage(message['FromUserName'], message['ToUserName'], articles)
        elif u'人文馆' in message['Content']:
            # 用户查询人文馆座位信息
            # 以图文消息形式返回
            articles = getLibrarySeatNews()
            return makeNewsMessage(message['FromUserName'], message['ToUserName'], articles)
        elif u'文图' in message['Content']:
            # 用户查询人文图书馆座位信息
            # 以文字消息形式返回
            response = getLibrarySeatText()
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
        elif u'教' in message['Content']:
            # 查询教室排课信息
            articles = getClassroomInfoArticles(message['Content'])
            return makeNewsMessage(message['FromUserName'], message['ToUserName'], articles)
        elif message['Content'].startswith('#'):
            # 查询教室排课信息, 简单版本
            articles = getClassroomInfoArticles_simple(message['Content'])
            return makeNewsMessage(message['FromUserName'], message['ToUserName'], articles)
        elif u'音乐' in message['Content']:
            music = getRandomMusic()
            return makeMusicMessage(message['FromUserName'], message['ToUserName'], music)
        elif 'test' in message['Content']:
            # 测试通道
            response = message['Content']
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
        else:
            # 文字消息原样返回
            response = message['Content']
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
    else:
        # 其他类型的消息不支持
        response = u'暂不支持非文字消息'
        return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
