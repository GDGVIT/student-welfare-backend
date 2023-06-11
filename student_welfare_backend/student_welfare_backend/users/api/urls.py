from django.urls import path
from student_welfare_backend.users.api.views import (
    RegistrationView,
    LoginView,
    VerifyOTPView,
    RefreshOTPView,
    ResetPasswordView,
    VerifyResetPasswordOTPView,
)
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "users"

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify_account/", VerifyOTPView.as_view(), name="verify_account"),
    path("refresh_otp/", RefreshOTPView.as_view(), name="refresh_otp"),
    path("refresh_token/", TokenRefreshView.as_view(), name="refresh_token"),
    path("reset_password/", ResetPasswordView.as_view(), name="reset_password"),
    path(
        "verify_reset_password_otp/",
        VerifyResetPasswordOTPView.as_view(),
        name="verify_reset_password_otp",
    ),
]
