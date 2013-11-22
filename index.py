#-*- coding:utf-8 -*-

# def app(environ, start_response):
#     status = '200 OK'
#     headers = [('Content-type', 'text/html')]
#     start_response(status, headers)
#     body=["Welcome to Baidu Cloud!\n"]
#     return body

# from bae.core.wsgi import WSGIApplication
# application = WSGIApplication(app)

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'ThuHelper.settings'

path = os.path.dirname(os.path.abspath(__file__)) + '/ThuHelper'
if path not in sys.path:
    sys.path.insert(1, path)

from django.core.handlers.wsgi import WSGIHandler
from bae.core.wsgi import WSGIApplication

application = WSGIApplication(WSGIHandler())
