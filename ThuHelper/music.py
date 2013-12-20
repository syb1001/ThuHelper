# coding=utf-8

# music.py
# 返回一个随机的音乐

import random
from urllib import quote, urlopen
from database import getOneMusicByType
from .settings import URL_MUSIC_IMAGE, URL_PLAYER_PREF

# 从数据库获取随机音乐
# 返回一个music对象用于生成音乐消息
def getRandomMusicByType(dict):
    # 从数据库中获取随机的音乐
    # 返回的数据包含title和singer字段
    music = getOneMusicByType(dict)

    # 数据库返回空
    if music == None:
        return {
            'Title': '',
            'Singer': '',
            'Description': '',
            'Url': '',
            'HQUrl': '',
            'ImageUrl': ''
        }

    # 使用百度音乐搜索接口
    # 得到xml搜索结果
    url = 'http://box.zhangmen.baidu.com/x?op=12&count=1&title=' + quote(music['Title'].encode('utf-8')) + '$$' + quote(music['Singer'].encode('utf-8')) + '$$$$'
    xml = urlopen(url).read().replace('gb2312', 'utf-8')

    # 解析xml得到搜索结果中第一条音乐的url
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(xml)
    pref_path = tree.getiterator('encode')[0].text
    xcode = tree.getiterator('decode')[0].text
    music_url = pref_path[0: pref_path.rfind('/') + 1] + xcode

    # 增加url字段
    music['Url'] = music_url
    music['HQUrl'] = music_url

    return music

# 生成音乐列表
# 用来返回图文消息
def formMusicTypeList():
    list = []
    for i in range(1, 4):
        # 先从每个维度上随机取出1个类型
        keys = random.sample(music_type['type' + str(i)], 1)
        for j in range(1, 2):
            # 根据每个类型构造相应图文消息
            ele = {
                'Title': music_type['type' + str(i)][keys[j-1]],
                'Url': URL_PLAYER_PREF + '?type=' + str(i) + '&class=' + keys[j-1]
            }
            list.append(ele)
    random.shuffle(list)
    list.insert(0, {
        'Title': u'热门音乐分类-点击播放',
        'PicUrl': URL_MUSIC_IMAGE,
        'Url': URL_PLAYER_PREF
    })
    list.append({
        'Title': u'随便听听',
        'Url': URL_PLAYER_PREF
    })
    return list

# 预定义音乐类型
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
        'd': u'钢琴',
        'e': u'轻音乐'
    }
}