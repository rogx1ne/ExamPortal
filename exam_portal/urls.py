from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from exam_portal import views as portal_views
from exam_portal.admin_site import admin_site

urlpatterns = [
    path("admin/", admin_site.urls),
    path("accounts/", include("accounts.urls")),
    path("_health/", portal_views.health_check, name="health"),
    path("", include("exams.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
