# coding=utf-8

# urls.py
# 路由配置

from django.conf.urls import patterns, include, url
from django.conf import settings
from ThuHelper.database import dbinit, dbtest

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ThuHelper.views.home', name='home'),
    # url(r'^ThuHelper/', include('ThuHelper.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'ThuHelper.views.entry'),
    url(r'^library/$', 'ThuHelper.views.library'),
    url(r'^musicplay$', 'ThuHelper.views.musicplay'),
    url(r'^help/$', 'ThuHelper.views.help'),
    url(r'^about/$', 'ThuHelper.views.about'),
    url(r'^dataupdate/$', 'ThuHelper.views.dataupdate'),
    url(r'^dbinit/', dbinit),
    url(r'^dbtest/', dbtest),
    url(r'^insertmusic/', 'ThuHelper.views.insertmusic'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATICFILES_DIRS[0],
        'show_indexes': True
    }),
)