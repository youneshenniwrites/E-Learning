from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from ..models import Subject, Course
from .serializers import SubjectSerializer, CourseSerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API viewset to both list objects
    and retrieve a single objects
    '''
    
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseEnrollView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        course.users.add(request.user)
        return Response({'enrolled': True})


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
