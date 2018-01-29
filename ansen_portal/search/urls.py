from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.search, name='newsearch'),
    url(r'^an/$', views.projlist, name='projlist'),
    url(r'^an/(?P<pid>\d+)$', views.project, name='project')
]
