from django.contrib import admin
from .models import Student, Course, Region, District, Session

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_id', 'cost')

admin.site.register(Student)
admin.site.register(Region)
admin.site.register(District)