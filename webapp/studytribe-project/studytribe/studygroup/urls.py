# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('studytribe.studygroup.views',
    url(r'^studygroups/$', 'studygroup_list'),
    url(r'^studygroups/(?P<pk>[0-9]+)/$', 'studygroup_detail')
)

urlpatterns = format_suffix_patterns(urlpatterns)
