# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from studytribe.studyfootmark import views 

urlpatterns = patterns('',  
    url(r'^studyfootmark/',views.StudyFootmarkView.as_view(),name='study-footmark'),
)

