import hashlib
from xml.etree import ElementTree as ET

from .settings import WEIXIN_TOKEN
import datetime

def checkSignature(request):
    token = WEIXIN_TOKEN

    signature = request.GET['signature']
    timestamp = request.GET['timestamp']
    nonce = request.GET['nonce']

    str = ''.join(sorted([token, timestamp, nonce]))

    if hashlib.sha1(str).hexdigest() == signature:
        return True
    else:
        return False

def parseXml(xml):
    xml_tree = ET.fromstring(xml)
    content = dict()
    for i in xml_tree:
        content[i.tag] = i.text
    return content

# 根据时间返回课程时间序号, 可选参数为偏移分钟数
def getClassSeqNumByDatetime(_datetime, _deltaMinute = 0):
    delta = datetime.timedelta(0, 0, 0, 0, _deltaMinute)
    dt = _datetime + delta  
    hours =   9,  12, 15, 16, 18, 21
    minutes = 35, 15,  5, 55, 40, 45
    timeList = list()
    for i in range(6):
        timeList.append(dt.replace(dt.year, dt.month, dt.day, hours[i], minutes[i]))
    timeTuple = tuple(timeList)
    classSeqNum = 0;
    if dt >= timeTuple[5]:
        classSeqNum = 6
    else:
        for i in range(6):
            if dt < timeTuple[i]:
                classSeqNum = i + 1
                break        
    return classSeqNum

# 根据当前时间返回课程时间序号, 可选参数为偏移分钟数
def getClassSeqNumByNowTime(_deltaMinute = 0):
    dt = datetime.datetime.now()
    return getClassSeqNumByDatetime(dt, _deltaMinute)