# -*- coding:utf-8 -*-
from studytribe.studygroup import models
from studytribe.studygroup import serializers
from rest_framework import mixins
from rest_framework import generics
from studytribe.studygroup.permissions import IsOwnerOrReadOnly
from rest_framework import permissions

#for template dev
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def study_group_list(request):
    context = {}
    return render_to_response("studytribe/studygroup/base.html",
                              context,
                              context_instance=RequestContext(request))
"""
StudyTribe:学习部落
"""
class StudyTribeListRes(generics.ListCreateAPIView):
    template_name = "studytribe/studygroup/base.html"
    model = models.StudyTribe
    serializer_class = serializers.StudyTribeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          )

class StudyTribeRes(generics.RetrieveAPIView):
    model = models.StudyTribe
    serializer_class = serializers.StudyTribeSerializer

"""
StudyGroup:班级
"""
class StudyGroupListRes(generics.ListCreateAPIView):
    """
    List all studygroup,or create a new studygroup
    """
    model = models.StudyGroup
    serializer_class = serializers.StudyGroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    def pre_save(self, obj):
        obj.tribe = models.StudyTribe.objects.get(pk=self.kwargs['tribe_id'])

class StudyGroupRes(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve,update or delete a studygroup
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    model = models.StudyGroup
    serializer_class = serializers.StudyGroupSerializer



