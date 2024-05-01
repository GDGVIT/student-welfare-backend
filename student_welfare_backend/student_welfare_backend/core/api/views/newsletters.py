import calendar

from django.db.models import Case, Value, IntegerField, When
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
from student_welfare_backend.customs.pagination import CustomPagination,NewsletterPagination
from student_welfare_backend.customs.permissions import IsDSW, IsADSW
from student_welfare_backend.customs.views import BaseBulkUploadView, BaseBulkDownloadView


class NewsletterViewSet(ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    pagination_class = NewsletterPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["year", "month"]
    search_fields = ["year", "month"]
    ordering_fields = ["year", "month"]
    
    def get_month_index(self, month_name):
        # Get the index (1-based) of the month name using calendar library
        months = {month.lower(): index for index, month in enumerate(calendar.month_name) if month}
        return months.get(month_name.lower())

    def get_queryset(self):
        queryset = super().get_queryset()
        # Custom sorting logic: Convert month names to numeric values
        queryset = queryset.annotate(
            month_index=Case(
                *[When(month__iexact=month_name, then=Value(self.get_month_index(month_name))) for month_name in calendar.month_name[1:]],  # start from index 1 to skip empty string at index 0
                default=Value(0), output_field=IntegerField()
            )
        )

        # Order queryset by year (descending) and month_index (descending)
        queryset = queryset.order_by('-year', '-month_index')
        return (queryset)


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