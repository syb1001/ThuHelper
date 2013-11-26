import hashlib

import sys
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('UTF-8')

from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from .utils import *
from .messages import *

"""
def checkSignature(request):
    token = 'helloworld'

    signature = request.GET.get('signature', '')
    timestamp = request.GET.get('timestamp', '')
    nonce = request.GET.get('nonce', '')
    echostr = request.GET.get('echostr', '')

    infostr = ''.join(sorted([token, timestamp, nonce]))
    if hashlib.sha1(infostr).hexdigest() == signature:
        return HttpResponse(echostr)
    else:
        return HttpResponse("Invalid Request")
"""

def echo(text):
    return text

def index(req):
    if not checkSig(req):
        return HttpResponseForbidden()
    if req.method == 'GET':
        return HttpResponse(req.GET.get('echostr', ''))
    req_msg = parseXml(req)
    ret = 'Null Response.'

    if req_msg.get('MsgType', '') == 'text':
        # uncomment the next line when you implement response
        # ret = response(req_msg.get('Content', ''))
        ret = req_msg.get('Content', '')

    return HttpResponse(makeTextMsg(req_msg, ret))