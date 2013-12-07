# coding=utf-8

# control.py
# 消息处理的逻辑
# 判断用户发送消息的用途
# 返回用户不同类型不同内容的消息

from message import *
from library import getLibrarySeatText, getLibrarySeatNews
from helpInfo import getHelpInfoArticles
from music import getRandomMusic
from classroom import getClassroomInfo, getRoomCourseInfo

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
        elif message['Content'].startswith('#'):
            # 查询教室排课信息, 简单版本
            response = getClassroomInfo(message['Content'])
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
        elif u'音乐' in message['Content']:
            # 随机播放一首音乐
            music = getRandomMusic()
            return makeMusicMessage(message['FromUserName'], message['ToUserName'], music)
        elif 'test' in message['Content']:
            # 测试通道
            response = message['Content']
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
        else:
            # 判断输入是否为某个教室
            # 若是一个教室则返回教室信息
            # 否则原样返回
            response = getRoomCourseInfo(message['Content'])
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
    elif message['MsgType'] == 'event':
        if message['Event'] == 'subscribe':
            response = u'欢迎关注清华自习小助手，请发送“帮助”或“help”查看帮助信息~'
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
        elif message['Event'] == 'CLICK':
            '''response = u'点也白点，没写完呢'
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)'''
            if message['EventKey'] == 'JSPKCX':
                response = u'请输入教室编号（例如：6B201，4101..）'
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
            elif message['EventKey'] == 'WTZWCX':
                articles = getLibrarySeatNews()
                return makeNewsMessage(message['FromUserName'], message['ToUserName'], articles)
            elif message['EventKey'] == 'JXLCX':
                response = u'请输入楼层（例如：#4,2...）'
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
            #推荐吃饭地点
            elif message['EventKey'] == 'QNC':
                response = u'点也白点，没写完呢'
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
            #推荐自习室
            elif message['EventKey'] == 'QNX':
                response = u'点也白点，没写完呢'
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
            #推荐音乐
            elif message['EventKey'] == 'LDYY':
                music = getRandomMusic()
                return makeMusicMessage(message['FromUserName'], message['ToUserName'], music)
            #签到
            elif message['EventKey'] == 'QD':
                response = u'点也白点，没写完呢'
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
            
            elif message['EventKey'] == 'HELP':
                articles = getHelpInfoArticles()
                return makeNewsMessage(message['FromUserName'], message['ToUserName'], articles)
            elif message['EventKey'] == 'ABOUT':
                response = u'只是一群被软工虐的机智程序员。。。'
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
            else:
                response = u'点也白点，没写完呢'
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
            
    else:
        # 其他类型的消息不支持
        response = u'暂不支持非文字消息'
        return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
