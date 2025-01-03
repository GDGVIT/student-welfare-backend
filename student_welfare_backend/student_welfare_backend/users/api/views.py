from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from student_welfare_backend.users.models import OTP
from student_welfare_backend.users.utils.otp import generate_otp
from student_welfare_backend.users.api.serializers import (
    UserLoginSerializer,
    UserAdminSerializer,
    UserAdminListSerializer,
)
from student_welfare_backend.customs.permissions import IsDSW, IsADSW
from student_welfare_backend.customs.views import BaseBulkUploadView, BaseBulkDownloadView


from student_welfare_backend.users.api.serializers import UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UpdateFCMTokenView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @staticmethod
    def post(request):
        fcm_token = request.data.get("fcm_token", None)

        if fcm_token == None:
            return Response(
                {"detail": "Please provide FCM token!"},
                status=HTTPStatus.BAD_REQUEST,
            )

        request.user.fcm_token = fcm_token
        request.user.save()

        return Response(
            {"detail": "FCM token updated successfully!"},
            status=HTTPStatus.OK,
        )

class RegistrationView(APIView):
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def post(request):
        username = request.data.get("username", None)
        name = request.data.get("name", None)
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        phone_no = request.data.get("phone_no", None)

        if any([username, name, email, password, phone_no]) is None:
            return Response(
                {"detail": "Please fill in all the fields!"},
                status=HTTPStatus.BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.password = make_password(password)
            user.save()
        else:
            user = User.objects.create_user(
                username=username,
                name=name,
                email=email,
                password=password,
                phone_no=phone_no,
            )

        if OTP.objects.filter(user=user).exists():
            OTP.objects.get(user=user).delete()

        otp = OTP.objects.create(user=user, value=generate_otp(), action="verify_account")
        message = f"OTP for verifying account is: {otp.value}. It will be active for 5 minutes."

        send_mail(
            "SWC: Verify email OTP",
            message,
            "noreply.sw@dscvit.com",
            recipient_list=[user.email],
            fail_silently=True,
        )

        return Response(
            {"detail": "OTP sent to email! Please verify account."},
            status=HTTPStatus.CREATED,
        )


class RefreshOTPView(APIView):
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def post(request):
        email = request.query_params.get("email", None)

        if email == None:
            return Response({"detail": "No email sent!"}, status=HTTPStatus.BAD_REQUEST)

        user = get_object_or_404(User, email=email)
        otp = get_object_or_404(OTP, user=user)
        otp.value = generate_otp()
        otp.expiry_date = otp.reset_expiry_date()
        otp.save()

        message = f"OTP for {otp.get_action_display()} is: {otp.value}. It will be active for 5 minutes."

        send_mail(
            f"SWC: {otp.get_action_display()} OTP",
            message,
            "noreply.sw@dscvit.com",
            recipient_list=[user.email],
            fail_silently=True,
        )

        return Response(
            {"detail": "OTP re-sent to email! Please verify account."},
            status=HTTPStatus.OK,
        )


class VerifyOTPView(APIView):
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def post(request):
        email = request.query_params.get("email", None)
        otp = request.data.get("otp")

        if email == None:
            return Response({"detail": "No email sent!"}, status=HTTPStatus.BAD_REQUEST)

        user = get_object_or_404(User, email=email)
        otp_object = get_object_or_404(OTP, user=user)

        if otp == otp_object.value:
            if otp_object.expiry_date > timezone.now():
                user.verified = True
                otp_object.delete()
                user.save()
            else:
                return Response(
                    {"detail": "OTP expired! Please generate a new OTP."},
                    status=HTTPStatus.BAD_REQUEST,
                )
        else:
            return Response({"detail": "Wrong OTP value."}, status=HTTPStatus.BAD_REQUEST)

        # Generate JWT refresh token for the user
        refresh_token = RefreshToken.for_user(user)

        serializer = UserLoginSerializer(user)
        # serializer.access_token = refresh_token.access_token
        # serializer.refresh_token = str(refresh_token)

        return Response(
            {
                "data": serializer.data,
                "access_token": str(refresh_token.access_token),
                "refresh_token": str(refresh_token),
            },
            status=HTTPStatus.OK,
        )


class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def post(request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"detail": "Email and password are required."},
                status=HTTPStatus.BAD_REQUEST,
            )

        user = get_object_or_404(User, email=email)

        if not user.check_password(password):
            return Response({"detail": "Incorrect password."}, status=HTTPStatus.BAD_REQUEST)

        if not user.verified:
            return Response(
                {"detail": "Please verify your account to login."},
                status=HTTPStatus.UNAUTHORIZED,
            )

        # Generate JWT refresh token for the user
        refresh_token = RefreshToken.for_user(user)

        serializer = UserLoginSerializer(user)
        serializer.access_token = refresh_token.access_token
        serializer.refresh_token = str(refresh_token)

        return Response(
            {
                "data": serializer.data,
                "access_token": str(refresh_token.access_token),
                "refresh_token": str(refresh_token),
            },
            status=HTTPStatus.OK,
        )


class ResetPasswordView(APIView):
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def post(request):
        email = request.data.get("email", None)

        if email == None:
            return Response({"detail": "Please enter email!"}, status=HTTPStatus.BAD_REQUEST)

        user = get_object_or_404(User, email=email)

        if user.verified == False:
            return Response(
                {"detail": "Please verify your account first!"},
                status=HTTPStatus.BAD_REQUEST,
            )

        if OTP.objects.filter(user=user).exists():
            OTP.objects.get(user=user).delete()
        otp = OTP.objects.create(user=user, value=generate_otp(), action="reset_password")
        message = f"OTP for resetting password is: {otp.value}. It will be active for 5 minutes."

        send_mail(
            f"SWC: {otp.get_action_display()} OTP",
            message,
            "noreply.sw@dscvit.com",
            recipient_list=[user.email],
            fail_silently=True,
        )

        return Response(
            {"detail": "OTP sent to email! Please verify account."},
            status=HTTPStatus.OK,
        )


class VerifyResetPasswordOTPView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        email = request.query_params.get("email", None)
        otp = request.data.get("otp")
        new_password = request.data.get("new_password")

        if email in [None, ""] or otp in [None, ""] or new_password in [None, ""]:
            return Response(
                {"detail": "Please enter all the fields!"},
                status=HTTPStatus.BAD_REQUEST,
            )

        user = get_object_or_404(User, email=email)
        otp_object = get_object_or_404(OTP, user=user)

        if otp == otp_object.value:
            if otp_object.expiry_date > timezone.now():
                user.password = make_password(new_password)
                otp_object.delete()
                user.save()
            else:
                return Response(
                    {"detail": "OTP expired! Please generate a new OTP."},
                    status=HTTPStatus.BAD_REQUEST,
                )
        else:
            return Response({"detail": "Wrong OTP value."}, status=HTTPStatus.BAD_REQUEST)

        return Response({"detail": "Password reset successful!"}, status=HTTPStatus.OK)


class UserAdminViewset(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsDSW | IsADSW]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["verified", "is_adsw", "is_dsw", "is_faculty"]
    search_fields = ["name", "email"]
    ordering_fields = ["name", "email"]

    def get_serializer_class(self):
        if self.action == "list":
            return UserAdminListSerializer
        return UserAdminSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter based on query parameters
        filter_params = self.request.query_params
        if "sw_team" in filter_params:
            queryset = self.get_sw_team()
        return queryset

    def get_sw_team(self):
        """
        Returns users with is_dsw or is_adsw
        """
        sw_team = self.queryset.filter(Q(is_dsw=True) | Q(is_adsw=True))
        return sw_team


class UserBulkUploadView(BaseBulkUploadView):
    csv_type = "user"


class UserBulkDownloadView(BaseBulkDownloadView):
    csv_type = "user"
