# coding=utf-8

# control.py
# 消息处理的逻辑
# 判断用户发送消息的用途
# 返回用户不同类型不同内容的消息

from message import makeTextMessage

def processMessage(message):
    # 根据用户发来的消息返回对应的消息
    if message['MsgType'] == 'text':
        # 文字消息原样返回
        response = message['Content']
        return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
    else:
        # 其他类型的消息不支持
        response = '目前不支持非文字消息'
        return makeTextMessage(message['FromUserName'], message['ToUserName'], response)
