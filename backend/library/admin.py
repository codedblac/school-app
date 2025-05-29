from django.contrib import admin
from .models import LibraryCategory, LibraryItem, BookmarkedItem, DownloadLog, ViewLog


@admin.register(LibraryCategory)
class LibraryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


class DownloadLogInline(admin.TabularInline):
    model = DownloadLog
    extra = 0
    readonly_fields = ('user', 'download_date', 'ip_address')
    can_delete = False
    show_change_link = True


class ViewLogInline(admin.TabularInline):
    model = ViewLog
    extra = 0
    readonly_fields = ('user', 'view_date', 'ip_address')
    can_delete = False
    show_change_link = True


@admin.register(LibraryItem)
class LibraryItemAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'resource_type', 'uploaded_by', 
        'upload_date', 'download_count', 'view_count', 'virus_scan_status', 'is_active'
    )
    list_filter = ('category', 'resource_type', 'virus_scan_status', 'is_active', 'upload_date')
    search_fields = ('title', 'description', 'preview_text')
    readonly_fields = ('download_count', 'view_count', 'virus_scan_status', 'virus_scan_report', 'upload_date')
    autocomplete_fields = ('category', 'uploaded_by')
    date_hierarchy = 'upload_date'
    inlines = [DownloadLogInline, ViewLogInline]

    fieldsets = (
        (None, {
            'fields': (
                'title', 'category', 'resource_type', 'description', 'preview_text', 'file', 'thumbnail', 'is_active'
            )
        }),
        ('Upload Info', {
            'fields': ('uploaded_by', 'upload_date')
        }),
        ('Analytics', {
            'fields': ('download_count', 'view_count')
        }),
        ('Virus Scan', {
            'fields': ('virus_scan_status', 'virus_scan_report')
        }),
    )


@admin.register(BookmarkedItem)
class BookmarkedItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'bookmarked_at')
    list_filter = ('bookmarked_at',)
    search_fields = ('user__username', 'item__title')
    date_hierarchy = 'bookmarked_at'


@admin.register(DownloadLog)
class DownloadLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'download_date', 'ip_address')
    list_filter = ('download_date',)
    search_fields = ('user__username', 'item__title', 'ip_address')
    date_hierarchy = 'download_date'


@admin.register(ViewLog)
class ViewLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'view_date', 'ip_address')
    list_filter = ('view_date',)
    search_fields = ('user__username', 'item__title', 'ip_address')
    date_hierarchy = 'view_date'
