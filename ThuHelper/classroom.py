# coding=utf-8

# classroom.py
# 教室排课信息获取

from database import getclassroomsbyfloor, getcoursebyroom
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
    ret =  str(dt.month) + u'月' + str(dt.day) + u'日' + u'第' + str(classSeqNum) + u'大节，\n'+ buildname + floor + u'层空闲教室：\n'
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

# 传入的room如果不是一个教室则原样返回
# 若是一个教室则返回该教室当天的排课信息
def getRoomCourseInfo(room):
    result = getcoursebyroom(room)
    if len(result) != 0:
        return formCourseText(result)
    else:
        return room

# 根据六位的01字符序列生成教室占用情况
def formCourseText(sequence):
    text = u'该教室今日安排：\n'
    i = 0
    for bit in sequence:
        i += 1
        text += u'第' + str(i) + u'大节'
        if bit == '0':
            text += u'无课\n'
        else:
            text += u'有课\n'
    return text.rstrip('\n')