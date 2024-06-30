from django.shortcuts import get_object_or_404, redirect, render
from admin_panel.models import Class, Teacher
from admin_panel.forms import ExamForm, QuestionForm
from admin_panel.models import Exam, ExamQuestion, Question, TeacherExam
from teacher_panel.forms import SelectExamForm

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
            teacher_exam = TeacherExam.objects.create(teacher=teacher, exam=_exam)
            teacher_exam.save()
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
    return render(request, 'teacher_exams/exam_form.html', {'teacher': teacher, 'form': form, 'exam': _exam})

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

# Questions Section
def select_exam_to_list_question(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    if request.method == 'POST':
        form = SelectExamForm(request.POST, teacher=teacher)
        if form.is_valid():
            selected_exam = form.cleaned_data['exam']
            return redirect('teacher_question_list', teacher_id=teacher.pk, exam_id=selected_exam.pk)
    else:
        form = SelectExamForm(teacher=teacher)
    return render(request, 'teacher_questions/select_exam.html', {'form': form, 'teacher': teacher})

def question_list(request, teacher_id, exam_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    exam = Exam.objects.get(pk=exam_id)
    exam_questions = ExamQuestion.objects.filter(exam=exam_id)
    questions = [exam_question.question for exam_question in exam_questions]
    return render(request, 'teacher_questions/question_list.html', {'teacher': teacher, 'questions': questions, 'exam': exam})

def select_exam_to_create_question(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    if request.method == 'POST':
        form = SelectExamForm(request.POST, teacher=teacher)
        if form.is_valid():
            selected_exam = form.cleaned_data['exam']
            return redirect('teacher_question_create', teacher_id=teacher.pk, exam_id=selected_exam.pk)
    else:
        form = SelectExamForm(teacher=teacher)
    return render(request, 'teacher_questions/select_exam.html', {'form': form, 'teacher': teacher})

def question_create(request, teacher_id, exam_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    exam = get_object_or_404(Exam, exam_id=exam_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            eq = ExamQuestion.objects.create(exam=exam, question=question)
            eq.save()
            return redirect('teacher_question_detail', teacher_id=teacher.pk, question_id=question.pk)
    form = QuestionForm()
    return render(request, 'teacher_questions/question_form.html', {'teacher': teacher, 'form': form})

def question_detail(request, teacher_id, question_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    question = Question.objects.get(pk=question_id)
    return render(request, 'teacher_questions/question_detail.html', {'teacher': teacher, 'question': question})

def question_update(request, teacher_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('teacher_question_detail', teacher_id=teacher.pk, question_id=question.pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'teacher_questions/question_form.html', {'teacher': teacher, 'form': form, 'question': question, 'update': True})

def question_delete(request, teacher_id, question_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    question = get_object_or_404(Question, pk=question_id)

    teacher_exams = TeacherExam.objects.filter(teacher=teacher)
    exam = None

    for teacher_exam in teacher_exams:
        tmp_exam = teacher_exam.exam
        if ExamQuestion.objects.filter(exam=tmp_exam, question=question).exists():
            exam = tmp_exam
            break

    if request.method == 'POST':
        question.delete()
        return redirect('teacher_question_list', teacher_id=teacher.pk, exam_id=exam.pk)

    return render(request, 'teacher_questions/question_confirm_delete.html', {'teacher': teacher, 'question': question, 'exam': exam})

# Results
def results(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    return render(request, 'teacher_results/dashboard.html', {
        'teacher': teacher,
    })