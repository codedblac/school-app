from rest_framework import viewsets, permissions
from .models import SubjectCategory, Subject, ClassSubject
from .serializers import (
    SubjectCategorySerializer, SubjectSerializer, ClassSubjectSerializer
)


class SubjectCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubjectCategory.objects.all()
    serializer_class = SubjectCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClassSubjectViewSet(viewsets.ModelViewSet):
    queryset = ClassSubject.objects.select_related('subject', 'school_class', 'teacher').all()
    serializer_class = ClassSubjectSerializer
    permission_classes = [permissions.IsAuthenticated]
