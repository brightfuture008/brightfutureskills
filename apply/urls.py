from django.urls import path
from . import views

app_name = 'apply'

urlpatterns = [
    path('', views.home, name='home'),
    path('apply/', views.add_student, name='add_student'),
    path('apply/confirm/', views.confirm_student_application, name='confirm_student_application'),
    path('my-profile/', views.student_profile, name='student_profile'),
    path('my-profile/edit/', views.edit_student, name='edit_student'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    # AJAX URLs
    path('ajax/districts/<int:region_id>/', views.ajax_districts, name='ajax_districts'),
    path('ajax/sessions/<int:course_id>/', views.ajax_sessions, name='ajax_sessions'),
]