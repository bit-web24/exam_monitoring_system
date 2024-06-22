from django.db import models

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    registration_no = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name