# coding: utf-8
from django.utils.translation import ugettext as _
from django.core.mail import send_mail as send_mail_func
from django.template.loader import render_to_string
from django import forms
from django.conf import settings
from studytribe.studygroup.models import StudyTribe,StudyGroup,StudentStudyLog
from django.contrib.auth.models import User,Group,Permission
from studytribe.studygroup.models import (HOMEWORK_EVALUATE_CHOICES,
                                          DISCIPLINE_EVALUATE_CHOICES)  
from django.core.mail import EmailMultiAlternatives

class StudyGroupForm(forms.Form):
    tribe_id = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(label="班级名称")
    description = forms.CharField(widget=forms.Textarea(
                                         attrs={'placeholder':_(u"班级描述")}),
                                         label="班级描述")

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

    def clean_name(self):
        name = self.cleaned_data['name']
        tribe_id = self.cleaned_data['tribe_id']
        tribe = StudyTribe.objects.get(pk=tribe_id)
        same_name_groups = tribe.study_groups.filter(name=name)
        if same_name_groups:
            raise forms.ValidationError(u"该学习部落中有一样名字的班级了,请另选名称。")
        return name


class StudyGroupMemberForm(forms.Form):
    group_id = forms.CharField(widget=forms.HiddenInput())
    username = forms.CharField(widget=forms.TextInput(
                                         attrs={
                                             'placeholder':u"用户名"
                                             }),label=u"用户名")

    email = forms.EmailField(widget=forms.TextInput(
                                         attrs={
                                             'placeholder':_("Email")
                                             }),
                                         label=_("Email"))

    def clean(self):
        cleaned_data = super(StudyGroupMemberForm, self).clean()
        group_id = cleaned_data['group_id']
        if cleaned_data.has_key('username'):
            username = cleaned_data["username"]
            user = User.objects.filter(username=username)
            if user:
                print dir(self.fields['email'])
                #去掉email的必要输入的校验
                pass
            group = StudyGroup.objects.get(pk=group_id)
            same_name_users = group.members.filter(username=username)
            if same_name_users:
                msg = u"该用户%s已经加入到这个班级了。" % username
                self._errors["username"] = self.error_class([msg])
        return cleaned_data

    #def clean(self):
    #    """
    #    clean the form
    #    """
    #    cleaned_data = super(ResetPasswordForm, self).clean()
    #    self._validate_old_password(cleaned_data)
    #    self._validate_confirm_password(cleaned_data)
    #    return cleaned_data

    #def _validate_old_password(self,cleaned_data):
    #    old_password = cleaned_data.get('old_password')
    #    if old_password:
    #        userid = cleaned_data.get('userid')
    #        user = IntrendUser.objects.get(id=userid)
    #        if not user.check_password(old_password):
    #            msg = _(u"The old password is wrong.")
    #            self._errors["old_password"] = self.error_class([msg])


    #def _validate_confirm_password(self,cleaned_data):
    #    password = cleaned_data.get("new_password")
    #    confirm_password = cleaned_data.get("confirm_password")
    #    if not password == confirm_password:
    #        # We know these are not in self._errors now.
    #        msg = _(u"Password don't equals the ConfirmPassword.")
    #        self._errors["confirm_password"] = self.error_class([msg])

    def save(self,group):
        """
        create a normal user to a group
        用户已经存在,但不在班级中,加入班级;
        用户不存在,创建用户为没有激活状态,并生成激活码,加入班级;
        用户已经存在并在班级中提示用户;
        """
        username,email = (self.cleaned_data['username'],
                                   self.cleaned_data['email'])
        user = None
        try:
            user = User.objects.get(username=username)
        except Exception, e:
            #user not exist
            print 'user not exist!'
            user = User.objects.create_user(username,email,'')
            user.is_active = False
            user.save()
        print 'user is activate:',user.is_active
        group.add_member(user)
        

class StudentStudyLogForm(forms.Form):
    """
    学生的教学日志,每日一评
    """
    teach_date = forms.DateField(widget=forms.TextInput(
                                         attrs={
                                             'id':u"datepicker",
                                             'placeholder':u"教学时间"
                                             }),label=u"教学时间")

    attend_time = forms.TimeField(widget=forms.TextInput(
                                         attrs={
                                             'id':u"attend-timepicker",
                                             'placeholder':u"到达时间"
                                             }),label=u"到达时间")

    home_work_desc = forms.CharField(widget=forms.Textarea(
                                            attrs={'placeholder':_(u"家庭作业")}),
                                            label=u"家庭作业")

    knowledge_essential = forms.CharField(label=u"知识要点")
    after_school_reading = forms.CharField(label=u"课外阅读")
    after_school_video = forms.CharField(label=u"课外中英文视频")
    homework_evaluate = forms.ChoiceField(label=u"作业完成情况",
                                          choices=HOMEWORK_EVALUATE_CHOICES)
    discipline_evaluate = forms.ChoiceField(label=u"纪律情况",
                                          choices=DISCIPLINE_EVALUATE_CHOICES)
    handcraft = forms.CharField(label=u"手工制作")
    overall_remark = forms.CharField(widget=forms.Textarea(
                                            attrs={'placeholder':_(u"总体评价")}),
                                            label=u"总体评价")
    send_email = forms.BooleanField(widget=forms.CheckboxInput(),
                                           label=u"同时发送电子邮件",
                                           initial=True,
                                           required=False)

    def send_studylog_mail(self,student,studylog,logger):
        ctx_dict = {'student':student,'study_log':studylog}
        subject = render_to_string(
                        'studytribe/studygroup/emails/study_log_email_subject.txt',
                        ctx_dict)
        txt_message = render_to_string(
                        'studytribe/studygroup/emails/study_log_email.txt',
                        ctx_dict)
        html_message = render_to_string(
                        'studytribe/studygroup/emails/study_log_email.html',
                        ctx_dict)
        email_sender = EmailMultiAlternatives(u"每日学习日志",
                                              txt_message,
                                              settings.DEFAULT_FROM_EMAIL,
                                              [student.email])
        email_sender.attach_alternative(html_message, "text/html")  
        email_sender.send(True)




    def save_log_sendmail(self,student,study_group,logger):
        """
        保存教学日志,同时根据情况发送邮件
        """
        (teach_date,attend_time,home_work_desc,
         knowledge_essential,after_school_reading,
         after_school_video,homework_evaluate,
         discipline_evaluate,handcraft,
         overall_remark,send_email,
        ) = (self.cleaned_data['teach_date'],
             self.cleaned_data['attend_time'],
             self.cleaned_data['home_work_desc'],
             self.cleaned_data['knowledge_essential'],
             self.cleaned_data['after_school_reading'],
             self.cleaned_data['after_school_video'],
             self.cleaned_data['homework_evaluate'],
             self.cleaned_data['discipline_evaluate'],
             self.cleaned_data['handcraft'],
             self.cleaned_data['overall_remark'],
             self.cleaned_data['send_email'])
        
        log = StudentStudyLog.objects.filter(
                                       student=student,
                                       study_group=study_group,
                                       teach_date=teach_date)
        if log:
            log = log[0]
            log.logger=logger
            log.teach_date=teach_date
            log.attend_time=attend_time
            log.home_work_desc=home_work_desc
            log.knowledge_essential=knowledge_essential
            log.after_school_reading=after_school_reading
            log.after_school_video=after_school_video
            log.homework_evaluate=homework_evaluate
            log.discipline_evaluate=discipline_evaluate
            log.handcraft=handcraft
            log.overall_remark=overall_remark
            log.save()
        else:
            log = StudentStudyLog.objects.create(
                                       student=student,
                                       study_group=study_group,
                                       logger=logger,
                                       teach_date=teach_date,
                                       attend_time=attend_time,
                                       home_work_desc=home_work_desc,
                                       knowledge_essential=knowledge_essential,
                                       after_school_reading=after_school_reading,
                                       after_school_video=after_school_video,
                                       homework_evaluate=homework_evaluate,
                                       discipline_evaluate=discipline_evaluate,
                                       handcraft=handcraft,
                                       overall_remark=overall_remark
                                       )
        if send_email:
            self.send_studylog_mail(student,log,logger)
        return log


