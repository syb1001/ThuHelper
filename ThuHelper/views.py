from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from xml.etree import ElementTree as ET

import hashlib, time

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def checkSignature(request):
    token = 'helloworld'

    signature = request.GET.get('signature', '')
    timestamp = request.GET.get('timestamp', '')
    nonce = request.GET.get('nonce', '')
    echostr = request.GET.get('echostr', '')

    infostr = ''.join(sorted([token, timestamp, nonce]))
    if hashlib.sha1(infostr).hexdigest() == signature:
        if request.GET.has_key('echostr'):
            return HttpResponse(echostr)
        else:
            reply = '<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content></xml>'
            xml = ET.fromstring(request.body)
            content = xml.find("Content").text
            fromUserName = xml.find("ToUserName").text
            toUserName = xml.find("FromUserName").text
            return HttpResponse(reply % (toUserName, fromUserName, str(int(time.time())), content))
    else:
        return HttpResponse("Invalid Request")
