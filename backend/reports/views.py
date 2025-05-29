from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Report
from .serializers import ReportSerializer

# Custom permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow only the creator to edit; read for anyone authenticated.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user

class IsReportOwnerOrAdmin(permissions.BasePermission):
    """
    Allow editing if admin or report creator.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.created_by == request.user

class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Allow access if user is teacher or admin.
    """
    def has_permission(self, request, view):
        return request.user.is_staff or getattr(request.user, 'role', '') == 'teacher'

class IsParentOrAdmin(permissions.BasePermission):
    """
    Allow access if user is parent or admin.
    """
    def has_permission(self, request, view):
        return request.user.is_staff or getattr(request.user, 'role', '') == 'parent'


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'term', 'class_name']
    search_fields = ['term', 'class_name', 'overall_grade']
    ordering_fields = ['created_at', 'term', 'class_name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Read permissions
            user_role = getattr(self.request.user, 'role', None)
            if self.request.user.is_staff:
                permission_classes = [permissions.IsAdminUser]
            elif user_role == 'teacher':
                permission_classes = [IsTeacherOrAdmin]
            elif user_role == 'parent':
                permission_classes = [IsParentOrAdmin]
            else:
                permission_classes = [permissions.IsAuthenticated]
        else:
            # Write permissions only for owner or admin
            permission_classes = [IsReportOwnerOrAdmin]

        return [perm() for perm in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Report.objects.all().order_by('-created_at')

        user_role = getattr(user, 'role', None)

        if user_role == 'teacher':
            # Assuming teacher has a related field `assigned_students`
            return Report.objects.filter(student__in=user.assigned_students.all()).order_by('-created_at')

        if user_role == 'parent':
            # Assuming parent has related children
            return Report.objects.filter(student__in=user.children.all()).order_by('-created_at')

        # Default to reports created by the user
        return Report.objects.filter(created_by=user).order_by('-created_at')
