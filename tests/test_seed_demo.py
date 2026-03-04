from django.core.management import call_command

from accounts.models import User
from exams.models import Exam, Question, Result, ResultAnswer


def test_seed_demo_idempotent_creates_expected_objects(db):
    call_command("seed_demo")

    admin = User.objects.get(username="admin_demo")
    assert admin.role == "ADMIN"
    assert admin.is_staff is True
    assert admin.is_superuser is True

    student = User.objects.get(username="student_demo")
    assert student.role == "STUDENT"
    assert student.is_staff is False
    assert student.is_superuser is False

    assert Exam.objects.filter(title__startswith="DEMO - ").count() >= 3
    assert Question.objects.filter(exam__title__startswith="DEMO - ").count() >= 1

    python_exam = Exam.objects.get(title="DEMO - Python Basics (MCQ)")
    assert Result.objects.filter(student=student, exam=python_exam).count() == 1
    assert ResultAnswer.objects.filter(result__student=student, result__exam=python_exam).exists()

    exams_count = Exam.objects.count()
    questions_count = Question.objects.count()
    results_count = Result.objects.count()
    answers_count = ResultAnswer.objects.count()

    # Running again should not create duplicates.
    call_command("seed_demo")

    assert Exam.objects.count() == exams_count
    assert Question.objects.count() == questions_count
    assert Result.objects.count() == results_count
    assert ResultAnswer.objects.count() == answers_count


def test_seed_demo_no_results_option(db):
    call_command("seed_demo", "--no-results")
    student = User.objects.get(username="student_demo")
    assert Result.objects.filter(student=student).count() == 0
