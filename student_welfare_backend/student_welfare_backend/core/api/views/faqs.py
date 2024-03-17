from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend


from student_welfare_backend.core.models import FAQ
from student_welfare_backend.core.api.serializers import FAQSerializer
from student_welfare_backend.customs.pagination import CustomPagination
from student_welfare_backend.customs.permissions import IsDSW, IsADSW


class FAQViewSet(ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["question", "answer"]
    ordering_fields = ["question"]
    ordering = ["question"]


class FAQAdminViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDSW | IsADSW]
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["question", "answer"]
    ordering_fields = ["question"]
    ordering = ["question"]