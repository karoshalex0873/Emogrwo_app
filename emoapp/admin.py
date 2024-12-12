from django.contrib import admin
from emoapp.models import Student,S_Assignment,SurveyQuestion,SurveyResponse,Issue
# Register your models here.
admin.site.register(Student)
admin.site.register(S_Assignment)
admin.site.register(SurveyResponse)
admin.site.register(SurveyQuestion)
admin.site.register(Issue)