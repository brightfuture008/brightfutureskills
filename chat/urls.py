from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chat/', views.chat_view, name='chat_list'),
    path('chat/<int:user_id>/', views.chat_view, name='chat_with'),
    path('comment/add/<int:course_id>/', views.add_comment, name='add_comment'),
    path('comment/edit/<int:comment_id>/', views.update_comment, name='update_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]