#coding=utf-8
#from bae.core import const
from ThuHelper.models import *
import MySQLdb
import datetime
from django.http import HttpResponse
from ThuHelper.settings import DATABASE_NAME
import pickle
import random
def dbtest(request):
    """
    mydb = MySQLdb.connect(
        host = const.MYSQL_HOST,
        port = int(const.MYSQL_PORT),
        user = const.MYSQL_USER,
        passwd = const.MYSQL_PASS,
        db = DATABASE_NAME,
    )
    cursor = mydb.cursor()
    cursor.execute('Select * from classroom')
    classrooms = [row[1] for row in cursor.fetchall()]
    for room in classrooms:
        print(room)
    mydb.close()
    """
    idleclassroom = getcoursebyroom('1101')
    return HttpResponse(idleclassroom)

def dbinit(request):
    roomfile = open('ThuHelper/data.pickle', 'rb')
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


def getclassroomsbyfloor(building, floor, time, weekday):
    classroomlist = classroom.objects.filter(building=building, floor=floor)
    result = []
    for row in classroomlist:
        isusable = isroomusable(row, time, weekday)
        if (isusable == '0'):
            roomdata = {}
            roomdata['roomnumber'] = row.roomnumber
            result.append(roomdata)
    return result

def getcoursebyroom(room):
    classroomlist = classroom.objects.filter(roomnumber__contains=room)
    if (len(classroomlist) == 0):
        return classroomlist
    else:
        return getcourse(classroomlist[0])


#def getclassroomsbyroom(room):


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
    p = classroom(building=building, floor=floornum, roomnumber=roomnumber, Monday=status[0:6], Tuesday=status[6:12], Wednesday=status[12:18], Thursday=status[18:24], Friday=status[24:30], Saturday=status[30:36], Sunday=status[36:42])
    p.save()






def getonemusic():
    musiclist = onlinemusic.objects.all()
    return musiclist[random.randint(0, len(musiclist) - 1)]