# coding=utf-8

# music.py
# 返回一个随机的音乐
from database import getonemusic

def getRandomMusic():
    randommusic = getonemusic()
    return {
        'Title': randommusic.title,
        'Description': randommusic.description,
        'Url': randommusic.LQURL,
        'HQUrl':randommusic.HQURL,
    }