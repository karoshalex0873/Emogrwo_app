from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from emoapp import views

urlpatterns = [
    path("", views.Getstarted, name="getstarted"),
    path("about", views.About, name="about"),
    path("register/", views.Register, name="register"),
    path("contact/", views.Contact, name="contact"),
    path("price/", views.Pricing, name="price"),
    path("login/", views.Login, name="login"),
    path("main/", views.Main, name="main"),
    path("assignment/", views.assignment_list, name="assignment"),
    path("survey_questions/", views.survey_questions, name="survey_questions"),
    path("mygrades/", views.grade_view, name="mygrades"),
    path("Gen-pdf/", views.Gen_pdf, name="Gen_pdf"),
    path("issue/", views.Private_Session, name="issue"),
    path("delete_issue/<int:issue_id>/", views.Del_Session, name="delete_issue"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
