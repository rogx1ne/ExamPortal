from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("exams/", views.exam_list, name="exam_list"),
    path("exams/<int:exam_id>/start/", views.take_exam, name="take_exam"),
    path("results/", views.results_list, name="results_list"),
    path("results/<int:result_id>/", views.result_detail, name="result_detail"),
    # Admin panel (in-app)
    path("admin-panel/exams/", views.admin_exam_list, name="admin_exam_list"),
    path("admin-panel/exams/create/", views.admin_exam_create, name="admin_exam_create"),
    path("admin-panel/exams/<int:exam_id>/edit/", views.admin_exam_edit, name="admin_exam_edit"),
    path(
        "admin-panel/exams/<int:exam_id>/delete/", views.admin_exam_delete, name="admin_exam_delete"
    ),
    path(
        "admin-panel/exams/<int:exam_id>/toggle/", views.admin_exam_toggle, name="admin_exam_toggle"
    ),
    path(
        "admin-panel/exams/<int:exam_id>/questions/",
        views.admin_question_list,
        name="admin_question_list",
    ),
    path(
        "admin-panel/exams/<int:exam_id>/questions/add/",
        views.admin_question_create,
        name="admin_question_create",
    ),
    path(
        "admin-panel/questions/<int:question_id>/edit/",
        views.admin_question_edit,
        name="admin_question_edit",
    ),
    path(
        "admin-panel/questions/<int:question_id>/delete/",
        views.admin_question_delete,
        name="admin_question_delete",
    ),
    path("admin-panel/results/", views.admin_results_list, name="admin_results_list"),
]
