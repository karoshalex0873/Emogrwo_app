# Generated by Django 5.1.3 on 2024-12-06 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emoAdmins', '0006_assignment_uploaded_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='uploaded_at',
        ),
    ]