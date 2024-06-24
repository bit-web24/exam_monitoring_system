from django.shortcuts import get_object_or_404, redirect, render
from .forms import ExamForm
from .models import Exam

# dashboard
def dashboard(request):
    total = {
        'exams' : len(Exam.objects.all()),
    }
    return render(request, 'teacher_dashboard/dashboard.html', {'total': total})

def exams(request):
    return render(request, 'teacher_exams/dashboard.html')

# SECTION: EXAMS
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'teacher_exams/exam_list.html', {'exams': exams})

def exam_detail(request, pk):
    _exam = get_object_or_404(Exam, pk=pk)
    return render(request, 'teacher_exams/exam_detail.html', {'exam': _exam})

def exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            _exam = form.save()
            return redirect('teacher_exam_detail', pk=_exam.pk)
    else:
        form = ExamForm()
    return render(request, 'teacher_exams/exam_form.html', {'form': form})

def exam_update(request, pk):
    _exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=_exam)
        if form.is_valid():
            form.save()
            return redirect('teacher_exam_list')
    else:
        form = ExamForm(instance=_exam)
    return render(request, 'teacher_exams/exam_form.html', {'form': form})

def exam_delete(request, pk):
    _exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        _exam.delete()
        return redirect('teacher_exam_list')
    return render(request, 'teacher_exams/exam_confirm_delete.html', {'exam': _exam})
