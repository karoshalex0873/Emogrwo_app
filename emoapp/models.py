from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class S_Assignment(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="submited/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SurveyQuestion(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SurveyResponse(models.Model):
    question = models.ForeignKey(
        SurveyQuestion, on_delete=models.CASCADE, related_name="responses"
    )
    response_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to: {self.question.title}"


class Issue(models.Model):
    ISSUE_TYPES = [
        ("text", "Text"),
        ("audio", "Audio"),
        ("video", "Video"),
    ]
    student_name = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="issues",
    )
    issue_type = models.CharField(max_length=5, choices=ISSUE_TYPES)
    text_message = models.TextField(blank=True, null=True)
    audio_message = models.FileField(upload_to="audio_issues/", blank=True, null=True)
    video_message = models.FileField(upload_to="video_issues/", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.issue_type}"
