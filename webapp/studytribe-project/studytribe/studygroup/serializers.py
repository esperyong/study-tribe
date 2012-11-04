# coding: utf-8
from studytribe.studygroup import models
from rest_framework import serializers
from rest_framework import fields
from django.forms import widgets


class StudyTribeSerializer(serializers.ModelSerializer):
    groups = fields.ManyPrimaryKeyRelatedField()
    class Meta:
        model = models.StudyTribe
        fields = ('id','name','groups')

class StudyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudyGroup
        fields = ('id','name')


