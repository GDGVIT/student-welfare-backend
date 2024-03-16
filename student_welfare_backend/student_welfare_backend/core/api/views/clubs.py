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
from student_welfare_backend.customs.pagination import CustomPagination
from student_welfare_backend.customs.permissions import IsDSW, IsADSW
from student_welfare_backend.customs.views import BaseBulkUploadView, BaseBulkDownloadView


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
    filterset_fields = ["is_technical", "is_chapter", "type", "sub_type"]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.action == "list":
            return ClubSerializer
        return ClubDetailSerializer
    

class SpecialOrganizationsAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def get(request):
        organization_type = request.query_params.get("type", None)
        if organization_type is None:
            return Response(
                {"detail": "Please provide a type parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if organization_type not in ["student_welfare", "student_council", "greviance_cell"]:
            return Response(
                {"detail": "Invalid type parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        organizations = Club.objects.filter(type=organization_type).all()
        if len(organizations) == 0:
            return Response(
                {"detail": "No such organizations found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        organization = organizations[0]
        return Response(
            ClubDetailSerializer(organization).data,
            status=status.HTTP_200_OK,
        )


class ClubAdminViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDSW | IsADSW]
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


class ClubBulkUploadView(BaseBulkUploadView):
    csv_type = "club"

class ClubBulkDownloadView(BaseBulkDownloadView):
    csv_type = "club"