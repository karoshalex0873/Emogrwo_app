from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from emoAdmins.forms import AssignmentForm, GradingForm
from emoapp.models import Issue, S_Assignment, Student, SurveyQuestion, SurveyResponse
from emoAdmins.models import Assignment, GradingSession
from emoapp.forms import IssueForm, SubmitForm, SurveyResponseForm
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


# Create your views here.
def Getstarted(request):
    return render(request, "index.html")


def About(request):
    return render(request, "about.html")


def Contact(request):
    return render(request, "contact.html")


def Pricing(request):
    return render(request, "pricing.html")


def Main(request):
    if request.method == "POST":
        if Student.objects.filter(
            email=request.POST["email"], password=request.POST["password"]
        ).exists():
            users = Student.objects.get(
                email=request.POST["email"], password=request.POST["password"]
            )
            return render(request, "main.html", {"user": users})
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    else:
        return render(request, "login.html")


def Register(request):
    if request.method == "POST":
        register_user = Student(
            name=request.POST["name"],
            email=request.POST["email"],
            age=request.POST["age"],
            gender=request.POST["gender"],
            password=request.POST["password"],
        )
        register_user.save()
        return redirect("/login")
    else:
        return render(request, "register.html")


def Login(request):
    return render(request, "login.html")


def show_assignment(request):
    student_assigment = Assignment.objects.all().order_by("title")
    return render(request, "assignments.html", {"student_assigment": student_assigment})


def assignment_list(request):
    if request.method == "POST":
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("assignment")
        else:
            messages.error(request, "Error uploading assignment. Please try again.")
    else:
        form = SubmitForm()
    submitted = Assignment.objects.all()
    return render(request, "main.html", {"form": form, "submitted": submitted})


def survey_questions(request):
    questions = SurveyQuestion.objects.all()
    if request.method == "POST":
        question_id = request.POST.get("question_id")
        question = get_object_or_404(SurveyQuestion, id=question_id)
        response_text = request.POST.get("response")
        if response_text:
            SurveyResponse.objects.create(
                question=question, response_text=response_text
            )
            return redirect("survey_questions")
    return render(request, "main.html", {"questions": questions})


def grade_view(request):
    student_sessions = GradingSession.objects.all().order_by("session_number")
    students = Student.objects.all().order_by("name")
    form = GradingForm
    return render(
        request,
        "main.html",
        {
            "students": students,
            "form": form,
            "student_sessions": student_sessions,
        },
    )


def Gen_pdf(request):
    # Create a response object to return the PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="grading_report.pdf"'

    # Create a BytesIO object to hold the PDF data
    buffer = BytesIO()

    # Initialize the document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Title with EmoGrow in a modern blue theme
    title_style = getSampleStyleSheet()["Title"]
    title_style.fontName = "Helvetica-Bold"
    title_style.fontSize = 28
    title_style.textColor = colors.HexColor("#215e41")  # Deep blue
    elements.append(Paragraph("EmoGrow", title_style))

    # Add the slogan
    slogan_style = getSampleStyleSheet()["Normal"]
    slogan_style.fontName = "Helvetica"
    slogan_style.fontSize = 16
    slogan_style.textColor = colors.HexColor("#215e41")  # Darker blue
    elements.append(Paragraph("Social Emotional Skills is Our Concern", slogan_style))

    # Add space
    elements.append(Spacer(1, 24))

    # Add a horizontal line divider in light blue
    elements.append(Spacer(1, 12))
    elements.append(
        Table(
            [[" "]],
            colWidths=[500],
            rowHeights=[2],
            style=[("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#215e41"))],
        )
    )
    elements.append(Spacer(1, 12))

    # Table with student grades and remarks
    table_data = [["Session Number", "Student Name", "Marks", "Remarks"]]

    # Add rows from GradingSession ordered by session_number, marks, and student name
    student_sessions = GradingSession.objects.all().order_by(
        "session_number", "marks", "student__name"
    )
    for session in student_sessions:
        table_data.append(
            [
                session.session_number,
                session.student.name,
                f"{session.marks}/10",
                session.remarks,
            ]
        )

    # Create the table
    table_style = TableStyle(
        [
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#215e41"),
            ),  # Deep blue for header
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.HexColor("#ffffff"),
            ),  # Light blue rows
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#215e41"),
            ),  # Blue grid lines
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
        ]
    )

    table = Table(table_data, colWidths=[100, 150, 100, 150])
    table.setStyle(table_style)
    elements.append(table)

    # Add footer or additional design elements
    elements.append(Spacer(1, 24))
    footer_style = getSampleStyleSheet()["Normal"]
    footer_style.fontName = "Helvetica"
    footer_style.fontSize = 10
    footer_style.textColor = colors.HexColor("#215e41")
    elements.append(
        Paragraph(
            "Generated by EmoGrow - Enhancing Social Emotional Learning", footer_style
        )
    )

    # Build the document
    doc.build(elements)

    # Return the PDF content to the browser
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def Private_Session(request ):
    if request.method == "POST":
        form = IssueForm(request.POST, request.FILES)
        student_id = request.POST.get("student_name")
        student = get_object_or_404(Student, id=student_id)

        if form.is_valid():
            issue = form.save(commit=False)
            issue.student_name = student  # Assign the selected student
            issue.save()
            return redirect("issue")  # Replace with your success page or URL
    else:
        form = IssueForm()

    # Pass students and issues to the template for rendering
    students = Student.objects.all()
    issues = Issue.objects.all()
    return render(
        request,
        "main.html",
        {"form": form, "students": students, "issues": issues},
    )


def Del_Session(request, issue_id):
    my_isssue = get_object_or_404(Issue, id=issue_id)
    my_isssue.delete()
    messages.success(request, "Response deleted successfully!")
    return redirect("issue")
