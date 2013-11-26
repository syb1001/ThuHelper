from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from ThuHelper.views import checkSignature

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ThuHelper.views.home', name='home'),
    # url(r'^ThuHelper/', include('ThuHelper.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^access/$', checkSignature),
)
