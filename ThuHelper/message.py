# coding=utf-8

# message.py
# 消息的生成与发送

from django.template.loader import get_template
from django.template import Context
import time

# 文字消息
def makeTextMessage(toUser, fromUser, content):
    template = get_template('xml_text.xml')
    context = Context({
        'ToUserName': toUser,
        'FromUserName': fromUser,
        'CreateTime': str(int(time.time())),
        'Content': content
    })
    return template.render(context)
