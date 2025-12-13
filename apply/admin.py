from django.contrib import admin
from django.urls import path
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .views import approve_payments_list
from .models import Student, Course, Session, Region, District, Enrollment
from users.models import Profile

class CustomAdminSite(admin.AdminSite):
    site_header = "Bright Skills Management"
    index_template = 'admin/index.html'

    def index(self, request, extra_context=None):
        pending_count = User.objects.filter(profile__payment_status=Profile.PaymentStatus.PENDING).count()
        if extra_context is None:
            extra_context = {}
        extra_context['pending_payment_count'] = pending_count
        return super().index(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'payments/',
                self.admin_view(approve_payments_list),
                name='payments_list'
            ),
        ]
        return custom_urls + urls

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fields = ('payment_status',)

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'is_staff', 'get_payment_status')
    list_filter = ('is_staff', 'is_superuser', 'groups', 'profile__payment_status')

    @admin.display(description='Payment Status')
    def get_payment_status(self, obj):
        return obj.profile.get_payment_status_display()

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    verbose_name = "Course Enrollment"
    verbose_name_plural = "Course Enrollments"
    fields = ('course', 'session')
    readonly_fields = ('course', 'session')
    can_delete = False

class StudentAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'code', 'email', 'region', 'created_at')
    list_filter = ('region', 'gender', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'code')
    inlines = [EnrollmentInline]

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_id', 'duration_months', 'cost')
    search_fields = ('title', 'course_id')
    filter_horizontal = ('sessions',)

admin_site = CustomAdminSite(name='custom_admin')

admin_site.register(User, UserAdmin)
admin_site.register(Student, StudentAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Session)
admin_site.register(Region)
admin_site.register(District)
admin_site.register(Enrollment)