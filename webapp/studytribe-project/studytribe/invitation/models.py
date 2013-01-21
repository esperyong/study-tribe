import random
import datetime

from django.conf import settings

from django.contrib.auth.models import User,Group
from django.contrib.sites.models import Site, RequestSite
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string

from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.utils.hashcompat import sha_constructor

from userena.utils import get_protocol
from studytribe.invitation import signals

INVITATION_PERM_TYPE_OWNER='owner'
INVITATION_PERM_TYPE_ADMIN='admin'
INVITATION_PERM_TYPE_MEMBER='member'

class InvitationManager(models.Manager):

    def invite(self, user, email,target,perm_type=INVITATION_PERM_TYPE_MEMBER):
        """
        Get or create an invitation for ``email`` from ``user`` to ``target``
        This method doesn't an send email. You need to call ``send_invitation()``
        method on returned ``Invitation`` instance.
        """
        invitation = None
        try:
            # It is possible that there is more than one invitation fitting
            # the criteria. Normally this means some older invitations are
            # expired or an email is invited consequtively.
            ctype = ContentType.objects.get_for_model(target)
            invitation = self.filter(user=user,
                                     email=email,
                                     target_content_type=ctype,
                                     target_object_id=target.id,
                                     perm_type=perm_type
                                     )[0]
            if not invitation.is_valid():
                invitation = None
        except (Invitation.DoesNotExist, IndexError):
            pass
        if invitation is None:
            #user.invitation_stats.use()
            key = '%s%0.16f%s%s' % (settings.SECRET_KEY,
                                    random.random(),
                                    user.email,
                                    email)
            key = sha_constructor(key).hexdigest()
            invitation = self.create(user=user, 
                                     email=email, 
                                     key=key,
                                     target=target,
                                     perm_type=perm_type)
        if invitation.invite_user_type == settings.INVITE_USER_TYPE_TRIBER:
            invitation.assign_perms()
        return invitation
    invite.alters_data = True

    def find(self, invitation_key):
        """
        Find a valid invitation for the given key or raise
        ``Invitation.DoesNotExist``.

        This function always returns a valid invitation. If an invitation is
        found but not valid it will be automatically deleted.
        """
        try:
            invitation = self.filter(key=invitation_key)[0]
        except IndexError:
            raise Invitation.DoesNotExist
        if not invitation.is_valid():
            invitation.delete()
            raise Invitation.DoesNotExist
        return invitation

    def valid(self):
        """Filter valid invitations.
        """
        expiration = now() - datetime.timedelta(settings.INVITATION_EXPIRE_DAYS)
        return self.get_query_set().filter(date_invited__gte=expiration)

    def invalid(self):
        """Filter invalid invitation.
        """
        expiration = now() - datetime.timedelta(settings.INVITATION_EXPIRE_DAYS)
        return self.get_query_set().filter(date_invited__le=expiration)

class Invitation(models.Model):
    user = models.ForeignKey(User, related_name='invitations')
    email = models.EmailField(_(u'e-mail'))
    key = models.CharField(_(u'invitation key'), max_length=40, unique=True)
    date_invited = models.DateTimeField(_(u'date invited'),default=now)
    perm_type = models.CharField(max_length=10)

    target_content_type = models.ForeignKey(ContentType)
    target_object_id = models.PositiveIntegerField()
    target = generic.GenericForeignKey('target_content_type','target_object_id')


    objects = InvitationManager()

    class Meta:
        verbose_name = _(u'invitation')
        verbose_name_plural = _(u'invitations')
        ordering = ('-date_invited',)

    def __unicode__(self):
        return _('%(username)s invited %(email)s on %(date)s') % {
            'username': self.user.username,
            'email': self.email,
            'date': str(self.date_invited.date()),
        }

    @models.permalink
    def get_absolute_url(self):
        return ('accept_invitation', (), {'invitation_key': self.key})

    @property
    def _expires_at(self):
        return self.date_invited + datetime.timedelta(settings.INVITATION_EXPIRE_DAYS)

    @property
    def invite_user_type(self):
        if not hasattr(self,'_invite_user_type') or self._invite_user_type is None:
            if self.invitee is None:
                self._invite_user_type = settings.INVITE_USER_TYPE_NOT_TRIBER
            else:
                user = self.invitee
                if user.is_active:
                    self._invite_user_type = settings.INVITE_USER_TYPE_TRIBER
                else:
                    self._invite_user_type = settings.INVITE_USER_TYPE_INACTIVE_TRIBER
        return self._invite_user_type

    @property
    def invitee(self):
        if not hasattr(self,'_invitee') or self._invitee is None:
            users = User.objects.filter(email=self.email)
            if len(users) > 0:
                self._invitee = users[0]
            else:
                self._invitee = None
        return self._invitee

    @property
    def invite_link(self):
        if not hasattr(self,'_invite_link') or self._invite_link is None:
            if self.invite_user_type == settings.INVITE_USER_TYPE_TRIBER:
                #print self.target
                self._invite_link = self.target.get_absolute_url()
            else:
                self._invite_link = self.get_absolute_url()
        return self._invite_link 

    def is_valid(self):
        """
        Return ``True`` if the invitation is still valid, ``False`` otherwise.
        """
        return now() < self._expires_at

    def expiration_date(self):
        """Return a ``datetime.date()`` object representing expiration date.
        """
        return self._expires_at.date()
    expiration_date.short_description = _(u'expiration date')
    expiration_date.admin_order_field = 'date_invited'

    def send_invitation(self, target=None, site=None, 
            request=None,method=settings.INVITATION_DEFAULT_INVITATION_METHOD):
        """
        Send invitation inform through email or sms or other method
        """
        if method == settings.INVITATION_DEFAULT_INVITATION_METHOD:
            self.send_email(target,site,request)

    def assign_perms(self):
        if self.invitee is not None and self.invitee.is_active:
            if self.perm_type == INVITATION_PERM_TYPE_OWNER: 
                self.target.add_user_to_owner_group(self.invitee)
            elif self.perm_type == INVITATION_PERM_TYPE_ADMIN:
                self.target.add_user_to_admin_group(self.invitee)
            else:
                self.target.add_user_to_member_group(self.invitee)

    def send_email(self, email=None, site=None, request=None):
        """
        Send invitation email.

        Both ``email`` and ``site`` parameters are optional. If not supplied
        instance's ``email`` field and current site will be used.

        **Templates:**

        :studytribe/invitation/invitation_email_subject.txt:
            Template used to render the email subject.

            **Context:**

            :invitation: ``Invitation`` instance ``send_email`` is called on.
            :site: ``Site`` instance to be used.

        :studytribe/invitation/invitation_email_message.txt:
            Template used to render the email body.

            **Context:**

            :invitation: ``Invitation`` instance ``send_email`` is called on.
            :expiration_days: ``INVITATION_EXPIRE_DAYS`` setting.
            :site: ``Site`` instance to be used.

        **Signals:**

        ``invitation.signals.invitation_sent`` is sent on completion.
        """
        email = email or self.email
        if site is None:
            if Site._meta.installed:
                site = Site.objects.get_current()
            elif request is not None:
                site = RequestSite(request)
        subject = render_to_string('studytribe/invitation/invitation_email_subject.txt',
                                   {'invitation': self, 'site': site})
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        message = render_to_string('studytribe/invitation/invitation_email_message.txt', 
                                  {'invitation': self,
                                  'expiration_days': settings.INVITATION_EXPIRE_DAYS,
                                  'site': site,
                                  'protocol':get_protocol()})
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        signals.invitation_sent.send(sender=self)

    def mark_accepted(self, new_user):
        """
        Update sender's invitation statistics and delete self.

        ``invitation.signals.invitation_accepted`` is sent just before the
        instance is deleted.
        """
        #self.user.invitation_stats.mark_accepted()
        signals.invitation_accepted.send(sender=self,
                                         inviting_user=self.user,
                                         new_user=new_user)
        if invitation.invite_user_type != settings.INVITE_USER_TYPE_TRIBER:
            self.assign_perms()
        self.delete()
    mark_accepted.alters_data = True

