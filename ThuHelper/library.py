# coding=utf-8

# library.py
# 人文图书馆座位信息获取
# 人文古树管空闲座位数量获取

from BeautifulSoup import BeautifulSoup
import urllib, random
from .settings import URL_LIBRARY, URL_LIBRARY_IMAGE_PREF, MAX_LIBRARY_IMAGE_INDEX

# 生成图文信息
def getLibrarySeatNews():
    info = u'人文馆当前共有空闲座位' + str(getLibrarySeatNum()) + u'个'
    return [{
        'Title': u'人文社科图书馆座位使用情况',
        'PicUrl': URL_LIBRARY_IMAGE_PREF + str(random.randint(1, MAX_LIBRARY_IMAGE_INDEX)) + '.jpg',
        'Url': URL_LIBRARY
    }, {
        'Title': info,
        'Url': URL_LIBRARY
    }]

# 获取座位信息
# 返回图书馆剩余座位数
def getLibrarySeatNum():
    info = getLibrarySeatInfo()
    num = 0
    for element in info:
        num += int(element['leftNum'])
    return num

# 获取座位信息
# 以字典数组形式返回
def getLibrarySeatInfo():
    url = 'http://seat.lib.tsinghua.edu.cn/roomshow/'
    page = urllib.urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html)
    tds = soup.findAll('td', style='font-size:20.0pt')

    i = 0
    info = []
    for td in tds:
        i += 1
        if i % 3 == 1:
            element = {}
            element['floor'] = td.string
        elif i % 3 == 2:
            element['takenNum'] = td.string
        else:
            element['leftNum'] = td.string
            info.append(element)
    return info

# 获取座位信息
# 并将座位信息转成文字消息
def getLibrarySeatText():
    array = getLibrarySeatInfo()
    text = ''
    for element in array:
        text += element['floor']
        text += u'：'
        text += '\n'
        text += u'已用座位'
        text += element['takenNum']
        text += u'，'
        text += u'剩余座位'
        text += element['leftNum']
        text += '\n'
    return text.rstrip('\n')
