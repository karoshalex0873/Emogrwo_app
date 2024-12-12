# Generated by Django 5.1.3 on 2024-12-11 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emoapp', '0005_issue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='student_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='emoapp.student'),
        ),
    ]
