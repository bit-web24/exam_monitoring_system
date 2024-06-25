from django.urls import path
from . import views

urlpatterns = [
    path('', views.choose_role, name='choose_role'),
    path('register_teacher', views.register_teacher, name='register_teacher'),
    path('login_teacher', views.login_teacher, name='login_teacher'),
    path('register_student', views.register_student, name='register_student'),
    path('login_student', views.login_student, name='login_student'),
]
