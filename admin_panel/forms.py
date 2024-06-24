from django import forms
from .models import Student, Teacher, Class, Course, Exam

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'registration_no', 'email', 'phone', 'class_id',]

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'email', 'phone', 'classes']
        widgets = {
            'classes': forms.CheckboxSelectMultiple()
        }

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'courses']
        widgets = {
            'courses': forms.CheckboxSelectMultiple()
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name']

class SelectTeacherForm(forms.Form):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())

class SelectClassForm(forms.Form):
    class_id = forms.ModelChoiceField(queryset=Class.objects.none())

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super(SelectClassForm, self).__init__(*args, **kwargs)
        if teacher:
            self.fields['class_id'].queryset = teacher.classes.all()

class AssignCourseForm(forms.Form):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.none(),
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        class_instance = kwargs.pop('class_instance', None)
        super(AssignCourseForm, self).__init__(*args, **kwargs)
        if class_instance:
            self.fields['courses'].queryset = class_instance.courses.all()
