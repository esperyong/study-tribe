# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from studytribe.studygroup import views 

urlpatterns = patterns('',
    url(r'^studygroups/$', views.StudyGroupListRes.as_view()),
    url(r'^studygroups/(?P<pk>[0-9]+)/$', views.StudyGroupRes.as_view())
)

urlpatterns = format_suffix_patterns(urlpatterns)

