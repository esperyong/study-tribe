# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url
import userena.views as userena_views
from studytribe.tribemember import forms
from studytribe.tribemember import views as memberviews

urlpatterns = patterns('studytribe',  

    url(r'^member/','tribemember.views.tribe_member',name='member'),

    url(r'^member/(?P<mid>[0-9]+)/$','tribemember.views.tribe_member',name='me'),

    url(r'^(signup|signin)/$',
       memberviews.signup_or_signin,
       name='studytribe_sign_main'),
    url(r'^$',
       memberviews.signup_or_signin,
       name='studytribe_sign_main'),

    # Activate
    url(r'^activate/(?P<activation_key>\w+)/$',
       userena_views.activate,
       {'success_url':"/accounts/%(username)s/"},
       name='tribemember_activate'),

)


