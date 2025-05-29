from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LibraryCategoryViewSet,
    LibraryItemViewSet,
    BookmarkedItemViewSet,
    DownloadLogViewSet,
    ViewLogViewSet,
)

router = DefaultRouter()
router.register(r'categories', LibraryCategoryViewSet, basename='librarycategory')
router.register(r'items', LibraryItemViewSet, basename='libraryitem')
router.register(r'bookmarks', BookmarkedItemViewSet, basename='bookmarkeditem')
router.register(r'downloads', DownloadLogViewSet, basename='downloadlog')
router.register(r'views', ViewLogViewSet, basename='viewlog')

urlpatterns = [
    path('', include(router.urls)),
]
