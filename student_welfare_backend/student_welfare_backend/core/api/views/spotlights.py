from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from student_welfare_backend.core.models import Spotlight
from student_welfare_backend.core.api.serializers import (
    SpotlightListSerializer,
    SpotlightDetailSerializer,
)
from student_welfare_backend.customs.pagination import CustomPagination
from student_welfare_backend.customs.permissions import IsDSW


class SpotlightViewSet(ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Spotlight.objects.all()
    serializer_class = SpotlightDetailSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = [
        "name",
        "time",
    ]
    search_fields = ["name", "time"]
    ordering_fields = [
        "name",
        "time",
    ]
    ordering = ["time"]

    def get_serializer_class(self):
        if self.action == "list":
            return SpotlightListSerializer
        return SpotlightDetailSerializer


class SpotlightAdminViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDSW]
    queryset = Spotlight.objects.all()
    serializer_class = SpotlightDetailSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter]
    earch_fields = ["name", "time"]
    ordering_fields = [
        "name",
        "time",
    ]
    ordering = ["time"]

    def get_serializer_class(self):
        if self.action == "list":
            return SpotlightListSerializer
        return SpotlightDetailSerializer
