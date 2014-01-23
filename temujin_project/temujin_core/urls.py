from django.conf.urls import patterns, include, url

from .views import CreateNsView, serve_file

urlpatterns = patterns('',
    
    url(r'^commands/getns/$',CreateNsView.as_view(), name="temujin_create_namespace"),

    url(r'^resources/file/(?P<ns>.+)/(?P<filename>.+)/$', serve_file, name="temujin_serve_file"),
    
)
