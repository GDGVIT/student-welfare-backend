from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from student_welfare_backend.users.forms import (
    UserAdminChangeForm,
    UserAdminCreationForm,
)
from student_welfare_backend.users.models import OTP

from django import forms
from django.contrib import messages
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from student_welfare_backend.sw_admin import sw_admin_site
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
                    "is_adsw",
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


# -----------------------------------------------------------------------------------


class VerifyOTPForm(forms.Form):
    otp_value = forms.CharField(label="Enter OTP", max_length=6)


class OTPVerificationMixin:
    @staticmethod
    def verify_otp(self, request, queryset):
        pass

    verify_otp.short_description = "Verify OTP"


class UserSWAdmin(auth_admin.UserAdmin, OTPVerificationMixin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "verified")}),
        (_("Personal info"), {"fields": ("name", "email", "phone_no")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_dsw",
                    "is_adsw",
                    "is_faculty",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "verified", "tenure"]
    search_fields = ["name", "tenure", "username"]
    actions = ["verify_otp"]

    def get_readonly_fields(self, request, obj=None):
        immutable_fields = ["groups", "user_permissions", "last_login", "date_joined", "is_superuser", "is_staff"]
        if request.user.is_dsw:
            return immutable_fields
        return ["is_dsw", "is_adsw", "is_faculty"] + immutable_fields

    # If User wants to save changes or delete use verify_otp action
    def change_view(self, request, object_id, form_url="", extra_context=None):
        print("Change view called")
        print(request)
        print(request.method)
        print(request.POST)
        if request.method == "POST":
            form = VerifyOTPForm(request.POST)
            if form.is_valid():
                otp_value = form.cleaned_data["otp_value"]
                print(otp_value)
                # Perform OTP verification logic here
                # Example:
                # if otp_value == valid_otp:
                #     perform_action()
                # else:
                #     return HttpResponseRedirect(reverse('admin:app_model_change', args=(object_id,)))
                #     # Redirect back to change form with the same object
                pass  # Placeholder for OTP verification logic
        else:
            form = VerifyOTPForm()

        extra_context = extra_context or {}
        extra_context["otp_form"] = form
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)


sw_admin_site.register(User, UserSWAdmin)
