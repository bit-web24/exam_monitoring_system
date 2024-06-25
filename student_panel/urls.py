from django.urls import path
from . import views

urlpatterns = [
    path('<int:student_id>/', views.student_dashboard, name='student_dashboard'),
    path('<int:student_id>/exams/', views.student_exams, name='student_exams'),
    path('<int:student_id>/exams/<int:exam_id>', views.student_exam_detail, name='student_exam_detail'),
    # path('marks', views.student_marks, name='marks'),
]
