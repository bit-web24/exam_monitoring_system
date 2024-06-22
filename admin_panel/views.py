from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student
from .forms import StudentForm

# SECTION: DASHBOARD
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def students(request):
    return render(request, 'students/dashboard.html')

def teachers(request):
    return render(request, 'teachers/dashboard.html')

def courses(request):
    return render(request, 'courses/dashboard.html')

def classes(request):
    return render(request, 'classes/dashboard.html')

def exams(request):
    return render(request, 'exams/dashboard.html')

# SECTION: STUDENTS 
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})
