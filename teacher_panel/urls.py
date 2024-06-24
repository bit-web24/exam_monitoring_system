from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='teacher_dashboard'),
    # path('questions', views.questions, name='questions'),
    path('exams', views.exams, name='teacher_exams'),

    # exams
    path('exams/all', views.exam_list, name='teacher_exam_list'),
    path('exams/create/', views.exam_create, name='teacher_exam_create'),
    path('exams/update/<int:pk>/', views.exam_update, name='teacher_exam_update'),
    path('exams/delete/<int:pk>/', views.exam_delete, name='teacher_exam_delete'),
    path('exams/detail/<int:pk>/', views.exam_detail, name='teacher_exam_detail'),
]
