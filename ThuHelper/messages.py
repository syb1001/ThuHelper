# coding=utf-8

import sys
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('UTF-8')

import time
import xml.etree.ElementTree as ET
from .utils import makeXml

# 开发者可以通过填写FuncFlag字段为1来对消息进行星标，你可以在实时消息的星标消息分类中找到该消息
# req_msg is a dictionary containing the information of request message
# dic is a dictionary containing the information to construct a new response message
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