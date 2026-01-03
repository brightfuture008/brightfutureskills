from django.contrib import admin
from .models import ChatMessage, CourseComment

@admin.register(CourseComment)
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'content', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'course')
    search_fields = ('content', 'user__username', 'course__title')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('message', 'sender__username', 'receiver__username')