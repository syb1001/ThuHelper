# coding=utf-8

# signin.py
# 处理用户签到事件

import time
from database import getLastTimebyID, getRecentInfobyID, changeLastTime, changeRecentInfo, addsignintime, getsignintimebyID
from .settings import URL_SIGNIN_IMAGE

#两个参数都是字符串
def signin(openID, now):

    info = getRecentInfobyID(openID)
    lasttime = getLastTimebyID(openID)
    if(not lasttime):
        # 没上过自习,首次签到
        addsignintime(openID)
        changeRecentInfo(openID, '000000000000000000000000000001')
        changeLastTime(openID, now)
        return [
            {
                'Title': u'签到信息',
                'PicUrl': URL_SIGNIN_IMAGE
            }, {
                'Title':u'这是您第一次签到，欢迎继续使用'
            }
        ]
    else:
        numofday = int((float(now) - lasttime)/(24*3600))+1
        timeforcheck = lasttime + numofday*24*3600
        x = time.localtime(timeforcheck)
        y = time.localtime(float(now))
        a= time.strftime('%Y-%m-%d %H:%M:%S', x)
        b = time.strftime('%Y-%m-%d %H:%M:%S', y)
        if(not a[9] == b[9]):
            numofday -= 1
        if numofday == 0:
            # 今日已签过到
            return u"您今天已经签过到了，感谢您的支持！"
        if(numofday >= 30):
            # 超过三十天没自习
            addsignintime(openID)
            changeRecentInfo(openID, '000000000000000000000000000001')
            changeLastTime(openID, now)
            myobject = {}
            myobject["all"] = getsignintimebyID(openID)
            myobject["month"] = 1
            return [
                {
                    'Title': u'签到信息',
                    'PicUrl': URL_SIGNIN_IMAGE
                }, {
                    'Title': u'您总共上自习次数'+str(myobject['all'])+u'\n您本月自习次数'+str(myobject['month'])
                }
            ]
        else:
            #统计一个月内上自习的次数
            addsignintime(openID)
            count = 0
            #newinfo = '000000000000000000000000000001'
            for i in range(numofday, 29):
                #newinfo[i - numofday] = info[i]
                if info[i] == '1':
                    count += 1
            newinfo = info[numofday:30]
            for i in range(30-numofday, 29):
                newinfo += '0'
            newinfo += '1'
            changeRecentInfo(openID, newinfo)
            changeLastTime(openID, now)
            myobject = {}
            myobject["all"] = getsignintimebyID(openID)
            myobject["month"] = count + 1
            return [
                {
                    'Title': u'签到信息',
                    'PicUrl': URL_SIGNIN_IMAGE
                }, {
                    'Title': u'您总共上自习次数'+str(myobject['all'])+u'\n您本月自习次数'+str(myobject['month'])
                }
            ]



