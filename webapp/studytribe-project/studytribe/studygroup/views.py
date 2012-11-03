# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from studytribe.studygroup.models import StudyGroup
from studytribe.studygroup.serializers import StudyGroupSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def studygroup_list(request):
    """
    List all code studygroup,or create a new studygroup
    """
    if request.method == 'GET':
        groups = StudyGroup.objects.all()
        serializer = StudyGroupSerializer(instance=groups)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = StudyGroupSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data,status=201)
        else:
            return JSONResponse(serializer.errors,status=400)
    
def studygroup_detail(request,pk):
    """
    Retrieve,update or delete a studygroup
    """
    try:
        studygroup = StudyGroup.objects.get(pk=pk)
    except StudyGroup.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = StudyGroupSerializer(instance=studygroup)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = StudyGroupSerializer(data,instance=studygroup)
        if serializer.is_valid(): 
            serializer.save()
            return JSONResponse(serializer.data)
        else:
            return JSONResponse(serializer.errors,status=400)

    elif request.method == 'DELETE':
        studygroup.delete()
        return HttpResponse(status=204)

