from django.conf import settings
from django.db import models


class Exam(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    total_marks = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_active", "created_at"]),
        ]

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    class Option(models.TextChoices):
        A = "A", "A"
        B = "B", "B"
        C = "C", "C"
        D = "D", "D"

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=Option.choices)
    marks = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.exam.title}: {self.question_text[:60]}"


class Result(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="results")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="results")
    score = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    percentage = models.DecimalField(max_digits=6, decimal_places=2)
    attempted_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-attempted_at"]
        constraints = [
            models.UniqueConstraint(fields=["student", "exam"], name="unique_student_exam_attempt"),
        ]
        indexes = [
            models.Index(fields=["exam", "attempted_at"]),
            models.Index(fields=["student", "attempted_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.student} - {self.exam} ({self.score}/{self.total_marks})"


class ResultAnswer(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="result_answers")
    selected_option = models.CharField(max_length=1, choices=Question.Option.choices)
    is_correct = models.BooleanField(default=False)
    marks_awarded = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["result", "question"], name="unique_answer_per_question_per_result"),
        ]

    def __str__(self) -> str:
        return f"{self.result_id} - Q{self.question_id} ({self.selected_option})"

