# coding=utf-8

# music.py
# 返回一个随机的音乐
import random
from database import getonemusic
from .settings import URL_MUSIC_IMAGE, URL_PLAYER

music_type = {
    'type1': {
        'a': u'古典',
        'b': u'流行',
        'c': u'摇滚',
        'd': u'乡村',
        'e': u'蓝调',
        'f': u'纯音乐'
    },
    'type2': {
        'a': u'欢快',
        'b': u'平静',
        'c': u'忧伤',
        'd': u'激烈',
        'e': u'小清新',
        'f': u'怀旧'
    },
    'type3': {
        'a': u'中文',
        'b': u'英文',
        'c': u'电影配乐',
        'd': u'交响',
        'e': u'轻音乐'
    }
}

def getRandomMusic():
    randommusic = getonemusic()
    return {
        'Title': randommusic.title,
        'Description': randommusic.singer,
        'Url': randommusic.LQURL,
        'HQUrl':randommusic.HQURL,
    }

def formMusicTypeList():
    list = [{
        'Title': u'热门音乐分类',
        'PicUrl': URL_MUSIC_IMAGE
    }]

    for i in range(1, 4):
        # 先从每个维度上随机取出3个类型
        keys = random.sample(music_type['type' + str(i)], 3)
        for j in range(1, 4):
            # 根据每个类型构造相应图文消息
            ele = {
                'Title': music_type['type' + str(i)][keys[j-1]],
                'Url': URL_PLAYER + 'type=' + str(j) + '&class=' + keys[j-1]
            }
            list.append(ele)
    return list
