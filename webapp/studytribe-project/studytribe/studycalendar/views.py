# -*- coding:utf-8 -*-
from django.views.generic import TemplateView
from django.utils.decorators import classonlymethod

class StudyCalendarView(TemplateView):
    template_name = "studytribe/studycalendar/base.html"

class MyTemplateView(object):
    def as_view(cls,**initkargs):
        pass
