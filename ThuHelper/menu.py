# coding=utf-8

# menu.py
# 设置微信服务号菜单
# 菜单变化时需手动运行

import urllib2, json, sys
from ThuHelper.settings import APPID, APP_SECRET, URL_ABOUT

reload(sys)
sys.setdefaultencoding('UTF-8')

url_get_token = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + APPID + '&secret=' + APP_SECRET
f = urllib2.urlopen(url_get_token)
string_json = f.read()
access_token = json.loads(string_json)['access_token']
#print access_token

posturl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + access_token
menu = '''{
    "button": [
        {
            "name": "上自习",
            "sub_button": [
                {
                    "type": "click",
                    "name": "文图座位查询",
                    "key": "LIBRARY"
                }, {
                    "type": "click",
                    "name": "教室排课查询",
                    "key": "COURSE"
                }, {
                    "type": "click",
                    "name": "空闲教室查询",
                    "key": "CLASSROOM"
                }
            ]
        },

        {
            "name": "摇一摇",
            "sub_button": [
                {
                    "type": "click",
                    "name": "来点儿音乐",
                    "key": "MUSIC"
                }, {
                    "type": "click",
                    "name": "去哪儿吃饭",
                    "key": "MEAL"
                }, {
                    "type": "click",
                    "name": "去哪儿学习",
                    "key": "STUDY"
                }
            ]
        },

        {
            "name": "签个到",
            "sub_button": [
                {
                    "type": "click",
                    "name": "签到",
                    "key": "SIGNIN"
                }, {
                    "type": "click",
                    "name": "帮助",
                    "key": "HELP"
                }, {
                    "type": "view",
                    "name": "关于我们",
                    "key": "''' + URL_ABOUT + '''"
                },
            ]
        }
    ]
}'''
request = urllib2.urlopen(posturl, menu.encode('utf-8') )
print request.read()
