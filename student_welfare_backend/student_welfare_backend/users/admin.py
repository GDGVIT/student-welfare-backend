from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from student_welfare_backend.users.forms import (
    UserAdminChangeForm,
    UserAdminCreationForm,
)
from student_welfare_backend.users.models import OTP

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password", "verified")}),
        (_("Personal info"), {"fields": ("name", "email", "phone_no")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_dsw",
                    "is_faculty",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_superuser", "verified", "tenure"]
    search_fields = ["name", "tenure", "username"]


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ["user", "value", "expiry_date", "action"]
    search_fields = ["user__name", "user__username"]
