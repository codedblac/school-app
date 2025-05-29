from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import SchoolAnalytics
from .serializers import SchoolAnalyticsSerializer

class AnalyticsDetailView(generics.RetrieveAPIView):
    """
    Retrieve analytics data for the logged-in user's school.
    Access restricted to authenticated users only.
    """
    serializer_class = SchoolAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, _created = SchoolAnalytics.objects.get_or_create(school=self.request.user)
        return obj
