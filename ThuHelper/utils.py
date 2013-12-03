import hashlib
from xml.etree import ElementTree as ET

from .settings import WEIXIN_TOKEN

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