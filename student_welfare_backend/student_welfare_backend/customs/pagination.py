from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from student_welfare_backend.core.models import Newsletter
from django.db.models import Min

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"
    max_page_size = 1000

class NewsletterPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"
    max_page_size = 1000

    def get_paginated_response(self, data):
        min_year = Newsletter.objects.aggregate(Min('year')).get('year__min')
        response = super().get_paginated_response(data)
        return Response({
            'min_year': min_year,
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })