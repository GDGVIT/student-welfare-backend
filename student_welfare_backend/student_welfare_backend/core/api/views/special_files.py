from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend


from student_welfare_backend.core.models import SpecialFile
from student_welfare_backend.core.api.serializers import SpecialFileSerializer
from student_welfare_backend.customs.pagination import CustomPagination
from student_welfare_backend.customs.permissions import IsDSW, IsADSW


class SpecialFileViewSet(ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = SpecialFile.objects.all()
    serializer_class = SpecialFileSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["type"]
    search_fields = ["year", "type"]
    ordering_fields = ["year"]
    ordering = ["-year"]


class SpecialFileAdminViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDSW | IsADSW]
    queryset = SpecialFile.objects.all()
    serializer_class = SpecialFileSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["type"]
    search_fields = ["year", "type"]
    ordering_fields = ["year"]
    ordering = ["-year"]