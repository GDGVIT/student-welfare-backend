import csv

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend


from student_welfare_backend.core.models import Club
from student_welfare_backend.core.api.serializers import (
    ClubSerializer,
    ClubDetailSerializer,
)
from student_welfare_backend.core.api.customs.pagination import CustomPagination
from student_welfare_backend.core.api.customs.permissions import IsDSW


class ClubsListView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def get(request):
        response = []
        for club in Club.objects.all():
            response.append(
                {
                    "id": club.id,
                    "name": club.name,
                }
            )
        return Response(response, status=status.HTTP_200_OK)


class ClubViewSet(ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Club.objects.all()
    serializer_class = ClubDetailSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["is_technical", "is_chapter"]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.action == "list":
            return ClubSerializer
        return ClubDetailSerializer


class ClubAdminViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDSW]
    queryset = Club.objects.all()
    serializer_class = ClubDetailSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["is_technical", "is_chapter"]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.action == "list":
            return ClubSerializer
        return ClubDetailSerializer


class ClubBulkUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDSW]

    @staticmethod
    def post(request):
        csv_file = request.FILES.get("file", None)

        if not csv_file:
            return Response(
                {"error": "No file found"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not csv_file.name.endswith(".csv"):
            return Response(
                {"error": "Invalid file type"}, status=status.HTTP_400_BAD_REQUEST
            )
        if csv_file.multiple_chunks():
            return Response(
                {"error": "File too large"}, status=status.HTTP_400_BAD_REQUEST
            )

        responses = {
            "success": [],
            "failure": [],
        }

        reader = csv.reader(csv_file.read().decode("utf-8").splitlines())
        next(reader)

        for row in reader:
            if len(row) != 3:
                responses["failure"].append(
                    {"row": row, "error": "Invalid number of columns"}
                )
                continue

            print(row)
            name, is_chapter, is_technical = row

            is_chapter = is_chapter.lower().capitalize()
            is_technical = is_technical.lower().capitalize()

            if not name:
                responses["failure"].append(
                    {"row": row, "detail": "Name cannot be empty"}
                )
                continue
            if is_chapter not in ["True", "False"]:
                responses["failure"].append(
                    {"row": row, "detail": "Invalid value for is_chapter"}
                )
                continue
            if is_technical not in ["True", "False"]:
                responses["failure"].append(
                    {"row": row, "detail": "Invalid value for is_technical"}
                )
                continue
            if Club.objects.filter(name=name).exists():
                responses["failure"].append(
                    {"row": row, "detail": f"Club {name} already exists"}
                )
                continue

            club = Club.objects.create(
                name=name,
                is_chapter=True if is_chapter == "True" else False,
                is_technical=True if is_technical == "True" else False,
            )
            responses["success"].append(
                {"row": row, "detail": f"Club {name} created successfully"}
            )

        return Response(responses, status=status.HTTP_200_OK)
