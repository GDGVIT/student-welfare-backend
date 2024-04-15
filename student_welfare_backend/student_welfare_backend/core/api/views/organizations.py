from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend


from student_welfare_backend.core.models import Organization
from student_welfare_backend.core.api.serializers import (
    OrganizationSerializer,
    OrganizationDetailSerializer,
)
from student_welfare_backend.customs.pagination import CustomPagination
from student_welfare_backend.customs.permissions import IsDSW, IsADSW
from student_welfare_backend.customs.views import BaseBulkUploadView, BaseBulkDownloadView


class OrganizationsListView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def get(request):
        response = []
        for organization in Organization.objects.all():
            response.append(
                {
                    "id": organization.id,
                    "name": organization.name,
                }
            )
        return Response(response, status=status.HTTP_200_OK)


class OrganizationViewSet(ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Organization.objects.all()
    serializer_class = OrganizationDetailSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["type", "sub_type"]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]
    special_organization_types = ["student_welfare", "student_council", "greviance_cell", "counseling_division"]

    def get_serializer_class(self):
        if (self.action == "list") and (
            self.request.query_params.get("type", None) not in self.special_organization_types
        ):
            return OrganizationSerializer

        return OrganizationDetailSerializer


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

        organizations = Organization.objects.filter(type=organization_type).order_by("-name").all()
        if len(organizations) == 0:
            return Response(
                {"detail": "No such organizations found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            OrganizationDetailSerializer(organizations, many=True).data,
            status=status.HTTP_200_OK,
        )


class OrganizationAdminViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDSW | IsADSW]
    queryset = Organization.objects.all()
    serializer_class = OrganizationDetailSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["type", "sub_type"]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]
    special_organization_types = ["student_welfare", "student_council", "greviance_cell"]

    def get_serializer_class(self):
        if (self.action == "list") and (
            self.request.query_params.get("type", None) not in self.special_organization_types
        ):
            return OrganizationSerializer

        return OrganizationDetailSerializer


class OrganizationBulkUploadView(BaseBulkUploadView):
    csv_type = "organization"


class OrganizationBulkDownloadView(BaseBulkDownloadView):
    csv_type = "organization"
