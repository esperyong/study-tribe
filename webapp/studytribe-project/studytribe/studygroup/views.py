# -*- coding:utf-8 -*-
from studytribe.studygroup import models
from studytribe.studygroup import serializers
from rest_framework import mixins
from rest_framework import generics

class StudyTribeListRes(generics.ListAPIView):
    model = models.StudyTribe
    serializer_class = serializers.StudyTribeSerializer

class StudyTribeRes(generics.RetrieveAPIView):
    model = models.StudyTribe
    serializer_class = serializers.StudyTribeSerializer

class StudyGroupListRes(generics.ListCreateAPIView):
    """
    List all studygroup,or create a new studygroup
    """

    model = models.StudyGroup
    serializer_class = serializers.StudyGroupSerializer

class StudyGroupRes(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve,update or delete a studygroup
    """
    model = models.StudyGroup
    serializer_class = serializers.StudyGroupSerializer


