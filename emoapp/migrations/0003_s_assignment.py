# Generated by Django 5.1.3 on 2024-12-10 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emoapp', '0002_remove_student_grade'),
    ]

    operations = [
        migrations.CreateModel(
            name='S_Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='submited/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
