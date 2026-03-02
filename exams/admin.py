from django.contrib import admin

from exam_portal.admin_site import admin_site

from .models import Exam, Question, Result, ResultAnswer


@admin.register(Exam, site=admin_site)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("title", "total_marks", "duration_minutes", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title",)


@admin.register(Question, site=admin_site)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("exam", "marks", "correct_option")
    list_filter = ("exam",)
    search_fields = ("question_text",)


@admin.register(Result, site=admin_site)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "exam", "score", "total_marks", "percentage", "attempted_at")
    list_filter = ("exam", "attempted_at")
    search_fields = ("student__username", "exam__title")


@admin.register(ResultAnswer, site=admin_site)
class ResultAnswerAdmin(admin.ModelAdmin):
    list_display = ("result", "question", "selected_option", "is_correct", "marks_awarded")
    list_filter = ("is_correct",)

