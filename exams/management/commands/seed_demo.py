from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from exams.models import Exam, Question, Result, ResultAnswer


@dataclass(frozen=True)
class DemoQuestion:
    text: str
    options: dict[str, str]
    correct: str
    marks: int = 1


@dataclass(frozen=True)
class DemoExam:
    title: str
    description: str
    duration_minutes: int
    total_marks: int
    is_active: bool
    questions: list[DemoQuestion]


DEMO_EXAMS: list[DemoExam] = [
    DemoExam(
        title="DEMO - Python Basics (MCQ)",
        description="Seeded demo exam for showcasing the portal.",
        duration_minutes=10,
        total_marks=5,
        is_active=True,
        questions=[
            DemoQuestion(
                text="Which keyword defines a function in Python?",
                options={"A": "func", "B": "def", "C": "function", "D": "lambda"},
                correct="B",
            ),
            DemoQuestion(
                text="What is the output of: print(2 ** 3)?",
                options={"A": "6", "B": "8", "C": "9", "D": "23"},
                correct="B",
            ),
            DemoQuestion(
                text="Which type is immutable?",
                options={"A": "list", "B": "dict", "C": "set", "D": "tuple"},
                correct="D",
            ),
            DemoQuestion(
                text="What does len('abc') return?",
                options={"A": "2", "B": "3", "C": "4", "D": "0"},
                correct="B",
            ),
            DemoQuestion(
                text="Which is a valid list literal?",
                options={"A": "(1,2,3)", "B": "{1,2,3}", "C": "[1,2,3]", "D": "<1,2,3>"},
                correct="C",
            ),
        ],
    ),
    DemoExam(
        title="DEMO - General Knowledge (MCQ)",
        description="Seeded demo exam for showcasing admin panel and analytics.",
        duration_minutes=8,
        total_marks=4,
        is_active=True,
        questions=[
            DemoQuestion(
                text="Which planet is known as the Red Planet?",
                options={"A": "Mars", "B": "Venus", "C": "Jupiter", "D": "Mercury"},
                correct="A",
            ),
            DemoQuestion(
                text="Water boils at what temperature (at sea level)?",
                options={"A": "50°C", "B": "90°C", "C": "100°C", "D": "120°C"},
                correct="C",
            ),
            DemoQuestion(
                text="Which is the largest ocean on Earth?",
                options={"A": "Atlantic", "B": "Indian", "C": "Pacific", "D": "Arctic"},
                correct="C",
            ),
            DemoQuestion(
                text="Which gas do plants absorb from the atmosphere?",
                options={"A": "Oxygen", "B": "Nitrogen", "C": "Carbon Dioxide", "D": "Helium"},
                correct="C",
            ),
        ],
    ),
    DemoExam(
        title="DEMO - Inactive Exam (Toggle Demo)",
        description="Seeded demo exam to demonstrate activate/deactivate.",
        duration_minutes=5,
        total_marks=2,
        is_active=False,
        questions=[
            DemoQuestion(
                text="This is an inactive exam question (demo). Pick A.",
                options={"A": "A", "B": "B", "C": "C", "D": "D"},
                correct="A",
            ),
            DemoQuestion(
                text="Second inactive demo question. Pick B.",
                options={"A": "A", "B": "B", "C": "C", "D": "D"},
                correct="B",
            ),
        ],
    ),
]


def _percent(score: int, total: int) -> Decimal:
    if total <= 0:
        return Decimal("0.00")
    return (Decimal(score) * Decimal("100") / Decimal(total)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class Command(BaseCommand):
    help = "Seed demo users/exams/questions/results for a quick invigilator-ready walkthrough."

    def add_arguments(self, parser) -> None:
        parser.add_argument("--admin-username", default="admin_demo")
        parser.add_argument("--admin-password", default="Admin@12345")
        parser.add_argument("--student-username", default="student_demo")
        parser.add_argument("--student-password", default="Student@12345")
        parser.add_argument(
            "--no-results", action="store_true", help="Do not create a sample Result/answers"
        )

    @transaction.atomic
    def handle(self, *args, **options) -> None:
        User = get_user_model()

        admin_username: str = options["admin_username"]
        admin_password: str = options["admin_password"]
        student_username: str = options["student_username"]
        student_password: str = options["student_password"]
        create_results = not bool(options["no_results"])

        admin, _ = User.objects.get_or_create(username=admin_username, defaults={"email": ""})
        admin.is_active = True
        admin.is_staff = True
        admin.is_superuser = True
        admin.role = "ADMIN"
        admin.set_password(admin_password)
        admin.save()

        student, _ = User.objects.get_or_create(username=student_username, defaults={"email": ""})
        student.is_active = True
        student.is_staff = False
        student.is_superuser = False
        student.role = "STUDENT"
        student.set_password(student_password)
        student.save()

        created_exams = 0
        created_questions = 0
        for demo_exam in DEMO_EXAMS:
            exam, exam_created = Exam.objects.get_or_create(
                title=demo_exam.title,
                defaults={
                    "description": demo_exam.description,
                    "total_marks": demo_exam.total_marks,
                    "duration_minutes": demo_exam.duration_minutes,
                    "is_active": demo_exam.is_active,
                },
            )
            if not exam_created:
                exam.description = demo_exam.description
                exam.total_marks = demo_exam.total_marks
                exam.duration_minutes = demo_exam.duration_minutes
                exam.is_active = demo_exam.is_active
                exam.save()
            else:
                created_exams += 1

            for q in demo_exam.questions:
                _, q_created = Question.objects.get_or_create(
                    exam=exam,
                    question_text=q.text,
                    defaults={
                        "option_a": q.options["A"],
                        "option_b": q.options["B"],
                        "option_c": q.options["C"],
                        "option_d": q.options["D"],
                        "correct_option": q.correct,
                        "marks": q.marks,
                    },
                )
                if q_created:
                    created_questions += 1

        if create_results:
            target_exam = Exam.objects.filter(title=DEMO_EXAMS[0].title).first()
            if (
                target_exam
                and not Result.objects.filter(student=student, exam=target_exam).exists()
            ):
                questions = list(target_exam.questions.all())
                total = sum(q.marks for q in questions)

                # Intentionally miss one answer to showcase non-100% results.
                score = 0
                answers_to_create: list[ResultAnswer] = []
                for idx, q in enumerate(questions):
                    selected = q.correct_option if idx != 0 else "A"
                    is_correct = selected == q.correct_option
                    marks_awarded = q.marks if is_correct else 0
                    score += marks_awarded
                    answers_to_create.append(
                        ResultAnswer(
                            question=q,
                            selected_option=selected,
                            is_correct=is_correct,
                            marks_awarded=marks_awarded,
                        )
                    )

                result = Result.objects.create(
                    student=student,
                    exam=target_exam,
                    score=score,
                    total_marks=total,
                    percentage=_percent(score, total),
                )
                for a in answers_to_create:
                    a.result = result
                ResultAnswer.objects.bulk_create(answers_to_create)

        self.stdout.write(self.style.SUCCESS("Demo data seeded."))
        self.stdout.write(
            f"Admin login: {admin_username} / {admin_password}  (dashboard: /accounts/dashboard/)"
        )
        self.stdout.write(
            f"Student login: {student_username} / {student_password}  (exams: /exams/)"
        )
