from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Conversation, Message, ContactRestriction

admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(ContactRestriction)