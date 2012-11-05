# coding: utf-8
from django.db import models

# Create your models here.

class StudyTribe(models.Model):
    """
    学习部落
    """
    name = models.CharField(max_length=100)


class StudyGroup(models.Model):
    """
    班级
    """
    tribe = models.ForeignKey(StudyTribe,related_name='groups')
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

class Topic(models.Model):
    """
    学习话题(讨论)
    """
    pass

class Comment(models.Model):
    """
    评论
    """
    pass
    
class Studyware(models.Model):
    """
    学习资料
    """
    pass

class AssignmentList(models.Model):
    """
    作业列表
    """
    pass

class Assignment(models.Model):
    """
    作业
    """
    pass

class Article(models.Model):
    """
    文章
    """
    pass

class Syllabus(models.Model):
    """
    教学大纲
    """
    pass

class SyllabusSchedule(models.Model):
    """
    课程表
    """
    pass
