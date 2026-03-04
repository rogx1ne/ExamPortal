from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from exam_portal.admin_site import admin_site

from .models import User


@admin.register(User, site=admin_site)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Role", {"fields": ("role",)}),)
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
