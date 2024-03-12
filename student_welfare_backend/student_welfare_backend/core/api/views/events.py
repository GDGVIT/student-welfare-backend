from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend


from student_welfare_backend.core.models import Event, Club
from student_welfare_backend.core.api.serializers import (
    EventListSerializer,
    EventDetailSerializer,
)
from student_welfare_backend.customs.pagination import CustomPagination
from student_welfare_backend.customs.permissions import IsDSW, IsADSW
from student_welfare_backend.customs.views import BaseBulkUploadView


class EventViewSet(ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["organizing_body__name", "venue", "start_time", "end_time"]
    search_fields = ["name", "organizing_body__name", "venue", "start_time", "end_time"]
    ordering_fields = [
        "name",
        "organizing_body__name",
        "venue",
        "start_time",
        "end_time",
    ]
    ordering = ["start_time"]

    def get_serializer_class(self):
        if self.action == "list":
            return EventListSerializer
        return EventDetailSerializer


class EventAdminViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDSW, IsADSW]
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter]
    earch_fields = ["name", "organizing_body__name", "venue", "start_time", "end_time"]
    ordering_fields = [
        "name",
        "organizing_body__name",
        "venue",
        "start_time",
        "end_time",
    ]
    ordering = ["start_time"]

    def get_serializer_class(self):
        if self.action == "list":
            return EventListSerializer
        return EventDetailSerializer


class EventBulkUploadView(BaseBulkUploadView):
    csv_type = "event"
