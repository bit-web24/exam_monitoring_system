from django.urls import path
from .views import dashboard, students, teachers, classes, courses, exams

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('students', students, name='students'),
    path('teachers', teachers, name='teachers'),
    path('classes', classes, name='classes'),
    path('courses', courses, name='courses'),
    path('exams', exams, name='exams'),
]
