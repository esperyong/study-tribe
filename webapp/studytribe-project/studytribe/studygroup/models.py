# coding: utf-8
from django.db import models
from django.contrib.auth.models import User,Group,Permission
from userena.signals import activation_complete
from django.dispatch import receiver
from guardian.shortcuts import assign as assign_perm

# Create your models here.

class StudyTribe(models.Model):
    """
    学习部落
    """
    name = models.CharField(max_length=100)
    owner = models.OneToOneField(User,related_name='owned_tribe')
    class Meta:
        permissions = (
          ('enter_tribe', 'Can Enter Tribe.'),
          ('remove_tribe', 'Can Remove Tribe.'),
          ('change_tribe_grade', 'Can Change Tribe Grade,Upgrade or Downgrade.'),
        )

@receiver(activation_complete)
def after_activation_complete_will_happen(sender,**kwargs):
    user = kwargs['user']
    owned_tribe = StudyTribe.objects.create(owner=user,name=(u"%s的学习部落" % user.username))

    tribe_owner_group = Group.objects.create(name='tribe_owner')
    assign_perm('studygroup.enter_tribe',tribe_owner_group,owned_tribe)
    assign_perm('studygroup.remove_tribe',tribe_owner_group,owned_tribe)
    assign_perm('studygroup.change_tribe_grade',tribe_owner_group,owned_tribe)

    tribe_admin_group = Group.objects.create(name='tribe_admin')
    assign_perm('studygroup.enter_tribe',tribe_admin_group,owned_tribe)
    assign_perm('studygroup.remove_tribe',tribe_admin_group,owned_tribe)

    tribe_member_group = Group.objects.create(name='tribe_member')
    assign_perm('studygroup.enter_tribe',tribe_member_group,owned_tribe)

    user.groups.add(tribe_owner_group) 

class StudyGroup(models.Model):
    """
    班级
    """
    tribe = models.ForeignKey(StudyTribe,related_name='groups')
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    class Meta:
        permissions = (
                ('remove_studygroup','Delete StudyGroup'),
        )

class Topic(models.Model):
    """
    学习话题(讨论)
    """
    study_group = models.ForeignKey(StudyTribe,related_name='topics')
    title = models.CharField(max_length=500)
    body = models.TextField(max_length=2000)

class Comment(models.Model):
    """
    评论
    """
    class Meta:
        abstract = True
    title = models.CharField(max_length=500)
    body = models.TextField(max_length=2000)

class TopicComment(Comment):
    """
    学习话题评论
    """
    topic = models.ForeignKey(Topic,related_name='comments')
    
class Studyware(models.Model):
    """
    学习资料
    """
    created = models.DateTimeField(auto_now_add=True)

class StudywareComment(Comment):
    """
    学习资料评论
    """
    studyware = models.ForeignKey(Studyware,related_name='comments')

class AssignmentList(models.Model):
    """
    作业列表
    """
    name = models.CharField(max_length=50) 

class Assignment(models.Model):
    """
    作业
    """
    alist = models.ForeignKey(AssignmentList,related_name='assignments')
    title = models.CharField(max_length=100) 
    content = models.CharField(max_length=500) 

class Article(models.Model):
    """
    文章
    """
    pass

class ArticleComment(Comment):
    """
    文章的评论
    """
    article = models.ForeignKey(Article,related_name='comments')

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
