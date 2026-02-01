from django.contrib import admin
from django.urls import path, reverse
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group

from .views import approve_payments_list, confirm_admission_list, confirm_student_admission
from .models import Student, Course, Session, Region, District, Enrollment
from users.models import Profile
from chat.models import ChatMessage
from django.core.mail import send_mail

class CustomAdminSite(admin.AdminSite):
    site_header = "Bright Skills Management"
    site_title = "Bright Skills Admin"
    index_title = "Dashboard"
    index_template = 'admin/custom_dashboard.html'

    def index(self, request, extra_context=None):
        # Add pending payment count to the dashboard context
        pending_count = User.objects.filter(profile__payment_status=Profile.PaymentStatus.PENDING).count()
        pending_admission_count = Student.objects.filter(enrollments__isnull=False).exclude(user__groups__name='Admitted').distinct().count()
        if extra_context is None:
            extra_context = {}
        extra_context['pending_payment_count'] = pending_count
        extra_context['pending_admission_count'] = pending_admission_count
        return super().index(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'payments/',
                self.admin_view(approve_payments_list),
                name='payments_list'
            ),
            path(
                'confirm-admissions/',
                self.admin_view(confirm_admission_list),
                name='confirm_admission_list'
            ),
            path(
                'confirm-admissions/<int:student_id>/',
                self.admin_view(confirm_student_admission),
                name='confirm_student_admission'
            ),
        ]
        return custom_urls + urls

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        
        for app in app_list:
            if app['app_label'] == 'apply':
                app['models'].extend([
                    {
                        'name': 'Approve Payments',
                        'object_name': 'ApprovePayments',
                        'admin_url': reverse('custom_admin:payments_list'),
                        'view_only': True,
                        'perms': {'change': True, 'add': False, 'delete': False},
                    },
                    {
                        'name': 'Confirm Admissions',
                        'object_name': 'ConfirmAdmissions',
                        'admin_url': reverse('custom_admin:confirm_admission_list'),
                        'view_only': True,
                        'perms': {'change': True, 'add': False, 'delete': False},
                    }
                ])
                app['models'].sort(key=lambda x: x['name'])
        return app_list

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'is_staff', 'get_payment_status')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'profile__payment_status')
    actions = ['approve_payment', 'reject_payment']

    @admin.action(description='Approve selected applications')
    def approve_application(self, request, queryset):
        for user in queryset:
            if hasattr(user, 'profile'):
                user.profile.payment_status = Profile.PaymentStatus.APPROVED
                user.profile.save()

    @admin.action(description='Reject selected applications')
    def reject_application(self, request, queryset):
        for user in queryset:
            if hasattr(user, 'profile'):
                user.profile.payment_status = Profile.PaymentStatus.UNPAID
                user.profile.save()

    @admin.display(description='Payment Status', ordering='profile__payment_status')
    def get_payment_status(self, instance):
        try:
            return instance.profile.payment_status
        except Profile.DoesNotExist:
            return 'No Profile'

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    readonly_fields = ('enrolled_at',)
    can_delete = True

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_id', 'duration_months', 'cost')
    search_fields = ('title', 'course_id')
    filter_horizontal = ('sessions',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'code', 'email', 'selected_courses', 'is_admitted_status', 'created_at')
    list_filter = ('region', 'gender', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'code')
    inlines = [EnrollmentInline]
    raw_id_fields = ('user',)
    actions = ['confirm_admission']

    @admin.display(description='Selected Courses')
    def selected_courses(self, obj):
        return ", ".join([e.course.title for e in obj.enrollments.all()])

    @admin.display(description='Admitted', boolean=True)
    def is_admitted_status(self, obj):
        return obj.user.groups.filter(name='Admitted').exists()

    @admin.action(description='Confirm Course & Admit Student')
    def confirm_admission(self, request, queryset):
        admitted_group, _ = Group.objects.get_or_create(name='Admitted')
        count = 0
        for student in queryset:
            if not student.enrollments.exists():
                self.message_user(request, f"Skipped {student.fullname}: No courses selected.", level='warning')
                continue
            
            student.user.groups.add(admitted_group)
            
            # Send notification
            msg = (
                f"Dear {student.user.username},\n\n"
                "Your course selection has been confirmed by the administration.\n"
                "You have been officially ADMITTED. You can now download your Admission Letter from your dashboard."
            )
            ChatMessage.objects.create(sender=request.user, receiver=student.user, message=msg)
            count += 1
        self.message_user(request, f"Successfully admitted {count} students.")

admin_site = CustomAdminSite(name='custom_admin')

admin_site.register(User, UserAdmin)
admin_site.register(Group, admin.ModelAdmin)
admin_site.register(Student, StudentAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Session)
admin_site.register(Region)
admin_site.register(District)
admin_site.register(Enrollment)