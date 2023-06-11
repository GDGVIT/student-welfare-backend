import csv
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
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
from student_welfare_backend.core.api.customs.pagination import CustomPagination
from student_welfare_backend.core.api.customs.permissions import IsDSW


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
    permission_classes = [IsAuthenticated, IsDSW]
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


class EventBulkUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDSW]

    @staticmethod
    def post(request):
        csv_file = request.FILES.get("file", None)
        if not csv_file:
            return Response(
                {"detail": "No file found"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not csv_file.name.endswith(".csv"):
            return Response(
                {"detail": "Invalid file type"}, status=status.HTTP_400_BAD_REQUEST
            )
        if csv_file.multiple_chunks():
            return Response(
                {"detail": "File too large"},
                status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            )

        responses = {
            "success": [],
            "failure": [],
        }

        reader = csv.reader(csv_file.read().decode("utf-8").splitlines())
        next(reader)
        for row in reader:
            if row[0] == "":
                continue
            if Event.objects.filter(name=row[0]).exists():
                continue

            if not Club.objects.filter(name=row[2]).exists():
                responses["failure"].append(
                    {"row": row[0], "detail": f"Club {row[2]} does not exist"}
                )
                continue

            event = Event.objects.create(
                name=row[0],
                description=row[1],
                organizing_body=Club.objects.get(name=row[2]),
                start_time=datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),
                end_time=datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S"),
                venue=row[5],
                poster_link=row[6],
            )

            if row[7] != "":
                event.event_coordinators.append(row[7])
            if row[8] != "":
                event.event_coordinators.append(row[8])

            responses["success"].append(
                {"row": row[0], "detail": f"Event {row[0]} created successfully"}
            )

        return Response(responses, status=status.HTTP_201_CREATED)
