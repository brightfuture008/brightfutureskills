from django.urls import path
from . import views

app_name = 'apply'

urlpatterns = [
    path('', views.home, name='home'),
    # Application Flow
    path('apply/', views.application_start, name='application_start'),
    path('apply/personal-info/', views.personal_info_view, name='personal_info'),
    path('apply/payment/', views.payment_view, name='payment'),
    path('apply/course-request/', views.course_request_view, name='course_request'),

    path('my-profile/', views.student_profile, name='student_profile'),
    path('my-profile/edit/', views.edit_student, name='edit_student'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    # AJAX URLs
    path('ajax/districts/<int:region_id>/', views.ajax_districts, name='ajax_districts'),
    path('ajax/sessions/<int:course_id>/', views.ajax_sessions, name='ajax_sessions'),

    # Payment flow URLs
    path('payment-instructions/', views.payment_instructions, name='payment_instructions'),
    path('mark-as-paid/', views.mark_as_paid, name='mark_as_paid'),
    path('manage/approve-payments/', views.approve_payments_list, name='approve_payments_list'),
    path('manage/approve/<int:user_id>/', views.approve_user_payment, name='approve_user_payment'),
]