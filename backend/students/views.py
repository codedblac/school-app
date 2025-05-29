from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Student
from .serializers import StudentSerializer

class IsParentOrStaff(permissions.BasePermission):
    """
    Custom permission:
    - Parents can only view students linked to them
    - Staff and admin can view all
    """

    def has_permission(self, request, view):
        # Allow access only to authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Staff/admin have full access
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Parents can only access their children
        if hasattr(request.user, 'role') and request.user.role == 'parent':
            return obj.parents.filter(id=request.user.id).exists()

        # Default deny
        return False


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().select_related('user', 'current_class', 'stream').prefetch_related('parents')
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsParentOrStaff]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['admission_number', 'current_class', 'stream']
    search_fields = ['admission_number', 'user__first_name', 'user__last_name']
    ordering_fields = ['admission_number', 'user__first_name']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return self.queryset.order_by('admission_number')

        if hasattr(user, 'role') and user.role == 'parent':
            # Return only students linked to this parent
            return self.queryset.filter(parents=user).order_by('admission_number')

        # Other users have no access by default
        return Student.objects.none()
