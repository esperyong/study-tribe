# -*- coding:utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from studytribe.studygroup.forms import StudentStudyLogForm
from studytribe.studygroup.models import StudyTribe,StudyGroup,StudentStudyLog

class StudyGroupViewTest(TestCase):
    def test_get_group_list_view(self):
        """
        测试获取班级列表View
        """
        response = self.client.get(
                    reverse('study-group-list',
                         kwargs=
                         {'tribe_id':'1'})
                   )

class StudentStudyLogFormTest(TestCase):
    def test_studylog_form(self):
        student = User.objects.create_user('liuyong','liuyong@gmail.com','123')
        logger = User.objects.create_user('guanqing','guanqing@gmail.com','123')
        study_tribe = StudyTribe.objects.user_create_tribe(logger)
        study_group = StudyGroup.objects.create(tribe=study_tribe,
                                                name=u'小二班',
                                                created_by=logger,
                                                description=u'铭铭的班级',
                                                )
        params = {
                   'teach_date':'2013-07-10',
                   'attend_time':'09:10',
                   'home_work_desc':u'考语文生词，跟读两单元瑞思英语课文',
                   'knowledge_essential':u'语文生词加强练习和字体的规范',
                   'after_school_reading':'少年儿童大百科',
                   'after_school_video':'每周看一到两次',
                   'homework_evaluate':'A',
                   'discipline_evaluate':'B',
                   'handcraft':u'试验做纸',
                   'overall_remark':u'铭铭今天先完成学校语文卷子,现在的语文。',
                   'send_email':'true',
                   }
        form = StudentStudyLogForm(params)
        self.assertTrue(form.is_valid())
        log = form.save_or_update(student,study_group,logger)
        self.assertIsNotNone(log)
        logs = StudentStudyLog.objects.filter(attend_time='09:10')
        self.assertEquals(len(logs),1)
        #self.assertNotNull(log)


