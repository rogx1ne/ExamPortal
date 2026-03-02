from django import forms

from .models import Exam, Question


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ("title", "description", "total_marks", "duration_minutes", "is_active")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "total_marks": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "duration_minutes": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = (
            "question_text",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_option",
            "marks",
        )
        widgets = {
            "question_text": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "option_a": forms.TextInput(attrs={"class": "form-control"}),
            "option_b": forms.TextInput(attrs={"class": "form-control"}),
            "option_c": forms.TextInput(attrs={"class": "form-control"}),
            "option_d": forms.TextInput(attrs={"class": "form-control"}),
            "correct_option": forms.Select(attrs={"class": "form-select"}),
            "marks": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }


class TakeExamForm(forms.Form):
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if questions is None:
            questions = []

        for question in questions:
            field_name = f"question_{question.id}"
            self.fields[field_name] = forms.ChoiceField(
                label=question.question_text,
                choices=[
                    ("A", f"A) {question.option_a}"),
                    ("B", f"B) {question.option_b}"),
                    ("C", f"C) {question.option_c}"),
                    ("D", f"D) {question.option_d}"),
                ],
                widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
                required=True,
            )
