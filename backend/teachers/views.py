from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Teacher
from .serializers import TeacherSerializer
from rest_framework.permissions import IsAuthenticated

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]