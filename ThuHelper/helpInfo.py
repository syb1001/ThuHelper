# coding=utf-8

# helpInfo.py
# 帮助信息获取

from .settings import URL_HELP_IMAGE, URL_HELP, URL_HELP_IMAGE_PREF

# 图文消息所需信息
def getHelpInfoArticles():
    return [{
        'Title': u'清华自习小助手功能介绍',
        'PicUrl': URL_HELP_IMAGE,
        'Url': URL_HELP
    }, {
        'Title': u'查询文科图书馆座位情况：\n点击菜单查看，或发送“人文馆”或“文图”等相关词语',
        'PicUrl': URL_HELP_IMAGE_PREF + 'book.jpg',
        'Url': URL_HELP
    }, {
        'Title': u'查询某教室今日课程安排：\n发送“6C301”、“4104”、\n“5205”等',
        'PicUrl': URL_HELP_IMAGE_PREF + 'pencil.jpg',
        'Url': URL_HELP
    }, {
        'Title': u'查询某教学楼空闲教室：\n发送“今天第二节四教二层”、“三教一段二层”、“五教”等',
        'PicUrl': URL_HELP_IMAGE_PREF + 'home.jpg',
        'Url': URL_HELP
    }, {
        'Title': u'播放音乐：\n点击菜单获取音乐列表，也可发送“音乐”或音乐类型',
        'PicUrl': URL_HELP_IMAGE_PREF + 'music.jpg',
        'Url': URL_HELP
    }, {
        'Title': u'点此消息查看更多',
        'Url': URL_HELP
    }]