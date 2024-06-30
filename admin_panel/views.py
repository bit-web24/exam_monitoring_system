from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import ClassCourseTeacher, Student, Teacher, Class, Course, Exam, TeacherCourse
from .forms import AssignCourseForm, SelectClassForm, SelectTeacherForm, StudentForm, TeacherForm, ClassForm, CourseForm, ExamForm

# SECTION: DASHBOARD
def dashboard(request):
    total = {
        'students' : len(Student.objects.all()),
        'teachers' : len(Teacher.objects.all()),
        'courses' : len(Course.objects.all()),
        'classes' : len(Class.objects.all()),
        'exams' : len(Exam.objects.all()),
    }
    return render(request, 'dashboard/dashboard.html', {'total': total})

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
            unique_id = form.cleaned_data['unique_id']
            if not Student.objects.filter(unique_id=unique_id).exists():
                student = form.save()
                return redirect('student_detail', pk=student.pk)
            else:
                messages.error(request, 'Student with unique ID Already Exists.')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            unique_id = form.cleaned_data['unique_id']
            new_student = Student.objects.filter(unique_id=unique_id)
            if new_student.exists() and new_student[0].pk == pk:
                form.save()
                return redirect('student_list')
            else:
                messages.error(request, 'Student\'s unique ID Can\'t be changed.')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})

def student_assign2class(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        student_ids = request.POST.getlist('students')
        selected_class = Class.objects.get(pk=class_id)

        for student_id in student_ids:
            student = Student.objects.get(pk=student_id)
            student.class_id = selected_class
            student.save()

        return redirect('student_assign2class')
    
    students = [stud for stud in Student.objects.all() if not stud.class_id]
    classes = Class.objects.all()
    return render(request, 'students/student_assign2class.html', {'students': students, 'classes': classes})


# SECTION: TEACHERS 
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher})

def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            return redirect('teacher_detail', pk=teacher.pk)
    else:
        form = TeacherForm()
    return render(request, 'teachers/teacher_form.html', {'form': form})

def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'teachers/teacher_form.html', {'form': form})

def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teacher_list')
    return render(request, 'teachers/teacher_confirm_delete.html', {'teacher': teacher})

def teacher_assign2class(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        classes = request.POST.getlist('classes')
        selected_teacher = Teacher.objects.get(pk=teacher_id)
        for _class in classes:
            if not selected_teacher.classes.filter(pk=_class).exists():
                selected_teacher.classes.add(_class)
        selected_teacher.save()

        return redirect('teacher_assign2class')
    
    teachers = Teacher.objects.all()
    classes = Class.objects.all()
    return render(request, 'teachers/teacher_assign2class.html', {'teachers': teachers, 'classes': classes})

def select_teacher(request):
    if request.method == 'POST':
        form = SelectTeacherForm(request.POST)
        if form.is_valid():
            teacher = form.cleaned_data['teacher']
            return redirect('select_class', teacher_id=teacher.pk)
    else:
        form = SelectTeacherForm()
    return render(request, 'teachers/select_teacher.html', {'form': form})

def select_class(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    if request.method == 'POST':
        form = SelectClassForm(request.POST, teacher=teacher)
        if form.is_valid():
            class_id = form.cleaned_data['class_id']
            return redirect('assign_course', teacher_id=teacher.pk, class_id=class_id.pk)
    else:
        form = SelectClassForm(teacher=teacher)
    return render(request, 'teachers/select_class.html', {'form': form, 'teacher': teacher})

def assign_course(request, teacher_id, class_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    class_instance = get_object_or_404(Class, pk=class_id)
    
    if request.method == 'POST':
        form = AssignCourseForm(request.POST, class_instance=class_instance)
        if form.is_valid():
            course = form.cleaned_data['course_id']
            ClassCourseTeacher.objects.create(
                teacher_id=teacher,
                class_id=class_instance,
                course_id=course
            )
            TeacherCourse.objects.create(teacher=teacher, course=course).save()
            return redirect('class_course_teacher_list')
    else:
        form = AssignCourseForm(class_instance=class_instance)
    
    return render(request, 'teachers/assign_course.html', {
        'teacher': teacher,
        'class': class_instance,
        'form': form,
    })

def load_classes(request):
    teacher_id = request.GET.get('teacher_id')
    classes = Class.objects.filter(teacher__id=teacher_id)
    return JsonResponse(list(classes.values('id', 'name')), safe=False)

def class_course_teacher_list(request):
    assignments = ClassCourseTeacher.objects.all()
    return render(request, 'teachers/class_course_teacher_list.html', {'assignments': assignments})


# SECTION: CLASSES 
def class_list(request):
    classes = Class.objects.all()
    return render(request, 'classes/class_list.html', {'classes': classes})

def class_detail(request, pk):
    _class = get_object_or_404(Class, pk=pk)
    return render(request, 'classes/class_detail.html', {'class': _class})

def class_create(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            unique_id = form.cleaned_data['unique_id']
            if not Class.objects.filter(unique_id=unique_id).exists():
                _class = form.save()
                return redirect('class_detail', pk=_class.pk)
            else:
                messages.error(request, f"Class with unique-id {unique_id} already exist.")
    else:
        form = ClassForm()
    return render(request, 'classes/class_form.html', {'form': form})

def class_update(request, pk):
    _class = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=_class)
        if form.is_valid():
            unique_id = form.cleaned_data['unique_id']
            new_class = Class.objects.filter(unique_id=unique_id)
            if new_class.exists() and new_class[0].pk == pk:
                form.save()
                return redirect('class_list')
            else:
                messages.error(request, "Class's unique-id can't be changed.")
    else:
        form = ClassForm(instance=_class)
    return render(request, 'classes/class_form.html', {'form': form})

def class_delete(request, pk):
    _class = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        _class.delete()
        return redirect('class_list')
    return render(request, 'classes/class_confirm_delete.html', {'class': _class})

def class_assigncourse(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        courses = request.POST.getlist('courses')
        selected_class = Class.objects.get(pk=class_id)
        for course in courses:
            if not selected_class.courses.filter(pk=course).exists():
                selected_class.courses.add(course)
        selected_class.save()

        return redirect('class_assigncourse')
    
    courses = Course.objects.all()
    classes = Class.objects.all()
    return render(request, 'classes/class_assigncourse.html', {'courses': courses, 'classes': classes})


# SECTION: COURSES 
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})

def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})

def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form})

def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

# SECTION: EXAMS 
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'exams/exam_list.html', {'exams': exams})

def exam_detail(request, pk):
    _exam = get_object_or_404(Exam, pk=pk)
    return render(request, 'exams/exam_detail.html', {'exam': _exam})
