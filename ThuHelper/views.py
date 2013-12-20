# coding=utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response
from ThuHelper.utils import checkSignature, parseXml
from ThuHelper.control import processMessage
from ThuHelper.library import getLibrarySeatInfo
from ThuHelper.database import insertonlinemusic
from .music import getRandomMusicByType

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt

def entry(request):
    # 进行token验证
    #if not checkSignature(request):
    #    return HttpResponse('Invalid Request')

    if request.GET.has_key('echostr'):
        # 接入微信公众平台的情�?        # 按微信平台要求返回echostr以�?过验�?
        return HttpResponse(request.GET['echostr'])
    else:
        message = parseXml(request.body)
        return HttpResponse(processMessage(message))

def library(request):
    dictArray = getLibrarySeatInfo()
    return render_to_response('library.html', {'seat': dictArray})

def musicplay(request):
    dict = {'type' + request.GET['type']: request.GET['class']}
    music = getRandomMusicByType(dict)
    return render_to_response('player.html', {'musicUrl': music['Url']})

def insertmusic(request):
    music = {}
    musiccomplete = 1
    if (request.method == 'POST'):
        if (len(request.POST['title']) == 0):
            musiccomplete = 0
            music['titleempty'] = 1
        else:
            music['title'] = request.POST['title']

        if (len(request.POST['singer']) == 0):
            musiccomplete = 0
            music['singerempty'] = 1
        else:
            music['singer'] = request.POST['singer']

        if (len(request.POST['description']) == 0):
            musiccomplete = 0
            music['descriptionempty'] = 1
        else:
            music['description'] = request.POST['description']

        if (len(request.POST['imageURL']) == 0):
            musiccomplete = 0
            music['imageURLempty'] = 1
        else:
            music['imageURL'] = request.POST['imageURL']

        if (musiccomplete == 1):
            music['type1'] = request.POST['type1']
            music['type2'] = request.POST['type2']
            music['type3'] = request.POST['type3']
            insertonlinemusic(music)
            return render_to_response('insertmusic.html', {
                'insertsuccess' : 1,
            })
        else:
            return render_to_response('insertmusic.html', {
                'music' : music,
            })
    else:
        return (render_to_response('insertmusic.html'))
