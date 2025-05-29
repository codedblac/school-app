from django.urls import path
from .views import AnalyticsDetailView

app_name = 'analytics'

urlpatterns = [
    path('my-analytics/', AnalyticsDetailView.as_view(), name='my-analytics'),
]
