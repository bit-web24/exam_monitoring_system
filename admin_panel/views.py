from django.shortcuts import render

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
