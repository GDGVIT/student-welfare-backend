from django.urls import path

from student_welfare_backend.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
)
from student_welfare_backend.users.api.views import CustromRegistrationView

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("register/", view=CustromRegistrationView.as_view(), name="register"),
]
