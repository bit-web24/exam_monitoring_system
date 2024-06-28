from django import forms
from .models import ClassCourseTeacher, Student, Teacher, Class, Course, Exam, Question

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'phone', 'class_id',]

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'phone', 'password' , 'classes']
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

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'option1', 'option2', 'option3', 'option4', 'expected_answer']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['question_type'].widget = forms.RadioSelect(choices=Question.QUESTION_TYPE_CHOICES)
        for field in ['option1', 'option2', 'option3', 'option4']:
            self.fields[field].required = False

class SelectTeacherForm(forms.Form):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())

class SelectClassForm(forms.Form):
    class_id = forms.ModelChoiceField(queryset=Class.objects.none())

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super(SelectClassForm, self).__init__(*args, **kwargs)
        if teacher:
            self.fields['class_id'].queryset = teacher.classes.all()

class AssignCourseForm(forms.ModelForm):
    class Meta:
        model = ClassCourseTeacher
        fields = ['course_id']

    def __init__(self, *args, **kwargs):
        class_instance = kwargs.pop('class_instance', None)
        super(AssignCourseForm, self).__init__(*args, **kwargs)
        if class_instance:
            self.fields['course_id'].queryset = class_instance.courses.all()
