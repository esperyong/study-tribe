# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from studytribe.invitation import views as invitation_views
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^invitation/accept/(?P<invitation_key>\w+)/$',
        invitation_views.accept_invitation,
        name='accept_invitation'),
)

