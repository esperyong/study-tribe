# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from studytribe.studygroup import views 
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    #url(r'^$', views.StudyTribeListRes.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.StudyTribeRes.as_view()),
    url(r'^(?P<tribe_id>[0-9]+)/studygroups/$', 
            views.StudyGroupListRes.as_view()),
    url(r'^studygroups/(?P<pk>[0-9]+)/$', views.StudyGroupRes.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += patterns('studytribe',  

    url(r'^studygroups/$',
        'studygroup.views.study_group_list',
        name='study-group-list'),

    url(r'^tribemember/invite-people/$',direct_to_template,
        {'template': 'studytribe/tribemember/invite_member.html'},
        name='invite-tribe-member'),

     url(r'^studygroups/projects_details/$',direct_to_template,
         {'template': 'studytribe/studygroup/projects_details.html'},
         name='projects_details'),

)

