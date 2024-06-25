from django.urls import path
from . import views

urlpatterns = [
    path('<int:student_id>/', views.student_dashboard, name='student_dashboard'),
    path('<int:student_id>/exams/', views.student_exams, name='student_exams'),
    # path('marks', views.student_marks, name='marks'),
]
