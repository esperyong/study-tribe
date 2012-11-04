# -*- coding:utf-8 -*-
from studytribe.studygroup.models import StudyGroup
from studytribe.studygroup.serializers import StudyGroupSerializer
from rest_framework import mixins
from rest_framework import generics

class StudyGroupListRes(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.MultipleObjectAPIView):
    """
    List all studygroup,or create a new studygroup
    """

    model = StudyGroup
    serializer_class = StudyGroupSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,format=None):
        return self.create(request,*args,**kwargs)

    
class StudyGroupRes(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.SingleObjectAPIView):
    """
    Retrieve,update or delete a studygroup
    """
    model = StudyGroup
    serializer_class = StudyGroupSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



