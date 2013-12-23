# coding=utf-8

# music.py
# 返回一个随机的音乐

import random
from urllib import quote, urlopen
from xml.etree import ElementTree
from database import getOneMusicByType
from .settings import URL_PLAYER_PREF,\
    URL_MUSIC_IMAGE_PREF as IMAGE_PREF, URL_MUSIC_IMAGE_SUF as IMAGE_SUF, MAX_MUSIC_IMAGE_INDEX as MAX_INDEX, \
    URL_MUSIC_NOTE_IMAGE_PREF, MAX_MUSIC_NOTE_IMAGE_INDEX, URL_MUSIC_GIFT_IMAGE_PREF, MAX_MUSIC_GIFT_IMAGE_INDEX
from .settings import EXPRESSION_LIST

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
    tree = ElementTree.fromstring(xml)
    if tree.find('count').text == '0':
        # 未找到这首音乐的有效资源
        music['Url'] = ''
        music['HQUrl'] = ''
        music['ImageUrl'] = ''
        return music
    else:
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
    notes = [1, 2, 3]
    random.shuffle(notes)
    for i in range(1, 4):
        # 先从每个维度上随机取出1个类型
        keys = random.sample(music_type['type' + str(i)], 1)
        for j in range(1, 2):
            # 根据每个类型构造相应图文消息
            ele = {
                'Title': music_type['type' + str(i)][keys[j-1]],
                'Url': URL_PLAYER_PREF + '?type=' + str(i) + '&class=' + keys[j-1],
                'PicUrl': URL_MUSIC_NOTE_IMAGE_PREF + str(notes[i-1])
                          + '/music' + str(random.randint(1, MAX_MUSIC_NOTE_IMAGE_INDEX[str(notes[i-1])])) + '.jpg'
            }
            list.append(ele)
    random.shuffle(list)
    list.insert(0, {
        'Title': u'点击音乐分类 随机欣赏音乐',
        'PicUrl': IMAGE_PREF + str(random.randint(1, MAX_INDEX)) + IMAGE_SUF,
        'Url': URL_PLAYER_PREF
    })
    list.append({
        'Title': u'随便听听',
        'PicUrl': URL_MUSIC_GIFT_IMAGE_PREF + str(random.randint(1, MAX_MUSIC_GIFT_IMAGE_INDEX)) + '.jpg',
        'Url': URL_PLAYER_PREF
    })
    return list

# 由表情得到音乐
def getMusicByExpression(expression):
    flag = 0
    music = None
    type = ''
    for type in EXPRESSION_LIST:
        for expre in EXPRESSION_LIST[type]:
            if expression.startswith(expre):
                dict = {
                    'type2' : type
                }
                music = getRandomMusicByType(dict)
                flag = 1
                break
        if (flag == 1):
            break
    if (flag == 1):
        if (music['Url'] == ''):
            message = u'抱歉，未找到' + music_type['type1'][type] + u'类型的音乐，换个表情试试吧~'
            return message
        else:
            return music
    else:
        return expression

# 预定义音乐类型
music_type = {
    'type1': {
        'a': u'古典', 'b': u'流行', 'c': u'摇滚', 'd': u'乡村', 'e': u'蓝调', 'f': u'纯音乐'
    },
    'type2': {
        'a': u'欢快', 'b': u'平静', 'c': u'忧伤', 'd': u'激烈', 'e': u'小清新', 'f': u'怀旧'
    },
    'type3': {
        'a': u'中文', 'b': u'英文', 'c': u'电影配乐', 'd': u'钢琴', 'e': u'轻音乐'
    }
}

def isTypeOfMusic(str):
    if str in music_type_list:
        return True
    else:
        return False

# 音乐类型列表
music_type_list = [
    u'音乐',
    u'古典', u'流行', u'摇滚', u'乡村', u'蓝调', u'纯音乐',
    u'欢快', u'平静', u'忧伤', u'激烈', u'小清新', u'怀旧',
    u'中文', u'英文', u'电影配乐', u'钢琴', u'轻音乐'
]

# 根据类型字符串得到用于查询数据库的字典
def getTypeDict(str):
    # 遍历music_type而不是music_type_list
    for type in music_type:
        for key in music_type[type]:
            if music_type[type][key] == str:
                return {
                    type: key
                }
    # 查询“音乐”时回空字典
    return {}
