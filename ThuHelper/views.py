from django.http import HttpResponse

import hashlib

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
