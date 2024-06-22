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
]
