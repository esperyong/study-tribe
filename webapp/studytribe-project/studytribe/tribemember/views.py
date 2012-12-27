# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from userena.decorators import secure_required
from userena.views import ExtraContextTemplateView
from userena import settings as userena_settings
from userena import signals as userena_signals
from userena.utils import signin_redirect, get_profile_model
from userena.forms import (SignupForm, SignupFormOnlyEmail, AuthenticationForm,
                           ChangeEmailForm, EditProfileForm)
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from studytribe.tribemember import forms

SIGNUP_FORM_NAME = 'signupform'
SIGNIN_FORM_NAME = 'signinform'

@csrf_protect
def tribe_member(request,mid=None):
    context = {}
    return render_to_response("studytribe/tribemember/base.html",
                              context,
                              context_instance=RequestContext(request))


def signup_or_signin(request,sign_type='signup'):
    print sign_type
    signup_form = forms.StudyTribeSignupForm
    signin_form = forms.StudyTribeSigninForm
    template_name = 'studytribe/tribemember/signin_or_signup.html'
    if sign_type == 'signup':
        return signup( request,
                signup_form=signup_form,
                template_name=template_name,
                extra_context={'signinform':signin_form,'signup':True} )
    else:
        return signin( request,
                auth_form=signin_form,
                template_name=template_name,
                extra_context={'signupform':signup_form,'signin':True} )

#几乎原样照抄userena的signup和login,view的代码,加上可以定制form在context中名字的代码
#因为在首页当中需要在一个页面中打印两个form表单,分别是loginform和signupform;
@secure_required
def signup(request, signup_form=SignupForm,
           template_name='studytribe/tribemember/signup_form.html', success_url=None,
           formname=SIGNUP_FORM_NAME,extra_context=None):

    if userena_settings.USERENA_WITHOUT_USERNAMES and (signup_form == SignupForm):
        signup_form = SignupFormOnlyEmail

    form = signup_form()

    if request.method == 'POST':
        form = signup_form(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Send the signup complete signal
            userena_signals.signup_complete.send(sender=None,
                                                 user=user)

            if success_url: redirect_to = success_url
            else: redirect_to = reverse('userena_signup_complete',
                                        kwargs={'username': user.username})

            # A new signed user should logout the old one.
            if request.user.is_authenticated():
                logout(request)
            return redirect(redirect_to)

    if not extra_context: extra_context = dict()
    extra_context[formname] = form
    return ExtraContextTemplateView.as_view(template_name=template_name,
                                            extra_context=extra_context)(request)

@secure_required
def signin(request, 
           auth_form=AuthenticationForm,
           template_name='studytribe/tribemember/signin_form.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           redirect_signin_function=signin_redirect, 
           formname=SIGNIN_FORM_NAME,
           extra_context=None):

    form = auth_form

    if request.method == 'POST':
        form = auth_form(request.POST, request.FILES)
        if form.is_valid():
            identification, password, remember_me = (form.cleaned_data['identification'],
                                                     form.cleaned_data['password'],
                                                     form.cleaned_data['remember_me'])
            user = authenticate(identification=identification,
                                password=password)
            if user.is_active:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(userena_settings.USERENA_REMEMBER_ME_DAYS[1] * 86400)
                else: request.session.set_expiry(0)

                if userena_settings.USERENA_USE_MESSAGES:
                    messages.success(request, _('You have been signed in.'),
                                     fail_silently=True)

                # Whereto now?
                redirect_to = redirect_signin_function(
                    request.REQUEST.get(redirect_field_name), user)
                return redirect(redirect_to)
            else:
                return redirect(reverse('userena_disabled',
                                        kwargs={'username': user.username}))

    if not extra_context: extra_context = dict()
    extra_context.update({
        formname: form,
        'next': request.REQUEST.get(redirect_field_name),
    })
    return ExtraContextTemplateView.as_view(template_name=template_name,
                                            extra_context=extra_context)(request)


