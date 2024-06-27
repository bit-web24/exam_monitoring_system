from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from admin_panel.models import Student, Teacher
import base64
import numpy as np
import cv2
import os
from deepface import DeepFace

def choose_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')

        request.session['role'] = role
        if role == 'admin':
            return redirect('dashboard')
        if role == 'teacher':
            return redirect('login_teacher')
        if role == 'student':
            return redirect('login_student')
        
    return render(request, 'choose_role.html')

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


def login_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        class_id = request.POST.get('class_id')

        try:
            student_id = int(student_id)
            # Since class_id is ForeignKey, ensure it's converted correctly or validate it
            class_id = int(class_id)

            student = get_object_or_404(Student, student_id=student_id)
            if student.class_id_id != class_id:
                raise ValueError("Class ID does not match.")

            request.session['student_id'] = student_id
            request.session['class_id'] = class_id

            if not student.face_image:
                return redirect('capture_face')
            else:
                return redirect('verify_face')

        except (ValueError, TypeError, Student.DoesNotExist) as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'login_student.html')


def capture_face(request):
    if request.method == 'POST':
        student_id = request.session.get('student_id')
        class_id = request.session.get('class_id')
        face_image = request.POST['face_image']
        
        try:
            image_data = base64.b64decode(face_image.split(',')[1])
            student = get_object_or_404(Student, student_id=student_id, class_id=class_id)
            student.face_image = image_data
            student.save()
            messages.success(request, 'Logged in successfully.')
            return redirect('student_dashboard', student_id=student_id)
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'capture_face.html')

def byte_to_png(photo, studentId, name):
    directory = f"captured/{studentId}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Assuming photo is already bytes-like, no need to decode again
    nparr = np.frombuffer(photo, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    face_filename = os.path.join(directory, f"{name}.png")
    cv2.imwrite(face_filename, img_np)
    return face_filename

def verify_face(request):
    if request.method == 'POST':
        try:
            face_image = request.POST.get('face_image')
            student_id = request.session.get('student_id')
            class_id = request.session.get('class_id')

            if face_image:
                student = get_object_or_404(Student, student_id=student_id, class_id_id=class_id)

                img_data = base64.b64decode(face_image.split(',')[1])
                stored_face_data = student.face_image

                path1 = byte_to_png(img_data, student.pk, 'login_image')
                path2 = byte_to_png(stored_face_data, student.pk, 'stored_image')

                res = DeepFace.verify(img1_path=path1, img2_path=path2)

                if res['verified']:
                    return redirect('student_dashboard', student_id=student_id)
                else:
                    messages.error(request, 'Unauthorized user detected.')
            else:
                messages.error(request, 'Please capture your face image.')

        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'verify_face.html')