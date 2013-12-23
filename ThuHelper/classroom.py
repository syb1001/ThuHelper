# coding=utf-8

# classroom.py
# 教室排课信息获取

from database import getclassroomsbyfloor, getcoursebyroom
from utils import getClassSeqNumByDatetime
import datetime

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

    '1':   1,
    '2':   2,
    '3':   3,
    '4':   4,
    '5':   5,
    '6':   6,
    '7':   7,
    '8':   8,
    '9':   9,
    '0':   0,
}

cn_delta = {
    u'前': -2,
    u'昨': -1,
    u'今': 0,
    u'明': 1,
    u'后': 2,
    u'大后': 3,
}

building_storey = {
    '1':  (1, 2),
    '2':  (1, 2),
    '31': (1, 2, 3),
    '32': (1, 3),
    '33': (1, 2, 3, 4),
    '4':  (1, 2, 3, 4),
    '5':  (1, 2, 3),
    '6A': (0, 1, 2, 3, 4),
    '6B': (1, 2, 3, 4),
    '6C': (1, 2, 3),
}

# 返回文字消息内容; queryStr := '@ID floor time day_delta'
def getClassroomInfo_time_day(queryStr):
    queryDict = getBuildFloorTimeDaydelta(queryStr)
    if int(queryDict['floor']) not in building_storey[queryDict['buildID']]:
        return buildIDtoName(queryDict['buildID']) + u'没有' + queryDict['floor'] + u'层，只有' \
               + ''.join(map(lambda x: str(x)+u'、', building_storey[queryDict['buildID']])).rstrip(u'、') \
               + u'层'

    dt = datetime.datetime.now()
    weekday = datetime.date(dt.year, dt.month, dt.day).weekday()
    weekday += int(queryDict['delta'])
    if weekday not in range(7):
        return u'现在只能得到本周的教室排课信息'
    dt += datetime.timedelta(days=int(queryDict['delta']))
    roomList = getclassroomsbyfloor(queryDict['buildID'], queryDict['floor'], int(queryDict['time']), weekday)
    buildname = buildIDtoName(queryDict['buildID'])
    ret = buildname + queryDict['floor'] + u'层空闲教室：\n'
    if roomList == []:
        ret += u'无'
    else:
        for room in roomList:
            ret = ret + room['roomnumber'].split()[0] + '\n'
    ret = ret.rstrip('\n')
    return ret

# 返回文字消息内容; query 是中文
def classroom(query):
    query = query.decode('UTF-8')
    if not valid_query(query):
        return u"您的输入似乎不太对哦~\n举个栗子：您可以输入“今天第二节四教二层”、“六教”等关键词查询所有没课的教室。"
    query_dict = query_to_dict(query)
    dt = datetime.datetime.now()
    ret = str(dt.month) + u'月' + str(dt.day + int(query_dict['day_delta'])) + u'日' + u'第' + query_dict['class_sequence'] + u'大节\n'
    if query_dict['storey'] != '-':
        if query_dict['building_id'] in building_storey:
            if int(query_dict['storey']) not in building_storey[query_dict['building_id']]:
                ret = ''
    if query_dict['class_sequence'] not in ('1', '2', '3', '4', '5', '6'):
        return u'一天只有6大节课'
    if query_dict['building_id'] == '6ABC':
        for section in ('A', 'B', 'C'):
            query_dict['building_id'] = '6' + section
            if query_dict['storey'] == '-':
                storeys = building_storey[query_dict['building_id']]
                for i in storeys:
                    query_dict['storey'] = str(i)
                    ret += getClassroomInfo_time_day(toQueryStr(query_dict))
                    ret += '\n'
                query_dict['storey'] = '-'
            else:
                ret += getClassroomInfo_time_day(toQueryStr(query_dict))
                ret += '\n'

    elif query_dict['building_id'] == '3123':
        for section in ('1', '2', '3'):
            query_dict['building_id'] = '3' + section
            if query_dict['storey'] == '-':
                storeys = building_storey[query_dict['building_id']]
                for i in storeys:
                    query_dict['storey'] = str(i)
                    ret += getClassroomInfo_time_day(toQueryStr(query_dict))
                    ret += '\n'
                query_dict['storey'] = '-'
            else:
                ret += getClassroomInfo_time_day(toQueryStr(query_dict))
                ret += '\n'
    else:
        if query_dict['storey'] == '-':
            storeys = building_storey[query_dict['building_id']]
            for i in storeys:
                query_dict['storey'] = str(i)
                ret += getClassroomInfo_time_day(toQueryStr(query_dict))
                ret += '\n'
            query_dict['storey'] = '-'
        else:
            ret += getClassroomInfo_time_day(toQueryStr(query_dict))
    ret = ret.rstrip('\n')
    return ret

def getBuildFloorTimeDaydelta(queryStr):
    t = tuple(queryStr.strip('@').split(' '))
    return {
        'buildID': t[0],
        'floor': t[1],
        'time': t[2],
        'delta': t[3],
    }

def valid_query(query):
    flag = False
    if u'教' in query:
        if query[query.index(u'教') - 1] in cn_num:
            flag = True
        else:
            return False
    if u'层' in query:
        if query[query.index(u'层') - 1] in cn_num:
            flag = True
        else:
            return False
    if u'节' in query:
        if query[query.index(u'节') - 1] in cn_num:
            flag = True
        else:
            return False
    if u'天' in query:
        if query[query.index(u'天') - 1] in cn_delta:
            flag = True
        else:
            return False
    return flag

# 返回一个字典，其中各项的值均为字符串
def query_to_dict(query):
    if u'教' in query:
        building_id = toNum(query[query.index(u'教')-1])
    else:
        building_id = 1

    if u'节' in query:
        class_sequence = toNum(query[query.index(u'节')-1])
    else:
        dt = datetime.datetime.now()
        class_sequence = getClassSeqNumByDatetime(dt, 5)

    if u'层' in query:
        storey = str(toNum(query[query.index(u'层')-1]))
    else:
        storey = '-'

    if u'天' in query:
        if query[query.index(u'天')-1] == u'后' and query[query.index(u'天')-2] == u'大':
            day_delta = to_delta(u'大后')
        else:
            day_delta = to_delta(query[query.index(u'天')-1])
    else:
        day_delta = 0

    section = ''
    if building_id == 6:
        if u'区' in query:
            section = query[query.index(u'区')-1].upper()
        else:
            section = 'ABC'
    elif building_id == 3:
        if u'段' in query:
            section = str(toNum(query[query.index(u'段')-1]))
        else:
            section = '123'
    building_id = str(building_id) + section
    return {
        'day_delta':   str(day_delta),
        'class_sequence':     str(class_sequence),
        'building_id': building_id,
        'storey':   storey,
    }

def toQueryStr(dic):
    return '@' + dic['building_id'] + ' ' + dic['storey'] \
           + ' ' + dic['class_sequence'] + ' ' + dic['day_delta']

def to_delta(word):
    cn_delta = {
        u'前': -2,
        u'昨': -1,
        u'今': 0,
        u'明': 1,
        u'后': 2,
        u'大后': 3,
    }
    return cn_delta[word]

def toNum(word):
    if isinstance(word, int):
        return word
    if word in cn_num:
        return cn_num[word]
    else:
        return word

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
    room = room.upper()
    result = getcoursebyroom(room)
    if len(result) != 0:
        return room + formCourseText(result)
    else:
        return room

# 根据六位的01字符序列生成教室占用情况
def formCourseText(sequence):
    text = u'教室今日安排：\n'
    i = 0
    for bit in sequence:
        i += 1
        text += u'第' + str(i) + u'大节'
        if bit == '0':
            text += u'空闲\n'
        else:
            text += u'有课\n'
    return text.rstrip('\n')