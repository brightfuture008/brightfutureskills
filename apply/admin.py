from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import Course, Student, Region, District

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id','title','lecturer','duration_months','cost')
    search_fields = ('title','course_id','lecturer')
    list_filter = ('duration_months',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('fullname','code','gender','course','region','district')
    list_filter = ('gender','course','region')

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('stats/', self.admin_site.admin_view(self.stats_view), name='student-stats'),
        ]
        return my_urls + urls

    def stats_view(self, request):
        qs = Student.objects.all()
        total = qs.count()
        male = qs.filter(gender='M').count()
        female = qs.filter(gender='F').count()
        by_region = []
        for r in Region.objects.all():
            count = qs.filter(region=r).count()
            pct = (count / total * 100) if total else 0
            by_region.append({'region': r.name, 'count': count, 'percent': round(pct,1)})
        context = dict(self.admin_site.each_context(request), total=total, male=male, female=female, by_region=by_region)
        return render(request, 'admin/student_stats.html', context)

admin.site.register(Region)
admin.site.register(District)

