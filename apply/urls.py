from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    path('students/<int:student_id>/enroll/', views.enroll_student, name='enroll_student'),
    path('students/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('students/success/<int:student_id>/', views.registration_success, name='registration_success'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('ajax/districts/<int:region_id>/', views.ajax_districts, name='ajax_districts'),
    path('ajax/sessions/<int:course_id>/', views.ajax_sessions, name='ajax_sessions'),
]