# -*- coding:utf-8 -*-
from rest_framework import status
from rest_framework.response import Response
from studytribe.studygroup.models import StudyGroup
from studytribe.studygroup.serializers import StudyGroupSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from django.http import Http404

class StudyGroupListRes(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.MultipleObjectAPIView):
    model = StudyGroup
    serializer_class = StudyGroupSerializer
    """
    List all studygroup,or create a new studygroup
    """
    def get(self,request,format=None):
        groups = StudyGroup.objects.all()
        serializer = StudyGroupSerializer(instance=groups)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer = StudyGroupSerializer(request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    
class StudyGroupRes(APIView):
    """
    Retrieve,update or delete a studygroup
    """
    def get_object(self,pk):
        try:
            return StudyGroup.objects.get(pk=pk)
        except StudyGroup.DoesNotExist:
            return Http404

    def get(self,request,pk,format=None):
        studygroup = self.get_object(pk)
        serializer = StudyGroupSerializer(instance=studygroup)
        return Response(serializer.data)

    def put(self,request,pk,format=None):
        studygroup = self.get_object(pk)
        serializer = StudyGroupSerializer(request.DATA,instance=studygroup)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        studygroup = self.get_object(pk)
        studygroup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



