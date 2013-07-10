# coding: utf-8
from django.utils.translation import ugettext as _
from django import forms
from django.conf import settings
from studytribe.studygroup.models import StudyGroup
from django.contrib.auth.models import User,Group,Permission

class StudyGroupForm(forms.Form):
    name = forms.CharField(label="班级名称")
    description = forms.CharField(label="班级描述")

    def save(self,user,tribe):
        """
        Create a new studygroup
        TODO write validation method for name unique
        """
        name,description = (self.cleaned_data['name'],
                            self.cleaned_data['description'])
        new_study_group = StudyGroup.objects.create(tribe=tribe,
                                                    name=name,
                                                    created_by=user,
                                                    description=description
                                                    )
        return new_study_group

class StudyGroupMemberForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
                                         attrs={
                                             'placeholder':u"用户名"
                                             }),label=u"用户名")

    nickname = forms.CharField(widget=forms.TextInput(
                                         attrs={
                                             'placeholder':u"昵称"
                                             }),label=u"昵称")

    email = forms.EmailField(widget=forms.TextInput(
                                         attrs={
                                             'placeholder':_("Email")
                                             }),
                                         label=_("Email"))

    def save(self,group):
        """
        create a normal user to a group
        用户已经存在,但不在班级中,加入班级;
        用户不存在,创建用户为没有激活状态,并生成激活码,加入班级;
        用户已经存在并在班级中为错误情况,TODO form validate;
        """
        username,nickname,email = (self.cleaned_data['username'],
                                   self.cleaned_data['nickname'],
                                   self.cleaned_data['email'])
        user = None
        try:
            user = User.objects.get(username=username)
        except Exception, e:
            #user not exist
            print 'user not exist!'
            user = User.objects.create_user(username,email,'')
            user.first_name = nickname
            user.is_active = False
            user.save()
        print 'user is activate:',user.is_active
        group.add_member(user)
        


