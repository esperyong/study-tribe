# coding: utf-8
from studytribe.studygroup import models
from rest_framework import serializers
from django.forms import widgets

class StudyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudyGroup
        fields = ('id','name')


