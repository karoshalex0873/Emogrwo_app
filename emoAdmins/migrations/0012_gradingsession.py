# Generated by Django 5.1.3 on 2024-12-11 09:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emoAdmins', '0011_rename_questions_question'),
        ('emoapp', '0004_surveyquestion_surveyresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='GradingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_number', models.IntegerField()),
                ('marks', models.IntegerField()),
                ('remarks', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grading_sessions', to='emoapp.student')),
            ],
        ),
    ]
