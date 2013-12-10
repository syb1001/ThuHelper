#coding=utf-8
#from bae.core import const
from ThuHelper.models import *
import MySQLdb
import datetime
from django.http import HttpResponse
from ThuHelper.settings import DATABASE_NAME
import pickle
import random

def dbinit(request):
    roomfile = open('ThuHelper/data.pkl', 'r')
    classroomlist = pickle.load(roomfile)
    roomfile.close()
    for room in classroomlist:
        insertclassroom(room['building'], room['name'][0], room['status'])
    return HttpResponse()

def isroomusable(data, time, weekday):
    nowweek = weekday + 1
    time = time - 1
    if (nowweek == 1):
        return data.Monday[time]
    elif (nowweek == 2):
        return data.Tuesday[time]
    elif (nowweek == 3):
        return data.Wednesday[time]
    elif (nowweek == 4):
        return data.Thursday[time]
    elif (nowweek == 5):
        return data.Friday[time]
    elif (nowweek == 6):
        return data.Saturday[time]
    elif (nowweek == 7):
        return data.Sunday[time]

def getcourse(data):
    nowweek = datetime.datetime.now().weekday() + 1
    if (nowweek == 1):
        return data.Monday
    elif (nowweek == 2):
        return data.Tuesday
    elif (nowweek == 3):
        return data.Wednesday
    elif (nowweek == 4):
        return data.Thursday
    elif (nowweek == 5):
        return data.Friday
    elif (nowweek == 6):
        return data.Saturday
    elif (nowweek == 7):
        return data.Sunday

# building, floor 是字符串; time, weekday 是数字
def getclassroomsbyfloor(building, floor, time, weekday):
    classroomlist = Classroom.objects.filter(building=building, floor=floor)
    result = []
    for row in classroomlist:
        isusable = isroomusable(row, time, weekday)
        if (isusable == '0'):
            roomdata = {}
            roomdata['roomnumber'] = row.roomnumber
            result.append(roomdata)
    return result

def getcoursebyroom(room):
    classroomlist = Classroom.objects.filter(roomnumber__contains=room)
    if (len(classroomlist) == 0):
        return classroomlist
    else:
        return getcourse(classroomlist[0])

def insertclassroom(building, roomnumber, status):
    #roomnumber = roomnumber.decode('unicode_escape')
    if (building == '1') or (building == '2'):
        floornum = int(roomnumber[0])
    elif (building[0] == '3') or (building == '4') or (building == '5'):
        floornum = int(roomnumber[1])
    elif (building[0] == '6'):
        floornum = int(roomnumber[2])
    #if (building[0] == '3'):
       #building += roomnumber[0]
    if (building[0] == '6'):
        building += roomnumber[1]
    p = Classroom(building=building, floor=floornum, roomnumber=roomnumber, Monday=status[0:6], Tuesday=status[6:12], Wednesday=status[12:18], Thursday=status[18:24], Friday=status[24:30], Saturday=status[30:36], Sunday=status[36:42])
    p.save()

def insertonlinemusic(music):
    p = Onlinemusic(title=music['title'], singer=music['singer'], description=music['description'], LQURL=music['LQURL'], HQURL=music['HQURL'], type1=music['type1'], type2=music['type2'], type3=music['type3'])
    p.save()

def getonemusic():
    musiclist = Onlinemusic.objects.all()
    return musiclist[random.randint(0, len(musiclist) - 1)]

# 根据音乐类型随机一首歌
# 传入的词典中可能含有'type1': 'b'这样的项
# 多维搜索时可能含有更多的项
def getOneMusicByType(dict):
    musicList = Onlinemusic.objects.all()
    return musicList[random.randint(0, len(musicList) - 1)]