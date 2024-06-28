from django.shortcuts import get_object_or_404, redirect, render
from admin_panel.models import Class, Teacher
from admin_panel.forms import ExamForm
from admin_panel.models import Exam, ClassCourseTeacher

# Dashboard
def dashboard(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    total = {
        'exams': Exam.objects.count(),
    }
    return render(request, 'teacher_dashboard/dashboard.html', {'teacher': teacher, 'total': total})

def exams(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    return render(request, 'teacher_exams/dashboard.html', {'teacher': teacher})

def questions(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    return render(request, 'teacher_questions/dashboard.html', {'teacher': teacher})

# SECTION: EXAMS
def exam_list(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    exams = Exam.objects.all()
    return render(request, 'teacher_exams/exam_list.html', {'teacher': teacher, 'exams': exams})

def exam_detail(request, teacher_id, pk):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    _exam = get_object_or_404(Exam, pk=pk)
    return render(request, 'teacher_exams/exam_detail.html', {'teacher': teacher, 'exam': _exam})

def exam_create(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            _exam = form.save()
            return redirect('teacher_exam_detail', teacher_id=teacher_id, pk=_exam.pk)
    else:
        form = ExamForm()
    return render(request, 'teacher_exams/exam_form.html', {'teacher': teacher, 'form': form})

def exam_update(request, teacher_id, pk):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    _exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=_exam)
        if form.is_valid():
            form.save()
            return redirect('teacher_exam_list', teacher_id=teacher_id)
    else:
        form = ExamForm(instance=_exam)
    return render(request, 'teacher_exams/exam_form.html', {'teacher': teacher, 'form': form})

def exam_delete(request, teacher_id, pk):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    _exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        _exam.delete()
        return redirect('teacher_exam_list', teacher_id=teacher_id)
    return render(request, 'teacher_exams/exam_confirm_delete.html', {'teacher': teacher, 'exam': _exam})

def exam_assign2class(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        exam_id = request.POST.get('exam_id')
        
        class_instance = Class.objects.get(pk=class_id)
        class_instance.exams.add(exam_id)
        return redirect('teacher_exam_list', teacher_id=teacher_id)
    
    classes = teacher.classes.all()
    exams = Exam.objects.all()
    return render(request, 'teacher_exams/exam_assign2class.html', {'teacher': teacher, 'classes': classes, 'exams': exams})
