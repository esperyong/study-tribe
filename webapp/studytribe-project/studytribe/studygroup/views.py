# -*- coding:utf-8 -*-
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from studytribe.studygroup.models import StudyGroup
from studytribe.studygroup.serializers import StudyGroupSerializer

@api_view(['GET', 'POST'])
def studygroup_list(request,format=None):
    """
    List all code studygroup,or create a new studygroup
    """
    if request.method == 'GET':
        groups = StudyGroup.objects.all()
        serializer = StudyGroupSerializer(instance=groups)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudyGroupSerializer(request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT','DELETE'])
def studygroup_detail(request,pk,format=None):
    """
    Retrieve,update or delete a studygroup
    """
    try:
        studygroup = StudyGroup.objects.get(pk=pk)
    except StudyGroup.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudyGroupSerializer(instance=studygroup)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StudyGroupSerializer(request.DATA,instance=studygroup)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        studygroup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

