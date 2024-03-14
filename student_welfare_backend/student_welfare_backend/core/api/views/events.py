from django.utils import timezone
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
from student_welfare_backend.customs.views import BaseBulkUploadView, BaseBulkDownloadView


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

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter based on query parameters
        filter_params = self.request.query_params
        if "upcoming" in filter_params:
            queryset = self.get_upcoming_events()
        elif "ongoing" in filter_params:
            queryset = self.get_ongoing_events()
        return queryset

    def get_upcoming_events(self):
        """
        Returns upcoming events.
        """
        print("Upcoming events")
        now = timezone.now()
        upcoming_events = self.queryset.filter(start_time__gt=now)
        return upcoming_events

    def get_ongoing_events(self):
        """
        Returns ongoing events.
        """
        print("Ongoing events")
        now = timezone.now()
        ongoing_events = self.queryset.filter(start_time__lte=now, end_time__gte=now)
        return ongoing_events


class EventAdminViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDSW | IsADSW]
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


class EventBulkDownloadView(BaseBulkDownloadView):
    csv_type = "event"