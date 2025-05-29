from django.db import models
from django.conf import settings
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex


class LibraryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Library Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class ResourceType(models.TextChoices):
    EBOOK = 'ebook', 'eBook'
    REVISION = 'revision', 'Revision Material'
    NOTES = 'notes', 'Class Notes'
    PAST_PAPER = 'past_paper', 'Past Paper'
    SYLLABUS = 'syllabus', 'Syllabus'
    VIDEO = 'video', 'Video'
    AUDIO = 'audio', 'Audio'


class LibraryItem(models.Model):
    category = models.ForeignKey(LibraryCategory, on_delete=models.SET_NULL, null=True, related_name='items')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=20, choices=ResourceType.choices, default=ResourceType.EBOOK)
    file = models.FileField(upload_to='library_files/')
    thumbnail = models.ImageField(upload_to='library_thumbnails/', null=True, blank=True)
    preview_text = models.TextField(blank=True, null=True, help_text='Short description or preview of the content')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='uploaded_library_items')
    upload_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # Analytics counters
    download_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)

    # Virus scanning metadata
    virus_scan_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('clean', 'Clean'), ('infected', 'Infected')],
        default='pending',
        help_text='Status of virus scan on the file'
    )
    virus_scan_report = models.TextField(blank=True, null=True, help_text='Details or report from virus scan')

    # PDF content full-text search vector (requires Postgres)
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        ordering = ['-upload_date']
        indexes = [
            GinIndex(fields=['search_vector']),
        ]

    def __str__(self):
        return self.title


class BookmarkedItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    item = models.ForeignKey(LibraryItem, on_delete=models.CASCADE, related_name='bookmarked_by')
    bookmarked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')
        ordering = ['-bookmarked_at']

    def __str__(self):
        return f"{self.user} bookmarked {self.item}"


class DownloadLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(LibraryItem, on_delete=models.CASCADE, related_name='download_logs')
    download_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-download_date']

    def __str__(self):
        return f"Download of {self.item} by {self.user} on {self.download_date}"


class ViewLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(LibraryItem, on_delete=models.CASCADE, related_name='view_logs')
    view_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-view_date']

    def __str__(self):
        return f"View of {self.item} by {self.user or 'anonymous'} on {self.view_date}"
