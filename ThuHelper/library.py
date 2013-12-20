# coding=utf-8

# library.py
# 人文图书馆座位信息获取
# 人文古树管空闲座位数量获取

from BeautifulSoup import BeautifulSoup
import urllib, random
from .settings import URL_LIBRARY, URL_LIBRARY_IMAGE_PREF, MAX_LIBRARY_IMAGE_INDEX

# 检查一个字符串中是否含有关于人文馆的关键词
def isConsultingLibrary(str):
    names = [u'文图', u'人文馆', u'文科馆', u'人文社科图书馆', u'人文图书馆', u'凯风']
    for name in names:
        if name in str:
            return True
    return False

# 生成图文信息
def getLibrarySeatNews():
    nums = getLibrarySeatNum()
    info1 = u'人文馆当前共有空闲座位' + str(nums[0]) + u'个'
    info2 = u'G层自修室' + str(nums[1]) + u'个\n其他区域' + str(nums[2]) + u'个'
    return [{
        'Title': u'人文社科图书馆座位使用情况',
        'PicUrl': URL_LIBRARY_IMAGE_PREF + str(random.randint(1, MAX_LIBRARY_IMAGE_INDEX)) + '.jpg',
        'Url': URL_LIBRARY
    }, {
        'Title': info1,
        'Url': URL_LIBRARY
    }, {
        'Title': info2,
        'Url': URL_LIBRARY
    }, {
        'Title': u'点此消息查看详细信息',
        'Url': URL_LIBRARY
    }]

# 获取座位信息
# 返回图书馆剩余座位数
def getLibrarySeatNum():
    info = getLibrarySeatInfo()
    num = 0
    for element in info:
        num += int(element['leftNum'])
    return (num, int(info[0]['leftNum']), num - int(info[0]['leftNum']))

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
