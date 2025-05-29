from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import EventCategory, Event, EventAttendee

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'organizer', 'start_datetime', 'end_datetime']
    list_filter = ['category', 'organizer']
    search_fields = ['title', 'description', 'location']

@admin.register(EventAttendee)
class EventAttendeeAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'rsvp_status', 'timestamp']
    list_filter = ['rsvp_status']
    search_fields = ['event__title', 'user__username']
