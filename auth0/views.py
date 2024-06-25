from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from admin_panel.models import Student, Teacher

def register_teacher(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            teacher = Teacher.objects.create(
                name=username,
                password=password,
                email="",
                phone=""
            )
            teacher.save()

            messages.success(request, 'Account created successfully.')
            return redirect('login_teacher')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request, 'register_teacher.html')

def login_teacher(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            teacher = Teacher.objects.get(name=username)
            if teacher.password == password:
                request.session['teacher_id'] = teacher.pk
                return redirect(f'teacher_dashboard', teacher_id=teacher.pk)
            else:
                messages.error(request, 'Invalid password.')
        except Teacher.DoesNotExist:
            messages.error(request, 'Teacher not found.')
    return render(request, 'login_teacher.html')

def choose_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        auth_type = request.POST.get('auth')

        request.session['role'] = role

        if role == 'admin':
            return redirect('dashboard')
        
        if role == 'teacher':
            if auth_type == 'login':
                return redirect('login_teacher')
            elif auth_type == 'register':
                return redirect('register_teacher')
            
    return render(request, 'choose_role.html')

# if role == 'student':
#                 student = Student.objects.create(
#                     name=username,
#                     password=password,
#                     registration_no="",
#                     email="",
#                     phone="",
#                     class_id=None
#                 )
#                 student.save()


# if role == 'student':
#     try:
#         student = Student.objects.get(name=username)
#         if student.password == password:
#             request.session['student_id'] = student.pk
#             return redirect('student_dashboard', student_id=student.pk)
#         else:
#             messages.error(request, 'Invalid password.')
#     except Student.DoesNotExist:
#         messages.error(request, 'Student not found.')