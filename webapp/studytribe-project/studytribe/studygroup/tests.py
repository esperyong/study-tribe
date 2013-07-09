# -*- coding:utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse

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



