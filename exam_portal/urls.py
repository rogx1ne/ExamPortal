from django.urls import path, include

from exam_portal.admin_site import admin_site


urlpatterns = [
    path("admin/", admin_site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("exams.urls")),
]
