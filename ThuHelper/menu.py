# -*- encoding: utf-8 -*-
#改菜单的时候手动运行一下。。
import urllib
import urllib2
from urllib import urlencode
import json
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')


gettoken = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx908467c39426e3bc&secret=82729dab279ea74bab044cd868ec1543"

f = urllib2.urlopen( gettoken )


stringjson = f.read() 

access_token = json.loads(stringjson)['access_token']

#print access_token

posturl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + access_token

menu = '''{
     "button":[
       {
           "name":"上自习",
           "sub_button":
           [{
               "type":"click",
               "name":"文图座位查询",
               "key":"WTZWCX"
            },
           {
               "type":"click",
               "name":"教室排课查询",
               "key":"JSPKCX"
            },
            
            {
               "type":"click",
               "name":"教学楼查询",
               "key":"JXLCX"
            }
            ]
       },

      {
           "name":"摇一摇",
           "sub_button":
           [{
               "type":"click",
               "name":"来点儿音乐",
               "key":"LDYY"
            },
            {
               "type":"click",
               "name":"去哪儿吃饭",
               "key":"QNC"
            },
            {
               "type":"click",
               "name":"去哪儿学习",
               "key":"QNX"
            }
            ]

      },
      {
           "name":"签个到",
           "sub_button":
           [{
               "type":"click",
               "name":"签到",
               "key":"QD"
            },
            {
               "type":"click",
               "name":"帮助",
               "key":"HELP"
            },
            {
               "type":"click",
               "name":"关于我们",
               "key":"ABOUT"
            },
            
            ]
       }]
 }'''


request = urllib2.urlopen(posturl, menu.encode('utf-8') )

print request.read()
