from django.contrib import admin
from django.urls import path, include
from accounts.views import RegisterView, UserListView
from audit.views import AuditLogViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'audit-logs', AuditLogViewSet, basename='auditlog')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts
    path('api/accounts/register/', RegisterView.as_view(), name='register'),
    path('api/accounts/users/', UserListView.as_view(), name='user-list'),

    # Include app URLs with prefixes and namespaces
    path('api/academics/', include(('academics.urls', 'academics'), namespace='academics')),
    path('api/accounts/', include('accounts.urls')),
    path('api/ai-assist/', include(('ai_assist.urls', 'ai_assist'), namespace='ai_assist')),
    path('api/analytics/', include(('analytics.urls', 'analytics'), namespace='analytics')),
    path('api/classes/', include(('classes.urls', 'classes'), namespace='classes')),
    path('api/students/', include(('students.urls', 'students'), namespace='students')),
    path('api/teachers/', include(('teachers.urls', 'teachers'), namespace='teachers')),
    path('api/attendance/', include(('attendance.urls', 'attendance'), namespace='attendance')),
    path('api/communication/', include(('communication.urls', 'communication'), namespace='communication')),
    path('api/discipline/', include('discipline.urls')),
    path('api/elearning/', include('e_learning.urls')),
    path('api/events/', include('events.urls')),
    path('api/library/', include('library.urls')),
    path('api/medical/', include('medical.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/portal/', include('portal.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/finance/', include('finance.urls')),
    path('api/grading/', include('grades.urls')),
    path('api/timetable/', include('timetable.urls')),
    path('api/subjects/', include('subjects.urls')),
    



    # Router URLs under a dedicated prefix
    path('api/audit/', include((router.urls, 'audit'), namespace='audit')),
]
