from django.urls import path
from student_welfare_backend.users.api.views import (
    RegistrationView,
    LoginView,
    VerifyOTPView,
    RefreshOTPView,
    Ping,
)

app_name = "users"

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify_account/", VerifyOTPView.as_view(), name="verify_account"),
    path("refresh_otp/", RefreshOTPView.as_view(), name="refresh_otp"),
    path("ping/", Ping.as_view(), name="ping"),
]