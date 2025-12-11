from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.home, name='home'),
    path('course_list/', views.course_list, name='course_list'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_course/', views.add_course, name='add_course'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('enroll/<int:student_id>/', views.enroll_student, name='enroll_student'),
    path('ajax/districts/<int:region_id>/', views.ajax_districts, name='ajax_districts'),
]