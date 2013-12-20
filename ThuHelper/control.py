# coding=utf-8

# control.py
# 消息处理的逻辑
# 判断用户发送消息的用途
# 返回用户不同类型不同内容的消息

from settings import EXPRESSION_LIST
from database import adduser
from message import *
from library import getLibrarySeatText, getLibrarySeatNews, isConsultingLibrary
from helpInfo import getHelpInfoArticles
from music import getRandomMusicByType, formMusicTypeList
from classroom import getClassroomInfo, getRoomCourseInfo, getClassroomInfo_time, getClassroomInfo_time_day, classroom
from food import get_food
from recommend_classroom import recommend_classroom

def processMessage(message):
    if message['MsgType'] == 'text':
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
        elif message['Content'].startswith('#'):
            # 查询教室排课信息, 简易版本
            response = getClassroomInfo(message['Content'])
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
        elif message['Content'].startswith('$'):
            # 查询教室排课信息, 加入时间参数
            response = getClassroomInfo_time(message['Content'])
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
        elif message['Content'].startswith('@'):
            # 查询教室排课信息, 加入日期偏移参数
            response = getClassroomInfo_time_day(message['Content'])
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
        elif message['Content'].startswith('/:'):
            flag = 0;
            for type in EXPRESSION_LIST:
                for expression in EXPRESSION_LIST[type]:
                    if (expression == message['Content']):
                        flag = 1;
                        break;


        elif u'教' in message['Content']:
            # 查询教室排课信息, 处理的是文字输入
            response = classroom(message['Content'])
            return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
        elif u'音乐' in message['Content']:
            # 随机播放一首音乐
            music = getRandomMusicByType({})
            if music['Title'] == '':
                return makeTextMessage(message['FromUserName'], message['ToUserName'], '抱歉，未找到该类型的音乐')
            else:
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
        # 响应用户事件
        if message['Event'] == 'subscribe':
            # 响应订阅事件
            # 订阅号欢迎消息
            #response = u'欢迎关注清华自习小助手，请发送“帮助”或“help”查看帮助信息~'
            # 服务号欢迎消息
            adduser(message['FromUserName'])
            response = u'欢迎关注清华自习小助手，请使用帮助菜单查看帮助信息~也可回复“帮助”或“help”哦~'
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
                           u'“四教”\n“六教C区”\n“三教三段2层”\n“今天第三节五教”\n“明天第二节四教三层”\n(其中教学楼名称必须指定)'
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
            elif message['EventKey'] == 'MEAL':
                # 推荐吃饭地点
                response = get_food()
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
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
                response = u'功能还没实现，敬请期待~'
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
            elif message['EventKey'] == 'HELP':
                # 帮助功能
                articles = getHelpInfoArticles()
                return makeNewsMessage(message['FromUserName'], message['ToUserName'], articles)
            elif message['EventKey'] == 'ABOUT':
                # 开发者信息
                response = u'机智的程序猿小组'
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
            else:
                # 其他事件不响应
                response = u'抱歉...暂不支持响应此事件'
                return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
    else:
        # 其他类型的消息不支持
        response = u'暂不支持非文字消息'
        return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
