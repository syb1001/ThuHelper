# coding=utf-8

# views.py
# 定义视图

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
import random
import json

from .utils import checkSignature, parseXml
from .control import processMessage
from .library import getLibrarySeatInfo
from .database import insertonlinemusic, updateclassroombyweek
from .music import getRandomMusicByType
from .settings import URL_ALBUM_PREF, MAX_ALBUM_IMAGE_INDEX

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt

# 微信消息推送入口
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

# 文图座位信息页面
def library(request):
    dictArray = getLibrarySeatInfo()
    return render_to_response('library.html', {'seat': dictArray})

# 帮助信息页面
def help(request):
    return render_to_response('help.html', {})

def about(request):
    return render_to_response('about.html', {})

# 音乐播放器页面
def musicplay(request):
    if request.GET.has_key('type') and request.GET.has_key('class'):
        dict = {'type' + request.GET['type']: request.GET['class']}
    else:
        dict = {}
    music = getRandomMusicByType(dict)
    return render_to_response('player.html', {
        'musicUrl': music['Url'],
        'title': music['Title'],
        'description': music['Description'],
        'imageUrl': music['ImageUrl'],
        'albumUrl': URL_ALBUM_PREF + str(random.randint(1, MAX_ALBUM_IMAGE_INDEX)) + '.jpg'
    })

def dataupdate(request):
    data = request.POST['data']
    #aa = json.dumps(data)
    data = json.loads(data)
    week = data['weekday']
    building = data['building']
    for classroom in data['status']:
        updateclassroombyweek(str(building), classroom['name'], week, classroom['status'])
    length = len(request.POST)
    response = HttpResponse(simplejson.dumps({'message': 'ok', 'statusCode': 0, 'dictLength': length}, ensure_ascii=False))
    response['Access-Control-Allow-Origin'] = '*'
    return response

# 音乐插入后台页面
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
