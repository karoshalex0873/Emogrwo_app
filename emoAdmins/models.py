from django.db import models
from mimetypes import guess_type
from emoapp.models import Student

# Create your models here.
class teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    gender = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="assignments/")

    def __str__(self):
        return self.title

class Question(models.Model):
    title=models.CharField(max_length=200)
    body=models.TextField()

    def __str__(self):
        return self.title


class GradingSession(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="grading_sessions"
    )
    session_number = models.IntegerField()  # Correct field name here
    marks = models.IntegerField()
    remarks = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.session_number} - {self.student.name}"


