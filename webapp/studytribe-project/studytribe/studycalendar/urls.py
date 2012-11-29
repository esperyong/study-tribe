# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from studytribe.studygroup import views 
from studytribe.studycalendar.views import StudyCalendarView
urlpatterns = patterns('',  
    url(r'^studycalendar/',
        StudyCalendarView.as_view(),
        name='study-calendar'),
)

