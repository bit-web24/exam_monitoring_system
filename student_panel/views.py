from django.shortcuts import get_object_or_404, redirect, render
from admin_panel.models import Class, Exam, Student, StudentExamAttempted, ExamQuestion, Question

def student_dashboard(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student.class_id == None:
        _class = None
    else:
        _class = get_object_or_404(Class, pk=student.class_id.pk)
    
    if _class is None:
        total = {
            'exams': 0,
        }
    else:
        total = {
            'exams': _class.exams.count(),
        }
    return render(request, 'student_dashboard/dashboard.html', {'student': student, 'total': total})

def student_exams(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    _class = get_object_or_404(Class, pk=student.class_id.pk)
    exams = _class.exams.all()
    return render(request, 'student_exams/dashboard.html', {'student': student, 'exams': exams})

def student_exam_detail(request, student_id, exam_id):
    student = get_object_or_404(Student, pk=student_id)
    _class = get_object_or_404(Class, pk=student.class_id.pk)
    exam = get_object_or_404(_class.exams, pk=exam_id)
    total_questions = ExamQuestion.objects.filter(exam=exam).count()
    return render(request, 'student_exams/exam_detail.html', {'student': student, 'class': _class, 'exam': exam, 'total_questions': total_questions})

def student_exam_start(request, student_id, exam_id):
    student = get_object_or_404(Student, pk=student_id)
    exam = get_object_or_404(Exam, pk=exam_id)  # Corrected to use pk for primary key
    exam_questions = ExamQuestion.objects.filter(exam=exam)
    questions = [exam_question.question for exam_question in exam_questions]  # List comprehension for simplicity

    return render(request, 'student_exams/exam_start.html', {
        'student': student,
        'questions': questions,
        'exam': exam
    })

def student_exam_submit(request, student_id, exam_id):
    student = get_object_or_404(Student, pk=student_id)
    exam = get_object_or_404(Exam, exam_id=exam_id)
    sea = StudentExamAttempted.objects.create(student=student, exam=exam, attempted=True)
    sea.save()
    return redirect('student_exams', student_id=student.pk)