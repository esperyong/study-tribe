# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url
import userena.views as userena_views
from studytribe.tribemember import forms

urlpatterns = patterns('studytribe',  

    url(r'^member/','tribemember.views.tribe_member',name='member'),

    url(r'^member/(?P<mid>[0-9]+)/$','tribemember.views.tribe_member',name='me'),

    url(r'^signup/$',
       userena_views.signup,
       {
           'template_name':'accounts/signup_form.html',
           'signup_form':forms.StudyTribeSignupForm,
        },
       name='tribemember_signup'),

    url(r'^login/$',
       userena_views.signin,
       {
           'template_name':'accounts/login.html',
           'auth_form':forms.StudyTribeAuthForm,
        },
       name='tribemember_signin'),

    url(r'^$',
       userena_views.signin,
       {
           'template_name':'studytribe/tribemember/login_or_signup.html',
           'auth_form':forms.StudyTribeAuthForm,
        },
       name='studytribe_index'),


    # Activate
    url(r'^activate/(?P<activation_key>\w+)/$',
       userena_views.activate,
       {'success_url':"/accounts/%(username)s/"},
       name='tribemember_activate'),

)


