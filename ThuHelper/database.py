# coding=utf-8

# database.py
# 数据库操作

#from bae.core import const
from ThuHelper.models import *
import MySQLdb
import datetime
from django.http import HttpResponse
from ThuHelper.settings import DATABASE_NAME
import httplib
import pickle
import random
from settings import WEIXIN_TOKEN

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
    #app = signin('asdfasdfasdf', 123123)
    #appe = app
    return HttpResponse(0)

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

# building和floor是字符串
# time和weekday是数字
# weekday的范围是0到6
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

# 获取一个教室的上课情况
def getcoursebyroom(room):
    classroomlist = Classroom.objects.filter(roomnumber__contains=room)
    if (len(classroomlist) == 0):
        return classroomlist
    else:
        return getcourse(classroomlist[0])

# 添加一个教室
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

# 修改某个教室某天的上课情况
def updateclassroombyweek(building, roomnumber, week, status):
    try:
        p = Classroom.objects.get(roomnumber=roomnumber)
    except Classroom.DoesNotExist:
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
        p = Classroom(building=building, floor=floornum, roomnumber=roomnumber)
    if (week == 1):
        p.Monday = status
    elif (week == 2):
        p.Tuesday = status
    elif (week == 3):
        p.Wednesday = status
    elif (week == 4):
        p.Thursday = status
    elif (week == 5):
        p.Friday = status
    elif (week == 6):
        p.Saturday = status
    elif (week == 7):
        p.Sunday = status
    p.save()


# 添加一首音乐
def insertonlinemusic(music):
    p = Onlinemusic(title=music['title'], singer=music['singer'], description=music['description'], imageURL=music['imageURL'], type1=music['type1'], type2=music['type2'], type3=music['type3'])
    p.save()

# 根据音乐类型随机返回music对象
# 传入的词典中可能含有'type1': 'b'这样的项
# 多维搜索时可能含有更多的项
# 暂不支持多维搜索
def getOneMusicByType(dict):
    musicList = None
    if dict.has_key('type1'):
        musicList = Onlinemusic.objects.filter(type1=dict['type1'])
    if dict.has_key('type2'):
        musicList = Onlinemusic.objects.filter(type2=dict['type2'])
    if dict.has_key('type3'):
        musicList = Onlinemusic.objects.filter(type3=dict['type3'])
    if not dict.has_key('type1') and not dict.has_key('type2') and not dict.has_key('type3'):
        # 如果字典为空则返回完全随机的歌曲
        musicList = Onlinemusic.objects.all()
    # 在列表中完全随机选择音乐返回
    # 需要保证列表不为空否则出错
    if len(musicList) == 0:
        return None
    music = musicList[random.randint(0, len(musicList) - 1)]
    # 以字典的形式返回
    # 其中字符串均为unicode
    return {
        'Title': music.title,
        'Singer': music.singer,
        'Description': music.singer,
        'ImageUrl': music.imageURL
    }

# 添加用户
def adduser(openid):
    newuser = User(openid=openid, latestsignuptime=0, signupstatus='000000000000000000000000000000', sumtime=0)
    newuser.save()

# 删除用户
def deluser(openid):
    try:
        olduser = User.objects.get(openid=openid)
        olduser.delete()
    except User.DoesNotExist:
        return 'Error!'

# 获取最近三十天的签到情况
def getRecentInfobyID(ID):
    try:
        oneuser = User.objects.get(openid=ID)
        return oneuser.signupstatus
    except User.DoesNotExist:
        return ''

# 修改最近三十天的签到情况
def changeRecentInfo(ID, info):
    try:
        oneuser = User.objects.get(openid=ID)
        oneuser.signupstatus = info
        oneuser.save()
    except User.DoesNotExist:
        return 'Error!'

# 获取上一次签到的时间
def getLastTimebyID(ID):
    try:
        oneuser = User.objects.get(openid=ID)
        return oneuser.latestsignuptime
    except User.DoesNotExist:
        return 0

# 修改上一次签到的时间
def changeLastTime(ID, now):
    try:
        oneuser = User.objects.get(openid=ID)
        oneuser.latestsignuptime = now
        oneuser.save()
    except User.DoesNotExist:
        return 'Error!'
# 用户的总签到次数加1
def addsignintime(ID):
    try:
        oneuser = User.objects.get(openid=ID)
        oneuser.sumtime += 1
        oneuser.save()
    except User.DoesNotExist:
        return 'Error!'

# 获取某用户的总签到次数
def getsignintimebyID(ID):
    try:
        oneuser = User.objects.get(openid=ID)
        return oneuser.sumtime
    except User.DoesNotExist:
        return 'Error!'

