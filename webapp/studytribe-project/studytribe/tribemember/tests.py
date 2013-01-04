# coding: utf-8

from django.test import TestCase
from bs4 import BeautifulSoup
from captcha.models import CaptchaStore,get_safe_now
from django.contrib.auth.models import User,Group,Permission
from django.core.urlresolvers import reverse
from django.core import mail
from django.conf import settings
from userena.models import UserenaSignup
from studytribe.studygroup.models import StudyTribe
from userena import settings as userena_settings
import re
from guardian.shortcuts import assign as assign_perm
from guardian.shortcuts import get_perms,get_objects_for_user


class SignupTest(TestCase):
    def setUp(self):
        UserenaSignup.objects.check_permissions()

    def teardown(self):
        pass

    def test_signup(self):
        """
        测试整个signup流程,大致的流程如下,边界测试写在代码中:
          1.获得登陆界面,按照上面的action发出post请求,应该返回register界面;
          2.按照register界面的action发出post;
          3.从数据库中能够获取到User并且is_activate标记为False(尚未激活);
          4.从邮件中取出激活邮件,从中获取到激活码链接,发送激活请求;
          5.激活成功后:
            a.从数据库取出User应该为激活状态,is_activate=True
            b.user应该有一个拥有的StudyTribe
            c.应该有三个权限组:tribeowner,tribeadmin,tribemember
            d.user属于这个tribe的tribeowner组
            e.tribeowner拥有:enter_tribe,remove_tribe,change_tribe_grade权限
            f.tribeadmin拥有:enter_tribe,remove_tribe权限
            g.tribemember拥有:enter_tribe权限
            f.跳转到选择tribe的界面中
          6.激活失败后显示失败界面
        """
        #随便选了input和对应的验证数,应该会抛出异常
        hashkey_from_page = 'scls'
        input_captcha = 'ss'
        self.assertRaises(Exception, 
                          CaptchaStore.objects.get,
                         {'response':input_captcha,
                          'hashkey':hashkey_from_page,
                          'expiration__gt':get_safe_now()})
        data = {
                'username':'someone',
                'email':'someone@introns.cn',
                'password1':'123456',
                'password2':'123456',
                'captcha_0':'sdjslf',
                'captcha_1':'XJMD',
                }
        response = self.client.post(reverse('studytribe_sign_main',args=['signup']),data)
        #发送的captcha_0不对,创建不了用户
        self.assertRaises(Exception, 
                          User.objects.get,
                         {'username':'someone'})
        #向register发送POST请求获取hashkey_from_page,在数据库中查出challenge
        #然后用这个表单POST,应该成功创建出一个没有激活的帐户
        soup = BeautifulSoup(response.content)
        ne = soup.find('input',{'id':'id_captcha_0'})
        hashkey_from_page = ne['value']
        csobj = CaptchaStore.objects.get(hashkey=hashkey_from_page)
        input_captcha = csobj.challenge
        data['captcha_0'] = hashkey_from_page
        data['captcha_1'] = input_captcha
        response = self.client.post(reverse('studytribe_sign_main',args=['signup']),data)
        user = User.objects.get(username='someone')
        self.assertTrue(user is not None)
        self.assertFalse(user.is_active)
        self.assertEquals(len(mail.outbox),1)
        #但此时还没有owned_tribe,激活后才有
        self.assertEquals(len(StudyTribe.objects.all()),0)
        #开始激活
        mail_content = mail.outbox[0].body
        match = re.search('activate/(.*)/' , mail_content)
        activation_key = match.group(1)
        c = self.client
        #用一个错误的激活码
        response = c.get(reverse('userena_activate',
                         kwargs={'activation_key':'sselsjdfkjl'}))
        self.assertFalse(User.objects.get(username__exact='someone').is_active,
                         msg = "After user been activated by a wrong activate_key,the user's is_active property should equals False.")
        #验证失败返回激活失败界面
        self.assertTemplateUsed(response,
                                settings.USER_ACTIVATE_FAIL_TEMPLATE)
        #try the correct activation_key
        response = c.get(reverse('userena_activate',
                         kwargs={'activation_key' : activation_key}))
        self.assertTrue(User.objects.get(username__exact='someone').is_active,
                        msg = "After user been activated,the user's is_active property should equals True.")
        #验证跳转到激活正确界面
        tribe_choose_url = (userena_settings.USERENA_SIGNIN_REDIRECT_URL %  
                            {'username':user.username})
        self.assertRedirects(response,tribe_choose_url)

        #验证权限begin
        user = User.objects.get(username__exact='someone')
        #if there have no tribe,will raise StudyTribe.DoesNotExist exception
        self.assertEquals(len(StudyTribe.objects.all()),1,
                          msg="After user been activated,the user's StudyTribe should be created.")
        permission_group = Group.objects.all()
        self.assertEquals(len(permission_group),3,
                         msg="After user been activated,three permission groups should be created.")

        towner = Group.objects.get(name="tribe_owner")
        tadmin = Group.objects.get(name="tribe_admin")
        tmember = Group.objects.get(name="tribe_member")
        owner_permissions = ['enter_tribe','remove_tribe','change_tribe_grade']
        admin_permissions = ['enter_tribe','remove_tribe']
        member_permissions = ['enter_tribe']

        owner_group_permissions = get_perms(towner,user.owned_tribe)
        self.assertEquals(len(owner_group_permissions),3)
        for perm_code in owner_group_permissions: 
            self.assertTrue(perm_code in owner_permissions)

        admin_group_permissions = get_perms(tadmin,user.owned_tribe)
        self.assertEquals(len(admin_group_permissions),2)
        for perm_code in admin_group_permissions: 
            self.assertTrue(perm_code in admin_permissions)

        member_group_permissions = get_perms(tmember,user.owned_tribe)
        self.assertEquals(len(member_group_permissions),1)
        for perm_code in member_group_permissions: 
            self.assertTrue(perm_code in member_permissions)

        self.assertEquals(len(user.groups.all()),1)
        self.assertTrue(user.groups.all()[0].name == 'tribe_owner')

        tribe = user.owned_tribe
        self.assertTrue(user.has_perm('studygroup.enter_tribe',tribe))
        self.assertTrue(user.has_perm('studygroup.remove_tribe',tribe))
        self.assertTrue(user.has_perm('studygroup.change_tribe_grade',tribe))
        self.assertFalse(user.has_perm('studygroup.change_tribe_grade'))

        self.assertEquals(len(get_objects_for_user(user,'studygroup.enter_tribe')),1)
        #验证权限end

    def test_signin(self):
        pass










