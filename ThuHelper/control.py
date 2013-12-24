# coding=utf-8

# control.py
# 消息处理的逻辑
# 判断用户发送消息的用途
# 返回用户不同类型不同内容的消息

import types
from database import adduser, deluser
from message import *
from library import getLibrarySeatText, getLibrarySeatNews, isConsultingLibrary
from helpInfo import getHelpInfoArticles
from music import getRandomMusicByType, formMusicTypeList, getMusicByExpression, isTypeOfMusic, getTypeDict
from classroom import getRoomCourseInfo, classroom
from food import food_articles
from recommend_classroom import recommend_classroom
from signin import signin
from settings import URL_WELCOME_IMAGE, URL_HELP

def processMessage(message):

    if message['MsgType'] == 'text':
        # 取出首尾空格和换行
        message['Content'] = message['Content'].strip('\n')
        message['Content'] = message['Content'].strip(' ')
        # 根据用户发来的消息返回对应的消息
        if message['Content'] in ['?', 'help', u'？', u'帮助']:
            # 帮助信息
            articles = getHelpInfoArticles()
            return makeNewsMessage(message['FromUserName'], message['ToUserName'], articles)
        elif isConsultingLibrary(message['Content']):
            # 用户查询人文图书馆座位信息
            # 以文字消息形式返回
            response = getLibrarySeatText()
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
        elif message['Content'].startswith('/:'):
            # 用户发送表情则返回音乐
            response = getMusicByExpression(message['Content'])
            if (type(response) is types.UnicodeType) or (type(response) is types.StringType):
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
            else:
                return makeMusicMessage(message['FromUserName'], message['ToUserName'], response)
        elif u'教' in message['Content']:
            # 查询教室排课信息, 处理的是文字输入
            response = classroom(message['Content'])
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
        elif isTypeOfMusic(message['Content']):
            # 根据音乐类型返回音乐消息
            dict = getTypeDict(message['Content'])
            music = getRandomMusicByType(dict)
            if music['Title'] == '':
                return makeTextMessage(message['FromUserName'], message['ToUserName'], '抱歉，未找到该类型的音乐，换个类型试试吧~')
            else:
                return makeMusicMessage(message['FromUserName'], message['ToUserName'], music)
        elif message['Content'] == u'签到':
            # 输文字签到
            response = signin(message['FromUserName'], message['CreateTime'])
            return makeNewsMessage(message['FromUserName'], message['ToUserName'], response)
        else:
            # 判断输入是否为某个教室
            # 若是一个教室则返回教室信息
            response = getRoomCourseInfo(message['Content'])
            # 如果不符合以上任意规则则识别为非法输入
            if response == '':
                response = u'无法识别您的输入，请输入教室代码、文图相关词语、教室查询字符串或音乐类型等与功能相关的文字'
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)

    elif message['MsgType'] == 'event':
        # 响应用户事件
        if message['Event'] == 'subscribe':
            # 订阅事件欢迎消息
            adduser(message['FromUserName'])
            response = [{
                'Title': u'欢迎您的关注！',
                'PicUrl': URL_WELCOME_IMAGE,
                'Url': URL_HELP
            }, {
                'Title': u'点击此消息查看帮助',
                'Url': URL_HELP
            }]
            return makeNewsMessage(message['FromUserName'], message['ToUserName'], response)
        elif message['Event'] == 'unsubscribe':
            # 取消订阅事件
            deluser(message['FromUserName'])
            response = u'谢谢您关注本产品，再见~'
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
        elif message['Event'] == 'CLICK':
            # 响应点击服务号菜单事件
            if message['EventKey'] == 'COURSE':
                # 教室排课查询
                response = u'查询某教室今天的排课情况\n您可以输入教室编号：\n“6A301”\n“4302”'
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
            elif message['EventKey'] == 'LIBRARY':
                # 文图座位查询
                articles = getLibrarySeatNews()
                return makeNewsMessage(message['FromUserName'], message['ToUserName'], articles)
            elif message['EventKey'] == 'CLASSROOM':
                # 空闲教室查询
                response = u'查询某教学楼空闲教室情况\n您可以输入关键词：\n' \
                           u'“四教”\n“六教C区”\n“三教三段2层”\n“今天第三节五教”\n“明天第二节四教三层”\n\n' \
                           u'其中教学楼名称必须指定\n目前支持一到六教'
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
            elif message['EventKey'] == 'MEAL':
                # 推荐吃饭地点
                articles = food_articles()
                return makeNewsMessage(message['FromUserName'], message['ToUserName'], articles)
            elif message['EventKey'] == 'STUDY':
                # 推荐自习室
                response = recommend_classroom()
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
            elif message['EventKey'] == 'MUSIC':
                # 推荐音乐
                articles = formMusicTypeList()
                return makeNewsMessage(message['FromUserName'], message['ToUserName'], articles)
            elif message['EventKey'] == 'SIGNIN':
                # 签到功能
                response = signin(message['FromUserName'], message['CreateTime'])
                return makeNewsMessage(message['FromUserName'], message['ToUserName'], response)
            elif message['EventKey'] == 'HELP':
                # 帮助功能
                articles = getHelpInfoArticles()
                return makeNewsMessage(message['FromUserName'], message['ToUserName'], articles)
            else:
                # 其他事件不响应
                response = u'抱歉...暂不支持响应此事件'
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
    else:
        # 其他类型的消息不支持
        response = u'暂不支持非文字消息'
        return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
