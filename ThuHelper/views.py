# coding=utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response
from .utils import checkSignature, parseXml
from .control import processMessage
from .library import getLibrarySeatInfo
from .music import getRandomMusic

# 防止403 error的语句
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt

def entry(request):
    # 进行token验证
    #if not checkSignature(request):
    #    return HttpResponse('Invalid Request')

    if request.GET.has_key('echostr'):
        # 接入微信公众平台的情况
        # 按微信平台要求返回echostr以通过验证
        return HttpResponse(request.GET['echostr'])
    else:
        # 接收用户消息的情况
        message = parseXml(request.body)
        return HttpResponse(processMessage(message))

def library(request):
    dictArray = getLibrarySeatInfo()
    return render_to_response('library.html', {'seat': dictArray})

def musicplay(request):
    music = getRandomMusic()
    return render_to_response('player.html', {'musicUrl': music['Url']})