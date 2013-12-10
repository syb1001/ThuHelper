# coding=utf-8

# classroom.py
# 教室排课信息获取

from database import getclassroomsbyfloor, getcoursebyroom
from utils import getClassSeqNumByDatetime
import datetime 

# 返回文字消息内容 queryStr := '#ID floor'
def getClassroomInfo(queryStr):
    queryDict = getBuildFloor(queryStr)
    buildID = queryDict['buildID']
    floor = queryDict['floor']
    dt = datetime.datetime.now()
    classSeqNum = getClassSeqNumByDatetime(dt, 5)
    buildname = buildIDtoName(buildID)
    weekday = datetime.date(dt.year, dt.month, dt.day).weekday()
    
    roomList = getclassroomsbyfloor(buildID, floor, classSeqNum, weekday)
    ret = str(dt.month) + u'月' + str(dt.day) + u'日' + u'第' + str(classSeqNum) \
          + u'大节，\n' + buildname + floor + u'层空闲教室：\n'
    for room in roomList:
        ret = ret + room['roomnumber'].split()[0] + '\n'
    ret = ret.rstrip('\n')
    return ret

# 返回文字消息内容 queryStr := '$ID floor time'
def getClassroomInfo_time(queryStr):
    queryDict = getBuildFloorTime(queryStr)
    dt = datetime.datetime.now()
    weekday = datetime.date(dt.year, dt.month, dt.day).weekday()
    roomList = getclassroomsbyfloor(queryDict['buildID'], queryDict['floor'], int(queryDict['time']), weekday)
    buildname = buildIDtoName(queryDict['buildID'])
    ret = str(dt.month) + u'月' + str(dt.day) + u'日' + u'第' + queryDict['time'] \
          + u'大节，\n' + buildname + queryDict['floor'] + u'层空闲教室：\n'
    for room in roomList:
        ret = ret + room['roomnumber'].split()[0] + '\n'
    ret = ret.rstrip('\n')
    return ret

# 返回文字消息内容; queryStr := '@ID floor time day_delta'
def getClassroomInfo_time_day(queryStr):
    queryDict = getBuildFloorTimeDaydelta(queryStr)
    dt = datetime.datetime.now()
    weekday = datetime.date(dt.year, dt.month, dt.day).weekday()
    weekday += int(queryDict['delta'])
    if weekday not in range(7):
        return u'现在只能得到本周的教室排课信息'
    dt += datetime.timedelta(days=int(queryDict['delta']))
    roomList = getclassroomsbyfloor(queryDict['buildID'], queryDict['floor'], int(queryDict['time']), weekday)
    buildname = buildIDtoName(queryDict['buildID'])
    ret = str(dt.month) + u'月' + str(dt.day) + u'日' + u'第' + queryDict['time'] \
          + u'大节，\n' + buildname + queryDict['floor'] + u'层空闲教室：\n'
    for room in roomList:
        ret = ret + room['roomnumber'].split()[0] + '\n'
    ret = ret.rstrip('\n')
    return ret

# 返回文字消息内容; query 是中文
def classroom(query):
    query = query.decode('UTF-8')
    if not valid_query(query):
        return u"您的输入似乎不太对哦～\n举一个栗子：您可以输入“今天第二节四教二层”，" \
               u"来查询所有没课的教室。"
    query_dict = parseQuery(query)
    return getClassroomInfo_time_day(toQueryStr(query_dict))


def getBuildFloor(queryStr):
    t = tuple(queryStr.strip('#').split(' '))
    return {
        'buildID': t[0],
        'floor': t[1],
    }

def getBuildFloorTime(queryStr):
    t = tuple(queryStr.strip('$').split(' '))
    return {
        'buildID': t[0],
        'floor': t[1],
        'time': t[2],
    }

def getBuildFloorTimeDaydelta(queryStr):
    t = tuple(queryStr.strip('@').split(' '))
    return {
        'buildID': t[0],
        'floor': t[1],
        'time': t[2],
        'delta': t[3],
    }

def valid_query(query):
    if u'天' and u'节' and u'教' and u'层' in query:
        if query[query.index(u'天') - 1] in (u'今', u'明', u'后'):
            return True
        else:
            return False
    else:
        return False

def parseQuery(query):
    daydelta = wordtoDay(query[query.index(u'天')-1])
    seq = toNum(query[query.index(u'节')-1])
    floor = str(toNum(query[query.index(u'层')-1]))
    build = toNum(query[query.index(u'教')-1])
    section = ''
    if build == 6:
        section = query[query.index(u'区')-1]
    elif build == 3:
        section = query[query.index(u'段')-1]
    build = str(build) + section
    return {
        'delta':   str(daydelta),
        'seq':     str(seq),
        'buildID': build,
        'floor':   floor,
    }

def toQueryStr(dic):
    return '@' + dic['buildID'] + ' ' + dic['floor'] \
           + ' ' + dic['seq'] + ' ' + dic['delta']

def wordtoDay(word):
    cn_delta = {
        u'今': 0,
        u'明': 1,
        u'后': 2,
        u'大后': 3,
    }
    return cn_delta[word]

def toNum(word):
    if isinstance(word, int):
        return word
    cn_num = {
        u'〇': 0,
        u'一': 1,
        u'二': 2,
        u'三': 3,
        u'四': 4,
        u'五': 5,
        u'六': 6,
        u'七': 7,
        u'八': 8,
        u'九': 9,

        u'零': 0,
        u'壹': 1,
        u'贰': 2,
        u'叁': 3,
        u'肆': 4,
        u'伍': 5,
        u'陆': 6,
        u'柒': 7,
        u'捌': 8,
        u'玖': 9,

        u'貮': 2,
        u'两': 2,
    }
    return cn_num[word]

def nametoBuildID(name):
    d = {
        u'一教': '1',
        u'二教': '2',
        u'三教一段': '31',
        u'三教二段': '32',
        u'三教三段': '33',
        u'四教': '4',
        u'五教': '5',
        u'六教A区': '6A',
        u'六教B区': '6B',
        u'六教C区': '6C',
    }
    return d[name]

def buildIDtoName(id):
    buildDict = {
        '1': u'一教',
        '2': u'二教',
        '31': u'三教一段',
        '32': u'三教二段',
        '33': u'三教三段',
        '4': u'四教',
        '5': u'五教',
        '6A': u'六教A区',
        '6B': u'六教B区',
        '6C': u'六教C区',
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