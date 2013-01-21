# coding: utf-8
from django.contrib.auth.models import Group

class AdminAuthGroupMixin(object):
    """
    提供管理权限组的相关方法的mixin
    使用这个mixin的类需要提供:
    def get_admin_auth_group_name(self):
    这个方法.
    """
    def get_admin_auth_group(self):
        return Group.objects.get(name=self.get_admin_auth_group_name())

    def add_user_to_admin_group(self,user):
        """
        让用户成为管理员,即加入该用户到这个对象的管理员权限组
        """
        admin_auth_group = self.get_admin_auth_group()
        admin_auth_group.user_set.add(user)

    def get_admins(self):
        """
        return a queryset include  all users has admin permissions
        """
        return self.get_admin_auth_group().user_set.all()

class OwnerAuthGroupMixin(object):
    """
    提供管理权限组的相关方法的mixin
    使用这个mixin的类需要提供:
    def get_owner_auth_group_name(self):
    这个方法.
    """
    def get_owner_auth_group(self):
        return Group.objects.get(name=self.get_owner_auth_group_name())

    def add_user_to_owner_group(self,user):
        """
        让用户成为该对象的拥有者,即加入该用户到对象的拥有者权限组
        """
        tribe_owner_auth_group = self.get_owner_auth_group()
        tribe_owner_auth_group.user_set.add(user) 

    def get_owners(self):
        """
        return a queryset include all users has owner permissions
        """
        return self.get_owner_auth_group().user_set.all()
   
class MemberAuthGroupMixin(object):
    """
    提供成员权限组的相关方法的mixin
    使用这个mixin的类需要提供:
    def get_member_auth_group_name(self):
    这个方法.
    """

    def get_member_auth_group(self):
        return Group.objects.get(name=self.get_member_auth_group_name())

    def add_user_to_member_group(self,user):
        """
        让用户成为该对象的成员,即加入该用户到这个对象的成员权限组
        """
        tribe_member_auth_group = self.get_member_auth_group()
        tribe_member_auth_group.user_set.add(user) 

    def get_members(self):
        """
        return a queryset include  all users has member permissions
        """
        return self.get_member_auth_group().user_set.all()

