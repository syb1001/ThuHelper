# coding=utf-8

# signin.py
# 处理用户签到事件

import time, random
from database import getLastTimebyID, getRecentInfobyID, changeLastTime, changeRecentInfo, addsignintime, getsignintimebyID, getrankbyID
from .settings import URL_SIGNIN_IMAGE

#两个参数都是字符串
def signin(openID, now):

    info = getRecentInfobyID(openID)
    lastSignTime = getLastTimebyID(openID)
    totalSignTime = getsignintimebyID(openID)

    if not lastSignTime:
        # 首次签到
        addsignintime(openID)
        changeRecentInfo(openID, '000000000000000000000000000001')
        changeLastTime(openID, now)
        dictTemp = getrankbyID(openID)
        return [{
                'Title': u'学霸是怎样炼成的',
                'PicUrl': URL_SIGNIN_IMAGE
            }, {
                'Title': u'欢迎您使用自习签到功能。\n' + getSaying() + '\n要想成为学霸，坚持签到吧~'
            }, {
                'Title': u'您这个月总共签到：1次\n总签到次数：1次\n' +
                         u'您目前排在第' + str(dictTemp['rank']) + u'名\n击败了' +
                         str(round((1 - float(dictTemp['rank'] - 1) / (dictTemp['total'] - 1)) * 100, 1)) + u'%的学霸'
            }, {
                'Title': u'学习要对自己诚实，不要故意刷数据呦~↖(^ω^)↗\n注：每天只能签到一次'
            }
        ]
    else:
        # 计算距上次自习已有多长时间
        numOfDay = int((float(now) - lastSignTime)/(24*3600))+1
        timeforcheck = lastSignTime + numOfDay*24*3600
        x = time.localtime(timeforcheck)
        y = time.localtime(float(now))
        a= time.strftime('%Y-%m-%d %H:%M:%S', x)
        b = time.strftime('%Y-%m-%d %H:%M:%S', y)
        if not a[9] == b[9]:
            numOfDay -= 1

        if numOfDay > 0:
            # 今日还没签过到
            # 增加总签到次数
            addsignintime(openID)
            totalSignTime += 1
            # 更改上一次签到时间
            changeLastTime(openID, now)
            # 得到签到排名
            dictTemp = getrankbyID(openID)
            if numOfDay >= 30:
                # 超过三十天没自习
                changeRecentInfo(openID, '000000000000000000000000000001')
                return [{
                            'Title': u'学霸是怎样炼成的',
                            'PicUrl': URL_SIGNIN_IMAGE
                        }, {
                            'Title': u'欢迎您使用自习签到功能。\n' + getSaying() + '\n要想成为学霸，坚持签到吧~'
                        }, {
                            'Title': u'您这个月总共签到：1次\n总签到次数：' + str(totalSignTime) + u'次\n' +
                                     u'您目前排在第' + str(dictTemp['rank']) + u'名\n击败了' +
                                     str(round((1 - float(dictTemp['rank'] - 1) / (dictTemp['total'] - 1)) * 100, 1)) + u'%的学霸'
                        }, {
                            'Title': u'距您上次自习好久好久了o(╯□╰)o\n这么久没有自习了，学渣要努力啊！'
                        }
                ]
            else:
                # 统计一个月内上自习的次数
                count = 0
                for i in range(numOfDay, len(info)):
                    if info[i] == '1':
                        count += 1
                count += 1
                # 更新状态串
                newInfo = info[numOfDay: len(info)]
                for i in range(30 - numOfDay, len(info) - 1):
                    newInfo += '0'
                newInfo += '1'
                changeRecentInfo(openID, newInfo)
                return [{
                            'Title': u'学霸是怎样炼成的',
                            'PicUrl': URL_SIGNIN_IMAGE
                        }, {
                            'Title': u'欢迎您使用自习签到功能。\n' + getSaying() + '\n要想成为学霸，坚持签到吧~'
                        }, {
                            'Title': u'您这个月总共签到：' + str(count) + u'次\n总签到次数：' + str(totalSignTime) + u'次\n' +
                                     u'您目前排在第' + str(dictTemp['rank']) + u'名\n击败了' +
                                     str(round((1 - float(dictTemp['rank'] - 1) / (dictTemp['total'] - 1)) * 100, 1)) + u'%的学霸'
                        }, {
                            'Title': u'据您上次自习已经过去了' + str(numOfDay) + u'天\n' + getRemark(numOfDay)
                        }
                ]
        else:
            # 今日已签过到
            # 统计一个月内上自习的次数
            count = 0
            for i in range(0, len(info)):
                if info[i] == '1':
                    count += 1
            dictTemp = getrankbyID(openID)
            return [{
                    'Title': u'学霸是怎样炼成的',
                    'PicUrl': URL_SIGNIN_IMAGE
                }, {
                    'Title': u'您这个月总共签到：' + str(count) + u'次\n总签到次数：' + str(totalSignTime) + u'次\n' +
                             u'您目前排在第' + str(dictTemp['rank']) + u'名\n击败了' +
                             str(round((1 - float(dictTemp['rank'] - 1) / (dictTemp['total'] - 1)) * 100, 1)) + u'%的学霸'
                }, {
                    'Title': u'今天您已经签过到了'
                }
            ]

# 根据距上次自习的天数得到评价
def getRemark(num):
    if num <= 3:
        return u'最近自习很勤奋嘛~继续朝着学霸的方向努力吧！'
    elif num <= 10:
        return u'常去自习有益身体健康~'
    elif num <= 20:
        return u'不多练习，技艺会生疏的哦~'
    else:
        return u'很久不去自习了嘛，不要甘当学渣啊！'

# 随机得到一句劝学名言
def getSaying():
    sentences = [
        u'冰冻三尺，非一日之寒，经常自习才能拥有知识',
        u'书山有路勤为径，学海无涯苦作舟，虽是老话，历久弥新',
        u'一寸光阴一寸金，珍惜学习的时光，收获宝贵的知识',
        u'日积月累，点滴的知识也能汇成海洋',
        u'业精于勤，荒于嬉。把握现在，才能拥有未来'
    ]
    return sentences[random.randint(0, len(sentences) - 1)]