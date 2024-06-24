# Generated by Django 4.2.11 on 2024-06-24 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0008_class_courses'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassCourseTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.class')),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.course')),
                ('teacher_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.teacher')),
            ],
        ),
    ]