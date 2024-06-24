from django.db import models

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self) -> str:
        return self.name
    
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    registration_no = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    class_id = models.ForeignKey(Class, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    classes = models.ManyToManyField(Class, blank=True)
    
    def __str__(self):
        return self.name

class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class ClassCourseTeacher(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return f"{self.class_id.name} - {', '.join(course.name for course in self.courses.all())} - {self.teacher_id.name}"
