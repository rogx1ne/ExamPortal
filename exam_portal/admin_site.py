from django.contrib.admin import AdminSite


class ExamPortalAdminSite(AdminSite):
    site_header = "Online Examination Portal - Admin"
    site_title = "Exam Portal Admin"
    index_title = "Administration"

    def has_permission(self, request):
        user = request.user
        return bool(
            user.is_active
            and user.is_authenticated
            and user.is_staff
            and getattr(user, "role", None) == "ADMIN"
        )


admin_site = ExamPortalAdminSite(name="exam_portal_admin")

