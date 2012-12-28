# coding: utf-8

from django.test import TestCase
from bs4 import BeautifulSoup
from captcha.models import CaptchaStore,get_safe_now
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class SignupTest(TestCase):
    def setUp(self):
        pass

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
            f.tribeowner拥有:enter_tribe,remove_tribe权限
            g.tribeowner拥有:endter_tribe权限
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
        #向register发送POST请求获取hashkey_from_page,在数据库中查出challenge
        #然后用这个表单POST,应该成功创建出一个没有激活的帐户
         data = {
                'first_name':'someone',
                'email':'someone@introns.cn',
                'password':'123456',
                'confirm_password':'123456',
                'username':'someone',
                'captcha_0':'sdjslf',
                'captcha_1':'XJMD',
                }
        response = self.client.post(reverse('studytribe_sign_main',args=['signup']),data)
        self.assertRaises(Exception, 
                          IntrendUser.objects.get,
                         {'first_name':'someone'})
        pass

    def test_signin(self):
        
        pass

