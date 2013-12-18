# coding=utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response
from .utils import checkSignature, parseXml
from .control import processMessage
from .library import getLibrarySeatInfo
from .database import insertonlinemusic
from .music import getRandomMusicByType

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
        message = parseXml(request.body)
        return HttpResponse(processMessage(message))

def library(request):
    dictArray = getLibrarySeatInfo()
    return render_to_response('library.html', {'seat': dictArray})

def musicplay(request):
    if request.GET.has_key('type') and request.GET.has_key('class'):
        dict = {'type' + request.GET['type']: request.GET['class']}
    else:
        dict = {}
    music = getRandomMusicByType(dict)
    return render_to_response('player.html', {
        'musicUrl': music['Url'],
        'title': music['Title'],
        'description': music['Description']
    })

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

        if (len(request.POST['LQURL']) == 0):
            musiccomplete = 0
            music['LQURLempty'] = 1
        else:
            music['LQURL'] = request.POST['LQURL']

        if (len(request.POST['HQURL']) == 0):
            musiccomplete = 0
            music['HQURLempty'] = 1
        else:
            music['HQURL'] = request.POST['HQURL']

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
