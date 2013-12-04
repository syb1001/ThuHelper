# coding=utf-8

# classroom.py
# 教室排课信息获取

from database import getclassroomsbyfloor
from utils import getClassSeqNumByDatetime
import datetime 

# 返回文字消息内容
def getClassroomInfo(queryStr):
    queryDict = getBuildFloor(queryStr)
    buildID = queryDict['buildID']
    floor = queryDict['floor']
    dt = datetime.datetime.now()
    classSeqNum = getClassSeqNumByDatetime(dt, 5)
    buildname = buildIDtoName(buildID)
    weekday = datetime.date(dt.year, dt.month, dt.day).weekday()
    
    roomList = getclassroomsbyfloor(buildID, floor, classSeqNum, weekday)
    ret =  str(dt.month) + u'月' + str(dt.day) + u'日' + u'第' + str(classSeqNum) + u'大节，\n'+ buildname + u'空闲教室：\n' 
    for room in roomList:
        ret = ret + room['roomnumber'].split()[0] + '\n'
    ret = ret.rstrip('\n')
    return ret

def getBuildFloor(queryStr):
    t = tuple(queryStr.strip('#').split(','))
    return {
    'buildID': t[0],
    'floor':   t[1],
    }

def buildIDtoName(id):
    buildDict = {
    '1': u'一教',
    '2': u'二教',
    '31':u'三教一段',
    '32':u'三教二段',
    '33':u'三教三段',   
    '4': u'四教',
    '5': u'五教',
    '6A':u'六教A区',
    '6B':u'六教B区',
    '6C':u'六教C区',
    }
    return buildDict[id]