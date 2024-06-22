from django import forms
from .models import Student, Teacher, Class, Course, Exam

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'registration_no', 'email', 'phone']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'email', 'phone']

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name']