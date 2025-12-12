from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.home, name='home'),
    path('students/add/', views.add_student, name='add_student'),
    path('my-profile/', views.student_profile, name='student_profile'),
    path('my-profile/edit/', views.edit_student, name='edit_student'),

    # Admin/staff-like views (optional, can be secured further)
    path('admin/students/', views.student_list, name='student_list'),
    path('admin/students/<int:student_id>/', views.student_detail, name='student_detail'),
    # Course views
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('ajax/districts/<int:region_id>/', views.ajax_districts, name='ajax_districts'),
    path('ajax/sessions/<int:course_id>/', views.ajax_sessions, name='ajax_sessions'),
    ]