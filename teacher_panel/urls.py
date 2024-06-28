from django.urls import path
from . import views

urlpatterns = [
    path('<int:teacher_id>/', views.dashboard, name='teacher_dashboard'),
    path('<int:teacher_id>/about', views.teacher_about, name='teacher_about'),
    path('<int:teacher_id>/exams', views.exams, name='teacher_exams'),

    # exams
    path('<int:teacher_id>/exams/all', views.exam_list, name='teacher_exam_list'),
    path('<int:teacher_id>/exams/create/', views.exam_create, name='teacher_exam_create'),
    path('<int:teacher_id>/exams/update/<int:pk>/', views.exam_update, name='teacher_exam_update'),
    path('<int:teacher_id>/exams/delete/<int:pk>/', views.exam_delete, name='teacher_exam_delete'),
    path('<int:teacher_id>/exams/detail/<int:pk>/', views.exam_detail, name='teacher_exam_detail'),
    path('<int:teacher_id>/exams/assign2class', views.exam_assign2class, name='teacher_assign_exam2class')
]
