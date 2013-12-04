# coding=utf-8

# classroom.py
# 教室排课信息获取

from database import getclassroomsbyfloor
from utils import getClassSeqNumByDatetime
import datetime 

# 图文消息所需信息
def getClassroomInfoArticles(queryStr):
	queryTuple = parseQuery(queryStr)
	retList = list()
	retList.append({
        'Title': u'空闲教室:',
        'PicUrl': '',
        'Url': ''
    })
	return retList


def parseQuery(queryStr):
	return {'ID':''}

def getClassroomInfoArticles_simple(queryStr):
	queryDict = getBuildFloor(queryStr)
	buildID = queryDict['buildID']
	floor = queryDict['floor']
	dt = datetime.datetime.now()
	classSeqNum = getClassSeqNumByDatetime(dt, 5)
	buildname = buildIDtoName(buildID)
	weekday = datetime.date(dt.year, dt.month, dt.day).weekday()

	roomList = getclassroomsbyfloor(buildID, floor, classSeqNum, weekday)
	itemList = list()
	for room in roomList:
		itemList.append({
			'Title': room['roomnumber'],
			'PicUrl': '',
			'Url': ''
		})

	retList = list()
	retList.append({
        'Title': dt.month + u'月' + dt.day + u'日 ' + buildname + u' 第' + str(classSeqNum) + u'大节' + u'空闲教室:',
        'PicUrl': '',
        'Url': ''
    })
	if len(itemList) > 10:
		itemTuple = tuple(itemList)
    	for i in range(10):
    		retList.append(itemTuple[i])
	else:
		retList.extend(itemList)
	return retList


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