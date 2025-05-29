from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import LibraryCategory, LibraryItem, BookmarkedItem, DownloadLog, ViewLog
from .serializers import (
    LibraryCategorySerializer,
    LibraryItemSerializer,
    BookmarkedItemSerializer,
    DownloadLogSerializer,
    ViewLogSerializer,
)

class LibraryCategoryViewSet(viewsets.ModelViewSet):
    queryset = LibraryCategory.objects.all()
    serializer_class = LibraryCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LibraryItemViewSet(viewsets.ModelViewSet):
    queryset = LibraryItem.objects.filter(is_active=True).select_related('category', 'uploaded_by')
    serializer_class = LibraryItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'resource_type']
    search_fields = ['title', 'description', 'preview_text']
    ordering_fields = ['upload_date', 'download_count', 'view_count']

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def bookmark(self, request, pk=None):
        item = self.get_object()
        bookmark, created = BookmarkedItem.objects.get_or_create(user=request.user, item=item)
        if created:
            return Response({'status': 'item bookmarked'})
        return Response({'status': 'already bookmarked'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def download(self, request, pk=None):
        item = self.get_object()
        ip = request.META.get('REMOTE_ADDR')
        DownloadLog.objects.create(user=request.user, item=item, ip_address=ip)
        # Increase download count atomically
        item.download_count = DownloadLog.objects.filter(item=item).count()
        item.save(update_fields=['download_count'])
        return Response({'status': 'download logged'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def view(self, request, pk=None):
        item = self.get_object()
        ip = request.META.get('REMOTE_ADDR')
        ViewLog.objects.create(user=request.user, item=item, ip_address=ip)
        # Increase view count atomically
        item.view_count = ViewLog.objects.filter(item=item).count()
        item.save(update_fields=['view_count'])
        return Response({'status': 'view logged'})

class BookmarkedItemViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkedItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BookmarkedItem.objects.filter(user=self.request.user).select_related('item')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DownloadLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DownloadLogSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = DownloadLog.objects.all().select_related('user', 'item')

class ViewLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ViewLogSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = ViewLog.objects.all().select_related('user', 'item')
