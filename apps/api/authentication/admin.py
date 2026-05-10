"""
authentication/admin.py
-----------------------
Django admin configuration for the User model.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from authentication.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for the custom User model.

    Adapts Django’s default admin (designed for AbstractUser)
    to our custom User (AbstractBaseUser without username).
    """

    list_display = (
        "id",
        "email",
        "phone",
        "role",
        "is_active",
        "must_change_password",
        "created_at",
    )
    list_filter = ("role", "is_active", "must_change_password", "is_staff")
    search_fields = ("email", "phone", "id")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at", "last_login")

    # Fieldsets for the detail page
    fieldsets = (
        (None, {"fields": ("id", "email", "phone", "password")}),
        (_("Role & Permissions"), {
            "fields": ("role", "is_active", "is_staff", "is_superuser", "must_change_password"),
        }),
        (_("Groups & Permissions"), {
            "classes": ("collapse",),
            "fields": ("groups", "user_permissions"),
        }),
        (_("Dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )

    # Fieldsets for user creation
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone", "role", "password1", "password2", "is_active"),
        }),
    )

    # Replace username (non-existent) with email in admin forms
    # Django's UserAdmin expects a "username" field → we override behavior
    filter_horizontal = ("groups", "user_permissions")