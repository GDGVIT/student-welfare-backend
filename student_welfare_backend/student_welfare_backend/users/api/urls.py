from django.urls import path
from rest_framework.routers import DefaultRouter
from student_welfare_backend.users.api.views import (
    RegistrationView,
    LoginView,
    VerifyOTPView,
    RefreshOTPView,
    ResetPasswordView,
    VerifyResetPasswordOTPView,
    UserAdminViewset,
    UserBulkUploadView,
    UserBulkDownloadView,
    UpdateFCMTokenView,
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
    path("admin/users/bulk_upload/", UserBulkUploadView.as_view(), name="user_bulk_upload"),
    path("admin/users/bulk_download/", UserBulkDownloadView.as_view(), name="user_bulk_download"),
    path("update_fcm_token/", UpdateFCMTokenView.as_view(), name="update_fcm_token"),
]

# USER ADMIN
user_admin_router = DefaultRouter()
user_admin_router.register(r"admin", UserAdminViewset, basename="users_admin")
urlpatterns += user_admin_router.urls