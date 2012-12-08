# -*- coding:utf-8 -*-
from studytribe.studycalendar import views 
from django.conf.urls import patterns, url

urlpatterns = patterns('',  
    url(r'^studycalendar/',views.StudyCalendarView.as_view(),name='study-calendar'),
)

