from django.test import Client
from django.urls import reverse

from accounts.models import User
from exams.models import Exam, Question, Result


def test_student_can_attempt_exam_only_once(db):
    user = User.objects.create_user(username="student1", password="pass12345")

    exam = Exam.objects.create(
        title="Sample",
        description="",
        total_marks=1,
        duration_minutes=10,
        is_active=True,
    )
    q = Question.objects.create(
        exam=exam,
        question_text="2+2?",
        option_a="3",
        option_b="4",
        option_c="5",
        option_d="6",
        correct_option=Question.Option.B,
        marks=1,
    )

    client = Client()
    client.force_login(user)

    url = reverse("take_exam", args=(exam.id,))
    res1 = client.post(url, data={f"question_{q.id}": "B"})
    assert res1.status_code == 302
    assert Result.objects.filter(student=user, exam=exam).count() == 1

    res2 = client.get(url)
    assert res2.status_code == 302
    assert Result.objects.filter(student=user, exam=exam).count() == 1
