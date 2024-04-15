from django.db.models import IntegerField
from django.db.models.functions import Cast
from rest_framework import status, filters
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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["year", "month"]
    search_fields = ["year", "month"]
    ordering_fields = ["year", "month"]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Custom ordering: Combine year and month into a numeric value for sorting
        queryset = queryset.annotate(
            year_as_int=Cast('year', IntegerField()),
            month_as_int=Cast('month', IntegerField())
        ).order_by('-year_as_int', '-month_as_int')
        
        return queryset


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



class NewsletterBulkUploadView(BaseBulkUploadView):
    csv_type = "newsletter"


class NewsletterBulkDownloadView(BaseBulkDownloadView):
    csv_type = "newsletter"