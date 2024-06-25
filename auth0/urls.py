from django.urls import path
from . import views

urlpatterns = [
    path('', views.choose_role, name='choose_role'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
]
