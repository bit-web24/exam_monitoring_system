from django.urls import path
from .views import dashboard, students, teachers, classes, courses, exams
from . import views

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('students', students, name='students'),
    path('teachers', teachers, name='teachers'),
    path('classes', classes, name='classes'),
    path('courses', courses, name='courses'),
    path('exams', exams, name='exams'),
    
    # students
    path('students/all', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/update/<int:pk>/', views.student_update, name='student_update'),
    path('students/delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('students/detail/<int:pk>/', views.student_detail, name='student_detail'),
    
    # teachers
    path('teachers/all', views.teacher_list, name='teacher_list'),
    path('teachers/create/', views.teacher_create, name='teacher_create'),
    path('teachers/update/<int:pk>/', views.teacher_update, name='teacher_update'),
    path('teachers/delete/<int:pk>/', views.teacher_delete, name='teacher_delete'),
    path('teachers/detail/<int:pk>/', views.teacher_detail, name='teacher_detail'),

    # classes
    path('classes/all', views.class_list, name='class_list'),
    path('classes/create/', views.class_create, name='class_create'),
    path('classes/update/<int:pk>/', views.class_update, name='class_update'),
    path('classes/delete/<int:pk>/', views.class_delete, name='class_delete'),
    path('classes/detail/<int:pk>/', views.class_detail, name='class_detail'),

    # courses
    path('courses/all', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/update/<int:pk>/', views.course_update, name='course_update'),
    path('courses/delete/<int:pk>/', views.course_delete, name='course_delete'),
    path('courses/detail/<int:pk>/', views.course_detail, name='course_detail'),

    # exams
    path('exams/all', views.exam_list, name='exam_list'),
    path('exams/create/', views.exam_create, name='exam_create'),
    path('exams/update/<int:pk>/', views.exam_update, name='exam_update'),
    path('exams/delete/<int:pk>/', views.exam_delete, name='exam_delete'),
    path('exams/detail/<int:pk>/', views.exam_detail, name='exam_detail'),
]
