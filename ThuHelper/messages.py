import sys
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('UTF-8')

import time
import xml.etree.ElementTree as ET
from .utils import makeXml

def makeMsg(req_msg, dic):
    dic.update({
        'ToUserName': req_msg['FromUserName'], 
        'FromUserName': req_msg['ToUserName'], 
        'CreateTime': str(int(time.time())), 
        'FuncFlag': '0', 
        })
    return ET.tostring(makeXml(dic), 'utf8')

def makeTextMsg(req_msg, text):
    return makeMsg(req_msg, {
        'MsgType': 'text', 
        'Content': text, 
        })