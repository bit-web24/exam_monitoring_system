from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from admin_panel.models import Student, Teacher
import base64

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
        
        if role == 'student':
            if auth_type == 'register':
                return redirect('register_student')
            
    return render(request, 'choose_role.html')


def register_student(request):
    if request.method == 'POST':
        username = request.POST['username']
        image_data = request.POST['image_data']
        img_data = base64.b64decode(image_data.split(',')[1])
        try:
            # For simplicity, store the image data directly in the student model
            student = Student.objects.create(
                name=username,
                face_image=img_data  # Store image data (replace with face encoding in production)
                # In practice, use a face recognition library to process and store face encodings
            )
            student.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login_student')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'register_student.html')


def login_student(request):
    if request.method == 'POST':
        try:
            face_image_data = request.POST['face_image']
            username = request.POST['username']
        
            if face_image_data and username:
                img_data = base64.b64decode(face_image_data.split(',')[1])
                # Assume finding student by matching with stored face_image data (base64 encoded)
                student = get_object_or_404(Student, name=username)
                if student:
                    
                    return redirect('student_dashboard', student_id=student.pk)
                else:
                    messages.error(request, 'Face image authentication failed. Student not found.')
            else:
                messages.error(request, 'Please capture your face image.')

        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'login_student.html')
