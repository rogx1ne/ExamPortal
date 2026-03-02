from decimal import Decimal, ROUND_HALF_UP

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Avg, Count
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required, student_required

from .forms import ExamForm, QuestionForm, TakeExamForm
from .models import Exam, Question, Result, ResultAnswer


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


@student_required
def exam_list(request):
    results = Result.objects.filter(student=request.user).values_list("exam_id", flat=True)
    exams = Exam.objects.filter(is_active=True).order_by("title")
    return render(request, "exams/exam_list.html", {"exams": exams, "attempted_exam_ids": set(results)})


@student_required
def take_exam(request, exam_id: int):
    exam = get_object_or_404(Exam, id=exam_id, is_active=True)
    if Result.objects.filter(student=request.user, exam=exam).exists():
        messages.info(request, "You have already attempted this exam.")
        return redirect("results_list")

    questions = list(exam.questions.all())
    if not questions:
        messages.error(request, "This exam has no questions yet.")
        return redirect("exam_list")

    if request.method == "POST":
        form = TakeExamForm(request.POST, questions=questions)
        if form.is_valid():
            total_marks = sum(q.marks for q in questions)
            score = 0
            computed_answers = []
            for q in questions:
                selected = form.cleaned_data[f"question_{q.id}"]
                is_correct = selected == q.correct_option
                marks_awarded = q.marks if is_correct else 0
                score += marks_awarded
                computed_answers.append((q, selected, is_correct, marks_awarded))

            percentage = Decimal("0.00")
            if total_marks > 0:
                percentage = (Decimal(score) * Decimal("100") / Decimal(total_marks)).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
                )

            try:
                with transaction.atomic():
                    result = Result.objects.create(
                        student=request.user,
                        exam=exam,
                        score=score,
                        total_marks=total_marks,
                        percentage=percentage,
                    )
                    ResultAnswer.objects.bulk_create(
                        [
                            ResultAnswer(
                                result=result,
                                question=q,
                                selected_option=selected,
                                is_correct=is_correct,
                                marks_awarded=marks_awarded,
                            )
                            for (q, selected, is_correct, marks_awarded) in computed_answers
                        ]
                    )
            except IntegrityError:
                messages.info(request, "You have already attempted this exam.")
                return redirect("results_list")

            messages.success(request, "Exam submitted successfully.")
            return redirect("result_detail", result_id=result.id)
    else:
        form = TakeExamForm(questions=questions)

    return render(request, "exams/take_exam.html", {"exam": exam, "form": form, "questions": questions})


@student_required
def results_list(request):
    results = Result.objects.filter(student=request.user).select_related("exam")
    return render(request, "exams/results_list.html", {"results": results})


@login_required
def result_detail(request, result_id: int):
    result = get_object_or_404(Result.objects.select_related("student", "exam"), id=result_id)
    is_admin = getattr(request.user, "role", None) == "ADMIN"
    if not is_admin and result.student_id != request.user.id:
        return HttpResponseForbidden("You are not allowed to view this result.")

    answers = result.answers.select_related("question").all()
    return render(request, "exams/result_detail.html", {"result": result, "answers": answers})


@admin_required
def admin_exam_list(request):
    exams = Exam.objects.all().order_by("-created_at")
    return render(request, "exams/admin/exam_list.html", {"exams": exams})


@admin_required
def admin_exam_create(request):
    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam created.")
            return redirect("admin_exam_list")
    else:
        form = ExamForm()
    return render(request, "exams/admin/exam_form.html", {"form": form, "title": "Create Exam"})


@admin_required
def admin_exam_edit(request, exam_id: int):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == "POST":
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam updated.")
            return redirect("admin_exam_list")
    else:
        form = ExamForm(instance=exam)
    return render(request, "exams/admin/exam_form.html", {"form": form, "title": "Edit Exam"})


@admin_required
def admin_exam_delete(request, exam_id: int):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == "POST":
        exam.delete()
        messages.success(request, "Exam deleted.")
        return redirect("admin_exam_list")
    return render(request, "exams/admin/exam_confirm_delete.html", {"exam": exam})


@admin_required
def admin_exam_toggle(request, exam_id: int):
    exam = get_object_or_404(Exam, id=exam_id)
    exam.is_active = not exam.is_active
    exam.save(update_fields=["is_active"])
    messages.success(request, "Exam status updated.")
    return redirect("admin_exam_list")


@admin_required
def admin_question_list(request, exam_id: int):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    return render(request, "exams/admin/question_list.html", {"exam": exam, "questions": questions})


@admin_required
def admin_question_create(request, exam_id: int):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            messages.success(request, "Question added.")
            return redirect("admin_question_list", exam_id=exam.id)
    else:
        form = QuestionForm()
    return render(
        request,
        "exams/admin/question_form.html",
        {"form": form, "exam": exam, "title": "Add Question"},
    )


@admin_required
def admin_question_edit(request, question_id: int):
    question = get_object_or_404(Question.objects.select_related("exam"), id=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question updated.")
            return redirect("admin_question_list", exam_id=question.exam_id)
    else:
        form = QuestionForm(instance=question)
    return render(
        request,
        "exams/admin/question_form.html",
        {"form": form, "exam": question.exam, "title": "Edit Question"},
    )


@admin_required
def admin_question_delete(request, question_id: int):
    question = get_object_or_404(Question.objects.select_related("exam"), id=question_id)
    if request.method == "POST":
        exam_id = question.exam_id
        question.delete()
        messages.success(request, "Question deleted.")
        return redirect("admin_question_list", exam_id=exam_id)
    return render(request, "exams/admin/question_confirm_delete.html", {"question": question})


@admin_required
def admin_results_list(request):
    results = Result.objects.select_related("student", "exam").order_by("-attempted_at")
    summary = (
        results.values("exam_id", "exam__title")
        .annotate(total_attempts=Count("id"), avg_score=Avg("score"), avg_percentage=Avg("percentage"))
        .order_by("-total_attempts", "exam__title")
    )
    return render(request, "exams/admin/results_list.html", {"results": results, "summary": summary})

