# coding: utf-8
from django.test import TestCase
from studytribe.invitation.models import Invitation
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from bs4 import BeautifulSoup
from captcha.models import CaptchaStore,get_safe_now
import re
from userena.models import UserenaSignup
from userena import signals as userena_signals


class InvitationTest(TestCase):

    def setUp(self):
        UserenaSignup.objects.check_permissions()

    def _sign_up_user(self,username,email,password):
        response = self.client.get(reverse('studytribe_sign_main',args=['signup']))
        soup = BeautifulSoup(response.content)
        ne = soup.find('input',{'id':'id_captcha_0'})
        hashkey_from_page = ne['value']
        csobj = CaptchaStore.objects.get(hashkey=hashkey_from_page)
        input_captcha = csobj.challenge
        data = {'username':username,
                'email':email,
                'password1':password,
                'password2':password,
                'captcha_0':hashkey_from_page,
                'captcha_1':input_captcha,}

        response = self.client.post(reverse('studytribe_sign_main',args=['signup']),data)
        user = User.objects.get(username__exact=username)
        user.is_active = True
        user.save()
        userena_signals.activation_complete.send(sender=None,user=user)
        return user

    def test_invite_tribe_member(self):
        """
        邀请一个已经是部落成员的用户
        直接赋予权限,并发送邮件,甚至可以发送站内消息;
        邀请链接:
        直接引导到邀请所在的链接,
        比如邀请到某一个部落,
        一个班级,一个课程.
        """
        user1 = self._sign_up_user('user1','user1@xuexibuluo.com','123456')
        user2 = self._sign_up_user('user2','user2@xuexibuluo.com','123456')
        invitation_target = user1.owned_tribe
        invitation = Invitation.objects.invite(user1,user2.email,invitation_target)
        self.assertNotEquals(invitation,None)
        invitation.send_invitation(user1.email)
        self.assertEquals(len(mail.outbox),3)#activation+invitation
        mail_subject = mail.outbox[2].subject
        mail_content = mail.outbox[2].body
        print invitation.invite_link
        print mail_subject 
        print mail_content

    def test_invite_not_tribe_member(self):
        """
        邀请一个还不是部落成员的用户
        邀请链接:
        直接引导到不需要激活的注册流程 
        创建active用户之后加入邀请的权限组
        """
        user1 = self._sign_up_user('user1','user1@xuexibuluo.com','123456')
        invitation_target = user1.owned_tribe
        #user = User.objects.create_user('test','test@xuexibuluo.com','test')
        #email = 'othertest@xuexibuluo.com'
        #invitation_target = user.owned_tribe
        #invitation = Invitation.objects.invite(user,email,invitation_target)
        #self.assertNotEquals(invitation,None)

    def test_invite_inactive_tribe_member(self):
        """
        邀请一个没有激活的用户,
        邀请链接具备激活的效用直接激活,
        因为激活的本意就是要验证邮箱的正确性
        激活之后加入邀请的权限组
        """
        #user = User.objects.create_user('test','test@xuexibuluo.com','test')
        #email = 'othertest@xuexibuluo.com'
        #invitation_target = user.owned_tribe
        #invitation = Invitation.objects.invite(user,email,invitation_target)
        #self.assertNotEquals(invitation,None)

    def test_accept_invitation(self):
        """
        Test accept invite
        """

class InvitationRestAPITest(TestCase):

    def test_invite(self):
        """
        Test invite
        """
        inviations = Invitation.objects.all()

    def test_accept(self):
        """
        Test accept invite
        """


