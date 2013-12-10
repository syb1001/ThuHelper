# coding=utf-8

# music.py
# 返回一个随机的音乐
from database import getonemusic

def getRandomMusic():
    randommusic = getonemusic()
    return {
        'Title': randommusic.title,
        'Description': randommusic.singer,
        'Url': randommusic.LQURL,
        'HQUrl':randommusic.HQURL,
    }

def musicTest():
    return [{
        'Title': u'人文社科图书馆座位使用情况',
        'Url': 'http://thuhelper11.duapp.com/musicplay/'
    }]
