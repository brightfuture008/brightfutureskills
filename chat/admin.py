from django.contrib import admin
from .models import CourseComment, ChatMessage

admin.site.register(CourseComment)
admin.site.register(ChatMessage)