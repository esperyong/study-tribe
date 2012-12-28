# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url
import userena.views as userena_views
from studytribe.tribemember import forms
from studytribe.tribemember import views as memberviews
from userena import settings as userena_settings
from django.utils.translation import ugettext as _

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
    # url(r'^activate/(?P<activation_key>\w+)/$',
    #     userena_views.activate,
    #     {'success_url':"/accounts/%(username)s/"},
    #     name='tribemember_activate'),

    url(r'^activate/(?P<activation_key>\w+)/$',
       userena_views.activate,
       name='userena_activate'),

    url(r'^(?P<username>[\.\w]+)/signup/complete/$',
       userena_views.direct_to_user_template,
       {'template_name': 'studytribe/tribemember/signup_complete.html',
        'extra_context': {'userena_activation_required': userena_settings.USERENA_ACTIVATION_REQUIRED,
                          'userena_activation_days': userena_settings.USERENA_ACTIVATION_DAYS,
                          'title_text': _("Signup almost done!"),
                          }},
       name='userena_signup_complete'),

    # Disabled account
    url(r'^(?P<username>[\.\w]+)/disabled/$',
       userena_views.direct_to_user_template,
       { 
         'template_name': 'studytribe/tribemember/disabled_tribemember.html',
         'extra_context': {'title_text':_("Disabled account")},
        },
       name='userena_disabled'),


)


