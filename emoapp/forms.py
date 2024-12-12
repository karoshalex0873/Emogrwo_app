from django import forms
from emoapp.models import Issue, S_Assignment, SurveyResponse


class SubmitForm(forms.ModelForm):
    class Meta:
        model = S_Assignment
        fields = ["title", "file"]


class SurveyResponseForm(forms.ModelForm):
    class Meta:
        model = SurveyResponse
        fields = ["response_text"]
        widgets = {
            "response_text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your answer here...",
                    "rows": 3,
                    "style": "border-color: #198754;",
                }
            ),
        }


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["issue_type", "text_message", "audio_message", "video_message"]

    def clean(self):
        cleaned_data = super().clean()
        issue_type = cleaned_data.get("issue_type")
        if issue_type == "text" and not cleaned_data.get("text_message"):
            raise forms.ValidationError("Text message cannot be empty.")
        elif issue_type == "audio" and not cleaned_data.get("audio_message"):
            raise forms.ValidationError("Please upload an audio file.")
        elif issue_type == "video" and not cleaned_data.get("video_message"):
            raise forms.ValidationError("Please upload a video file.")
        return cleaned_data
