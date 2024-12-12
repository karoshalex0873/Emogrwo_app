from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from emoAdmins.forms import AssignmentForm, GradingForm, SurveyQuestionForm
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from emoAdmins.models import GradingSession, teacher, Assignment
from emoapp.models import Student, SurveyQuestion, SurveyResponse
from emoAdmins.forms import AssignmentForm, QuestionsForm, GradingSession
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


def admin_site(request):
    if request.method == "POST":
        if teacher.objects.filter(
            email=request.POST["email"], password=request.POST["password"]
        ).exists():
            users = teacher.objects.get(
                email=request.POST["email"], password=request.POST["password"]
            )
            return render(request, "admin.html", {"user": users})
        else:
            return render(
                request, "loginAdmin.html", {"error": "Invalid email or password"}
            )
    return render(request, "admin.html")


def adminLogin(request):
    return render(request, "loginAdmin.html")


def Upload(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment uploaded successfully!")
            return redirect("upload")
        else:
            messages.error(request, "Error uploading assignment. Please try again.")
    else:
        form = AssignmentForm()
    assignments = Assignment.objects.all()  # Fetch all uploaded assignments
    return render(request, "admin.html", {"form": form, "docs": assignments})


def upload_question(request):
    if request.method == "POST":
        form = SurveyQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("questions")
    else:
        form = SurveyQuestionForm()
    return render(request, "admin.html", {"form": form})


def delete_assigment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment.delete()
    messages.success(request, "Assignment deleted successfully!")
    return redirect("upload")


def Responses(request):
    questions = SurveyQuestion.objects.prefetch_related("responses").all()
    myrespo = SurveyResponse.objects.select_related("question").all()
    context = {"questions": questions, "myrespo": myrespo}
    return render(request, "admin.html", context)


def grading_view(request):
    students = Student.objects.all()  # Fetch all students

    if request.method == "POST":
        form = GradingForm(request.POST)
        if form.is_valid():
            form.save()  # Save the valid form data to the database
            return redirect("grading_view")  # Redirect after saving
        else:
            print("Form errors:", form.errors)  # Debug: check validation errors
    else:
        form = GradingForm()

    # Fetch previous grading sessions
    student_sessions = GradingSession.objects.all()
    return render(
        request,
        "admin.html",
        {
            "students": students,
            "form": form,
            "student_sessions": student_sessions,
        },
    )


def generate_pdf(request):

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

    # Add rows from GradingSession
    student_sessions = GradingSession.objects.all()
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


def delete_Grades(request, grade_id):
    grades = get_object_or_404(GradingSession, id=grade_id)
    grades.delete()
    messages.success(request, "Assignment deleted successfully!")
    return redirect("grading_view")


def delete_question(request, question_id):
    question = get_object_or_404(SurveyQuestion, id=question_id)
    question.delete()
    messages.success(request, "Question deleted successfully!")
    return redirect("response")


def delete_response(request, response_id):
    response = get_object_or_404(SurveyResponse, id=response_id)
    response.delete()
    messages.success(request, "Response deleted successfully!")
    return redirect("response")
