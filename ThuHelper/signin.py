# coding=utf-8

# signin.py
# 处理用户签到事件
import time
from database import getLastTimebyID, getRecentInfobyID, changeLastTime, changeRecentInfo
#两个参数都是字符串
def signin(openID, now):
    info = getRecentInfobyID(openID)
    lasttime = getLastTimebyID(openID)
    if(not lasttime):       #没上过自习,首次签到
        changeRecentInfo(openID, '000000000000000000000000000001')
        changeLastTime(openID, now)
        return 0    #没上过自习
    else:
        numofday = int((float(now) - lasttime)/(24*3600))+1
        timeforcheck = lasttime + numofday*24*3600
        x = time.localtime(timeforcheck)
        y = time.localtime(float(now))
        a= time.strftime('%Y-%m-%d %H:%M:%S', x)
        b = time.strftime('%Y-%m-%d %H:%M:%S', y)
        if( not a[9] == b[9]):
            numofday -= 1
        if numofday == 0:
            return -1
        #超过三十天没自习
        if(numofday >= 30):
            changeRecentInfo(openID, '000000000000000000000000000001')
            changeLastTime(openID, now)
            #超过三十天没自习
            return 1
        else:
            #统计一个月内上自习的次数
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
            return count+1



