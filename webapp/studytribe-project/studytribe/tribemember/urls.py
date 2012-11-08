# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('studytribe',  
    url(r'^member/','tribemember.views.tribe_member',name='member'),
    url(r'^member/(?P<mid>[0-9]+)/$','tribemember.views.tribe_member',name='me'),
)


