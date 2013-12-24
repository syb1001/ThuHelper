# coding=utf-8

# recommend_classroom.py
# 推荐教室

from database import getclassroomsbyfloor
from utils import getClassSeqNumByDatetime
import datetime
import random

# 推荐教室备选教学楼编号
buildings = [
    '1',
    '31',
    '33',
    '4',
    '5',
    '6A',
    '6B',
    '6C',
]

buildings_weight = {
    '1': 5,
    '31': 23,
    '32': 0,
    '33': 20,
    '4': 20,
    '5': 20,
    '6A': 25,
    '6B': 25,
    '6C': 0,
}

code_building = {
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

# 返回文字消息内容, 推荐教室
def recommend_classroom():
    dt = datetime.datetime.now()
    class_seq = getClassSeqNumByDatetime(dt, 10)
    rooms = get_rooms(3, 10)
    if dt.minute < 10 and dt.minute != 0:
        minute_str = '0' + str(dt.minute)
    else:
        minute_str = str(dt.minute)
    time_string = str(dt.hour) + u'点' + minute_str + u'分'
    ret = u'现在是' + time_string + u'\n'
    ret += code_building[rooms['building']] \
           + str(rooms['floor']) + u'层\n第' + str(class_seq) + u'节课空闲教室较多\n'
    for i in range(3):
        ret += rooms['list'][i]['roomnumber'].split()[0] + '\n'
    ret += u'都是不错的选择^_^'
    return ret

def get_building():
    total = 0
    for key in buildings_weight:
        total += buildings_weight[key]
    num = random.randint(1, total)

    ret = ''
    building_list = sorted(buildings_weight)
    for building in building_list:
        if num - buildings_weight[building] <= 0:
            ret = building
            break
        else:
            num -= buildings_weight[building]
    return ret

def get_storey(building):
    storeys = building_storey[building]
    index = random.randint(0, len(storeys) - 1)
    return storeys[index]

def get_rooms(least_num, minute_delta):
    room_list = []
    building = ''
    storey = 0
    dt = datetime.datetime.now()
    class_seq = getClassSeqNumByDatetime(dt, minute_delta)
    weekday = datetime.date(dt.year, dt.month, dt.day).weekday()
    while len(room_list) < least_num:
        building = get_building()
        storey = get_storey(building)
        room_list = getclassroomsbyfloor(building, storey, class_seq, weekday)
    return {
        'list': room_list,
        'building': building,
        'floor': storey,
    }

# least_num 是最少的空闲教室数量
def get_rooms2(least_num, minute_delta):
    dt = datetime.datetime.now()
    class_seq = getClassSeqNumByDatetime(dt, minute_delta)
    weekday = datetime.date(dt.year, dt.month, dt.day).weekday()
    building_index = 0
    floors = []
    floor_index = 0
    room_list = []
    while len(room_list) < least_num:
        building_index = random.randint(0, len(buildings) - 1)
        floors = building_storey[buildings[building_index]]
        floor_index = random.randint(0, len(floors) - 1)
        room_list = getclassroomsbyfloor(buildings[building_index], floors[floor_index], class_seq, weekday)
    return {
        'list': room_list,
        'building': buildings[building_index],
        'floor': floors[floor_index]
    }