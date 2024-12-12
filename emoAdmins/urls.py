from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from EmoGrow import settings
from emoAdmins import views
from django.conf.urls.static import static

urlpatterns = [
    path("index/", views.admin_site, name="index"),
    path("loginAdmin/", views.adminLogin, name="loginAdmin"),
    path("index/upload/", views.Upload, name="upload"),
    path("upload/delete/<int:assignment_id>/", views.delete_assigment, name="delete"),
    path("questions/", views.upload_question, name="questions"),
    path("response", views.Responses, name="response"),
    path("grading/", views.grading_view, name="grading_view"),
    path("generate-pdf/", views.generate_pdf, name="generate_pdf"),
    path("grading/delete/<int:grade_id>/", views.delete_Grades, name="deleteGrade"),
    path("delete_question/<int:question_id>/",views.delete_question,name="delete_question",),
    path("delete_response/<int:response_id>/",views.delete_response,name="delete_response",),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
