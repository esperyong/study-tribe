# coding: utf-8
from userena.forms import SignupForm,AuthenticationForm
from captcha.fields import CaptchaField
from django.utils.translation import ugettext as _
from django import forms
from django.conf import settings
from userena.models import UserenaSignup

USERNAME_RE= r'^\S+$'

def set_captcha_widgets(widgets):
    if widgets:
        for widget in widgets:
            widget.attrs['class'] = 'span1'
            widget.attrs['maxlength'] = '10'
            widget.attrs['placeholder'] = u'验证码'

def set_fields_bootstrap_class(field):
    for widget in field.widget.widgets:
        widget.attrs['placeholder'] = field.label

class StudyTribeSignupForm(SignupForm):

    captcha = CaptchaField(error_messages={'invalid': _(u'accounts.invalid_captcha')})
    set_captcha_widgets(captcha.widget.widgets)

    username = forms.RegexField(regex=USERNAME_RE,
                                max_length=30,
                                widget=forms.TextInput(attrs={'placeholder':_("Username")}),
                                label=_("Username"),
                                error_messages={'invalid': _('Username must contain only letters, numbers, dots and underscores.')})

    email = forms.EmailField(widget=forms.TextInput(
                                         attrs={
                                             'placeholder':_("Email")
                                             }),
                                         label=_("Email"))

    password1 = forms.CharField(widget=forms.PasswordInput(
                                         attrs={'placeholder':_("Create password")},
                                         render_value=False),
                                         label=_("Create password"))

    password2 = forms.CharField(widget=forms.PasswordInput(
                                         attrs={'placeholder':_("Repeat password")},
                                         render_value=False),
                                         label=_("Repeat password"))

    def save(self,activate_required=settings.USERENA_ACTIVATION_REQUIRED):
        """ Creates a new user and account. Returns the newly created user. """
        username, email, password = (self.cleaned_data['username'],
                                     self.cleaned_data['email'],
                                     self.cleaned_data['password1'])

        new_user = UserenaSignup.objects.create_user(username,
                                                     email,
                                                     password,
                                                     not activate_required,
                                                     activate_required)
        return new_user


def identification_field_factory(label, error_required):
    """
    A simple identification field factory which enable you to set the label.

    :param label:
        String containing the label for this field.

    :param error_required:
        String containing the error message if the field is left empty.

    """
    return forms.CharField(label=label,
                           widget=forms.TextInput(attrs={'placeholder':label}),
                           max_length=75,
                           error_messages={'required': _("%(error)s") % {'error': error_required}})

class StudyTribeSigninForm(AuthenticationForm):
    """
    A custom form where the identification can be a e-mail address or username.

    """
    identification = identification_field_factory(_(u"Email or username"),
                                                  _(u"Either supply us with your email or username."))

    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(
                                   attrs={'placeholder':_("Password")}, 
                                   render_value=False))

