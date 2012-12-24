# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from userena.models import UserenaBaseProfile

class TribeMemberProfile(UserenaBaseProfile):
    user = models.OneToOneField(User)

def create_owned_profile(sender, instance, created, **kwargs):
    if created:
        profile = TribeMemberProfile.objects.create(user=instance)

post_save.connect(create_owned_profile, sender=User)

