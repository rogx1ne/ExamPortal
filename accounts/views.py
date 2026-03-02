from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.shortcuts import redirect, render

from exams.models import Exam, Result

from .decorators import admin_required, student_required
from .forms import StudentRegistrationForm


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect("login")
    else:
        form = StudentRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def dashboard(request):
    if getattr(request.user, "role", None) == "ADMIN":
        return redirect("admin_dashboard")
    return redirect("student_dashboard")


@admin_required
def admin_dashboard(request):
    exams = Exam.objects.all().order_by("-created_at")
    summary = (
        Result.objects.values("exam_id", "exam__title")
        .annotate(total_attempts=Count("id"), avg_score=Avg("score"), avg_percentage=Avg("percentage"))
        .order_by("-total_attempts", "exam__title")
    )
    recent_results = Result.objects.select_related("student", "exam").order_by("-attempted_at")[:10]
    return render(
        request,
        "accounts/admin_dashboard.html",
        {"exams": exams, "summary": summary, "recent_results": recent_results},
    )


@student_required
def student_dashboard(request):
    attempted_exam_ids = Result.objects.filter(student=request.user).values_list("exam_id", flat=True)
    available_exams = Exam.objects.filter(is_active=True).exclude(id__in=attempted_exam_ids).order_by("title")
    recent_results = Result.objects.filter(student=request.user).select_related("exam").order_by("-attempted_at")[:10]
    return render(
        request,
        "accounts/student_dashboard.html",
        {"available_exams": available_exams, "recent_results": recent_results},
    )

