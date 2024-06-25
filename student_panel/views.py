from django.shortcuts import get_object_or_404, render
from admin_panel.models import Class, Student

def student_dashboard(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    _class = get_object_or_404(Class, pk=student.class_id.pk)
    total = {
        'exams': _class.exams.count(),
    }
    return render(request, 'student_dashboard/dashboard.html', {'student': student, 'total': total})

def student_exams(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    _class = get_object_or_404(Class, pk=student.class_id.pk)
    exams = _class.exams.all()
    return render(request, 'student_exams/dashboard.html', {'student': student, 'exams': exams})
