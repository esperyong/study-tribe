# coding: utf-8
from django.db import models
from django.contrib.auth.models import User,Group,Permission
from userena.signals import activation_complete
from django.dispatch import receiver
from guardian.shortcuts import assign as assign_perm
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

TRIBE_OWNER_NAME_PATTERN='tribe_owner:%d'
TRIBE_ADMIN_NAME_PATTERN='tribe_admin:%d'
TRIBE_MEMBER_NAME_PATTERN='tribe_member:%d'
GROUP_ADMIN_NAME_PATTERN='group_admin:%d' 
GROUP_MEMBER_NAME_PATTERN='group_member:%d' 

class StudyTribeManager(models.Manager):

    def user_create_tribe(self,user):
        try:
            owned_tribe = user.created_tribe
        except StudyTribe.DoesNotExist, e:
            owned_tribe = StudyTribe.objects.create(
                                            created_by=user,
                                            name=(u"%s的学习部落" % user.username))

            owned_auth_group = Group.objects.create(
                                      name=owned_tribe.get_owner_auth_group_name())
            owned_tribe.assign_owner_perms(owned_auth_group)

            admin_auth_group = Group.objects.create(
                                      name=owned_tribe.get_admin_auth_group_name())
            owned_tribe.assign_admin_perms(admin_auth_group)

            member_auth_group = Group.objects.create(
                                      name=owned_tribe.get_member_auth_group_name())
            owned_tribe.assign_member_perms(member_auth_group)

            user.groups.add(owned_auth_group) 
        return owned_tribe


class StudyTribe(models.Model):
    """
    学习部落
    """
    name = models.CharField(max_length=100)
    created_by = models.OneToOneField(User,related_name='created_tribe')
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    objects = StudyTribeManager()

    class Meta:
        permissions = (
          ('enter_studytribe', 'Can Enter Tribe.'),
          ('change_studytribe_grade', 'Can Change Tribe Grade,Upgrade or Downgrade.'),
        )
        verbose_name = _('StudyTribe') 

    def create_study_group(self,name):
        """
        You must use this method to create study group,not use StudyGroup.objects.create
        method
        """
        study_group = StudyGroup.objects.create(tribe=self,name=name)
        return study_group

    def __unicode__(self):
        return _('study tribe %(name)s,owner is %(username)s.') % {
            'username': self.owner.username,
            'name': self.name,
        }

    @models.permalink
    def get_absolute_url(self):
        return ('study_tribe_detail',(),{'study_tribe_id':str(self.id)})

    def get_owner_auth_group_name(self):
        return TRIBE_OWNER_NAME_PATTERN % self.id

    def get_admin_auth_group_name(self):
        return TRIBE_ADMIN_NAME_PATTERN % self.id

    def get_member_auth_group_name(self):
        return TRIBE_MEMBER_NAME_PATTERN % self.id

    def get_owner_auth_group(self):
        return Group.objects.get(name=self.get_owner_auth_group_name())

    def get_admin_auth_group(self):
        return Group.objects.get(name=self.get_admin_auth_group_name())

    def get_member_auth_group(self):
        return Group.objects.get(name=self.get_member_auth_group_name())

    def add_user_to_owner_group(self,user):
        """
        让用户成为该学习部落的拥有者,即加入该用户到这个部落的拥有者权限组
        """
        tribe_owner_auth_group = self.get_owner_auth_group()
        tribe_owner_auth_group.user_set.add(user) 

    def add_user_to_admin_group(self,user):
        """
        让用户成为该学习部落的管理员,即加入该用户到这个部落的管理员权限组
        """
        tribe_admin_auth_group = self.get_admin_auth_group()
        tribe_admin_auth_group.user_set.add(user)
            
    def add_user_to_member_group(self,user):
        """
        让用户成为该学习部落的成员,即加入该用户到这个部落的成员权限组
        """
        tribe_member_auth_group = self.get_member_auth_group()
        tribe_member_auth_group.user_set.add(user) 

    def get_owners(self):
        """
        return a queryset include all users has owner permissions
        """
        return self.get_tribe_owner_auth_group().user_set.all()

    def get_admins(self):
        """
        return a queryset include  all users has admin permissions
        """
        return self.get_tribe_admin_auth_group().user_set.all()

    def get_members(self):
        """
        return a queryset include  all users has member permissions
        """
        return self.get_tribe_member_auth_group().user_set.all()

    def assign_owner_perms(self,user_or_group):
        group = user_or_group 
        assign_perm('studygroup.enter_studytribe',user_or_group,self)
        assign_perm('studygroup.delete_studytribe',user_or_group,self)
        assign_perm('studygroup.change_studytribe',user_or_group,self)
        assign_perm('studygroup.change_studytribe_grade',user_or_group,self)

    def assign_admin_perms(self,user_or_group):
        assign_perm('studygroup.enter_studytribe',user_or_group,self)
        assign_perm('studygroup.delete_studytribe',user_or_group,self)
        assign_perm('studygroup.change_studytribe',user_or_group,self)

    def assign_member_perms(self,user_or_group):
        assign_perm('studygroup.enter_studytribe',user_or_group,self)


@receiver(activation_complete)
def after_activation_complete_will_happen(sender,**kwargs):
    user = kwargs['user']
    StudyTribe.objects.user_create_tribe(user)

class StudyGroup(models.Model):
    """
    班级
    """
    tribe = models.ForeignKey(StudyTribe,related_name='study_groups')
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    class Meta:
        permissions = (
            ('enter_studygroup','enter StudyGroup'),
        )
        verbose_name = _('StudyGroup') 

    def __unicode__(self):
        return _('study group %(name)s,tribe is %(tribename)s.') % {
            'tribename': self.tribe.name,
            'name': self.name,
        }

    @models.permalink
    def get_absolute_url(self):
        return ('study_group_detail',(),
                {'study_tribe_id':str(self.tribe.id),
                 'study_group_id':str(self.id)}
                )

@receiver(post_save,sender=StudyGroup)
def after_study_group_create(sender, instance, created, **kwargs):
    if created:
        study_group = instance
        study_group_admin_group = Group.objects.create(
                                    name=GROUP_ADMIN_NAME_PATTERN % study_group.id)
        study_group_member_group = Group.objects.create(
                                    name=GROUP_MEMBER_NAME_PATTERN % study_group.id)

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
