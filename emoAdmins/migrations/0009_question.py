# Generated by Django 5.1.3 on 2024-12-07 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emoAdmins', '0008_rename_email_teacher_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('status', models.CharField(default='Pending', max_length=50)),
                ('response', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
