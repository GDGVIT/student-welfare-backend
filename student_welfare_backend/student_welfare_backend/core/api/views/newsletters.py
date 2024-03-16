from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend


from student_welfare_backend.core.models import Newsletter
from student_welfare_backend.core.api.serializers import NewsletterSerializer
from student_welfare_backend.customs.pagination import CustomPagination
from student_welfare_backend.customs.permissions import IsDSW, IsADSW
from student_welfare_backend.customs.views import BaseBulkUploadView, BaseBulkDownloadView


class NewsletterViewSet(ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["year", "month"]
    search_fields = ["year", "month"]
    ordering_fields = ["year", "month"]
    ordering = ["-year", "-month"]


class NewsletterAdminViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDSW | IsADSW]
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["year", "month"]
    search_fields = ["year", "month"]
    ordering_fields = ["year", "month"]
    ordering = ["-year", "-month"]