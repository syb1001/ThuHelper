# coding=utf-8

# message.py
# 消息的生成与发送

from django.template.loader import get_template
from django.template import Context
import time

# 文字消息
def makeTextMessage(toUser, fromUser, content):
    template = get_template('xml_text.xml')
    context = Context({
        'ToUserName': toUser,
        'FromUserName': fromUser,
        'CreateTime': str(int(time.time())),
        'Content': content
    })
    return template.render(context)

# 图片消息
def makeImageMessage(toUser, fromUser, mediaId):
    template = get_template('xml_image.xml')
    context = Context({
        'ToUserName': toUser,
        'FromUserName': fromUser,
        'CreateTime': str(int(time.time())),
        'MediaId': mediaId
    })
    return template.render(context)

# 语音消息
def makeVoiceMessage(toUser, fromUser, mediaId):
    template = get_template('xml_voice.xml')
    context = Context({
        'ToUserName': toUser,
        'FromUserName': fromUser,
        'CreateTime': str(int(time.time())),
        'MediaId': mediaId
    })
    return template.render(context)

# 视频消息
def makeVideoMessage(toUser, fromUser, mediaId, title, description):
    template = get_template('xml_voice.xml')
    context = Context({
        'ToUserName': toUser,
        'FromUserName': fromUser,
        'CreateTime': str(int(time.time())),
        'MediaId': mediaId,
        'Title': title,
        'Description': description
    })
    return template.render(context)

# 音乐消息
def makeMusicMessage(toUser, fromUser, music):
    template = get_template('xml_music.xml')
    context = Context({
        'ToUserName': toUser,
        'FromUserName': fromUser,
        'CreateTime': str(int(time.time())),
        'MusicUrl': music['Url'],
        'HQMusicUrl': music['HQUrl'],
        'Title': music['Title'],
        'Description': music['Description']
    })
    return template.render(context)

# 图文消息
def makeNewsMessage(toUser, fromUser, articles):
    template = get_template('xml_news.xml')
    context = Context({
        'ToUserName': toUser,
        'FromUserName': fromUser,
        'CreateTime': str(int(time.time())),
        'ArticleCount': len(articles),
        'Articles': articles
    })
    return template.render(context)
