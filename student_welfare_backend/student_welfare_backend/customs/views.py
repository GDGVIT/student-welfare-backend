from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from student_welfare_backend.customs.permissions import IsDSW, IsADSW
from student_welfare_backend.csv_handler.importer.csv_importer import CSVImporter
from student_welfare_backend.csv_handler.exporter import CSVExporter


class BaseAdminSWView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDSW | IsADSW]


class BaseBulkUploadView(BaseAdminSWView):
    importer_class = CSVImporter
    csv_type = None

    def post(self, request):
        csv_file = request.FILES.get("file")
        if not csv_file:
            return Response({"error": "No file found"}, status=status.HTTP_400_BAD_REQUEST)

        importer = self.importer_class(self.csv_type)
        success, responses = importer.process_csv(csv_file)
        
        if success:
            return Response(responses, status=status.HTTP_200_OK)
        else:
            return Response({"error": responses}, status=status.HTTP_400_BAD_REQUEST)


class BaseBulkDownloadView(BaseAdminSWView):
    exporter_class = CSVExporter
    csv_type = None

    def get(self, request):
        exporter = CSVExporter(self.csv_type)
        csv = exporter.export_csv(request.query_params.get("filter", {}))

        if type(csv) == dict:
            return Response(csv, status=status.HTTP_400_BAD_REQUEST)

       # Create an HTTP response with CSV data
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        # Write CSV data to the response
        response.write(csv.getvalue())
        return response