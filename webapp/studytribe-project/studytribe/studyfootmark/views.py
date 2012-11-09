# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def footmark(request):
    context = {}
    return render_to_response("studytribe/studyfootmark/base.html",
                              context,
                              context_instance=RequestContext(request))



