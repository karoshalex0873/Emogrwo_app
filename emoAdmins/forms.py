from django import forms
from emoAdmins.models import Assignment, GradingSession, Question
from emoapp.models import SurveyQuestion, SurveyResponse,Student


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["title", "file"]  # Match the fields in the model


class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "body"]


class SurveyQuestionForm(forms.ModelForm):
    class Meta:
        model = SurveyQuestion
        fields = ["title", "body"]  # Fields to display in the form
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the question title",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Provide the details of the question",
                    "rows": 4,
                }
            ),
        }


class GradingForm(forms.ModelForm):
    class Meta:
        model = GradingSession
        fields = [
            "student",
            "session_number",
            "marks",
            "remarks",
        ]  # Use 'session_number' instead of 'session'
