# Generated by Django 4.2.11 on 2024-06-24 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0010_remove_classcourseteacher_course_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classcourseteacher',
            name='courses',
        ),
        migrations.AddField(
            model_name='classcourseteacher',
            name='course_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.course'),
        ),
    ]