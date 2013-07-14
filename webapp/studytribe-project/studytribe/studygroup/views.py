# -*- coding:utf-8 -*-
from studytribe.studygroup import models
from studytribe.studygroup import serializers
from studytribe.studygroup import forms
from rest_framework import mixins
from rest_framework import generics
from studytribe.studygroup.permissions import IsOwnerOrReadOnly
from rest_framework import permissions


from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.models import User

#for template dev
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import loader,RequestContext
from django.views.decorators.csrf import csrf_protect
from guardian.decorators import permission_required
from django.http import HttpResponse,HttpResponseNotAllowed


def get_study_group_list(request,tribe_id,context): 
    study_tribe = get_object_or_404(models.StudyTribe, id__iexact=tribe_id)
    context['studygroup_list'] = models.StudyGroup.objects.filter(tribe=study_tribe)
    context['study_tribe'] = study_tribe
    return render_to_response("studytribe/studygroup/base.html",
                               context,
                               context_instance=RequestContext(request))



@permission_required('studygroup.enter_studytribe',
                     (models.StudyTribe,'id','tribe_id'))
def study_group_list(request,tribe_id):
    context = {}
    if request.method == 'GET':
        return get_study_group_list(request,tribe_id,context)
    if request.method == 'POST':
        form = forms.StudyGroupForm(request.POST)
        context['form'] = form
        if form.is_valid():
            #create a studygroup in database
            tribe = models.StudyTribe.objects.get(pk=tribe_id)
            studygroup = form.save(request.user,tribe)
            #fetch all study group in this tribe and render page to client
            return get_study_group_list(request,tribe_id,context)
        else:
            return render_to_response("studytribe/studygroup/create_group.html",
                                  context,
                                  context_instance=RequestContext(request))

@permission_required('studygroup.change_studytribe',
                     (models.StudyTribe,'id','tribe_id'))
def study_group_create_ui(request,tribe_id):
    context = {'form':forms.StudyGroupForm()}
    if request.method == 'GET':
        return render_to_response("studytribe/studygroup/create_group.html",
                                  context,
                                  context_instance=RequestContext(request))


def get_study_group_members_view():
    """
    获得班级成员界面
    """
    pass
    

def study_group_members(request,tribe_id,group_id):
    """
    班级成员主界面
    """
    context = {}
    context['form'] = None
    context['study_log_form'] = forms.StudentStudyLogForm()
    if request.method == 'GET':
        context['form'] = forms.StudyGroupMemberForm()
        context['group_id'] = group_id
        study_group = get_object_or_404(models.StudyGroup,pk=group_id)
    if request.method == 'POST':
        context['form'] = forms.StudyGroupMemberForm(request.POST)
        study_group = models.StudyGroup.objects.get(pk=group_id)
        if context['form'].is_valid():
            #save a student to tribe
            context['form'].save(study_group)
            context['form'] = forms.StudyGroupMemberForm()
        else:
            context['form_visible'] = True
    context['study_group'] = study_group
    return render_to_response("studytribe/studygroup/study_group_members.html",
                              context,
                              context_instance=RequestContext(request))

def student_study_log_input(request,group_id,member_id):
    context = {}
    if request.method == 'POST':
        context['study_log_form'] = forms.StudentStudyLogForm(request.POST)
        if context['study_log_form'].is_valid():
            #save a study log form and send a email to user
            study_group = models.StudyGroup.objects.get(pk=group_id)
            student = User.objects.get(pk=member_id)
            logger = request.user
            log = context['study_log_form'].save_log_sendmail(student,
                                                              study_group,
                                                              logger)
            return render_to_response("studytribe/studygroup/tparts/study_log_form.html",
                              context,
                              context_instance=RequestContext(request))
        else:
            return HttpResponse(loader.render_to_string(
                                 "studytribe/studygroup/tparts/study_log_form.html",
                                 context,
                                 context_instance=RequestContext(request)
                                ),status=400)
    else:
        return HttpResponseNotAllowed(['POST'])

def study_group_detail(request,study_tribe_id,study_group_id):
    context = {}
    return render_to_response("studytribe/studygroup/base.html",
                              context,
                              context_instance=RequestContext(request))

"""
write traditional view for quick and dirty
"""
class StudyGroupListView(ListView):

    context_object_name = "study_group_list"
    template_name = "studytribe/studygroup/studygroup_list.html"

    def get_queryset(self):
        study_tribe = get_object_or_404(Publisher, name__iexact=self.args[0])
        return StudyGroup.objects.filter(publisher=publisher)


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



