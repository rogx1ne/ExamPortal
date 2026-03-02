# Generated manually for initial project scaffold.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Exam",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(db_index=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("total_marks", models.PositiveIntegerField()),
                ("duration_minutes", models.PositiveIntegerField(help_text="Duration in minutes")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question_text", models.TextField()),
                ("option_a", models.CharField(max_length=255)),
                ("option_b", models.CharField(max_length=255)),
                ("option_c", models.CharField(max_length=255)),
                ("option_d", models.CharField(max_length=255)),
                ("correct_option", models.CharField(choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")], max_length=1)),
                ("marks", models.PositiveIntegerField(default=1)),
                (
                    "exam",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="questions", to="exams.exam"),
                ),
            ],
            options={"ordering": ["id"]},
        ),
        migrations.CreateModel(
            name="Result",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("score", models.PositiveIntegerField()),
                ("total_marks", models.PositiveIntegerField()),
                ("percentage", models.DecimalField(decimal_places=2, max_digits=6)),
                ("attempted_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "exam",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="results", to="exams.exam"),
                ),
                (
                    "student",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="results", to="accounts.user"),
                ),
            ],
            options={"ordering": ["-attempted_at"]},
        ),
        migrations.CreateModel(
            name="ResultAnswer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("selected_option", models.CharField(choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")], max_length=1)),
                ("is_correct", models.BooleanField(default=False)),
                ("marks_awarded", models.PositiveIntegerField(default=0)),
                (
                    "question",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="result_answers", to="exams.question"),
                ),
                (
                    "result",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="answers", to="exams.result"),
                ),
            ],
        ),
        migrations.AddIndex(model_name="exam", index=models.Index(fields=["is_active", "created_at"], name="exams_exam_is_acti_2efcf6_idx")),
        migrations.AddConstraint(model_name="result", constraint=models.UniqueConstraint(fields=("student", "exam"), name="unique_student_exam_attempt")),
        migrations.AddIndex(model_name="result", index=models.Index(fields=["exam", "attempted_at"], name="exams_resul_exam_id_474359_idx")),
        migrations.AddIndex(model_name="result", index=models.Index(fields=["student", "attempted_at"], name="exams_resul_student_801c6a_idx")),
        migrations.AddConstraint(model_name="resultanswer", constraint=models.UniqueConstraint(fields=("result", "question"), name="unique_answer_per_question_per_result")),
    ]

