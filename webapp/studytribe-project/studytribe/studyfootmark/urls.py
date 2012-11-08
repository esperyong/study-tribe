# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from studytribe.studygroup import views 

urlpatterns = patterns('studytribe',  
    url(r'^studyfootmark/','studyfootmark.views.footmark',name='study-footmark'),
)

