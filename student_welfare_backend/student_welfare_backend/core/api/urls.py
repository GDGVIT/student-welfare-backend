from django.urls import path
from rest_framework.routers import DefaultRouter
from student_welfare_backend.core.api.views.clubs import ClubViewSet, ClubAdminViewSet, ClubsListView, ClubBulkUploadView
from student_welfare_backend.core.api.views.events import EventViewSet, EventAdminViewSet, EventBulkUploadView


# URL PATTERNS
urlpatterns = [
    # LISTS
    path("clubs/titles/", ClubsListView.as_view(), name="clubs_titles"),
    # BULK UPLOAD
    path('admin/clubs/bulk_upload/', ClubBulkUploadView.as_view(), name='clubs_bulk_upload'),
    path('admin/events/bulk_upload/', EventBulkUploadView.as_view(), name='events_bulk_upload'),
]

# CLUBS
club_router = DefaultRouter()
club_router.register(r'clubs', ClubViewSet, basename='clubs')
urlpatterns += club_router.urls

club_admin_router = DefaultRouter()
club_admin_router.register(r'admin/clubs', ClubAdminViewSet, basename='clubs_admin')
urlpatterns += club_admin_router.urls


# EVENTS
event_router = DefaultRouter()
event_router.register(r'events', EventViewSet, basename='events')
urlpatterns += event_router.urls

event_admin_router = DefaultRouter()
event_admin_router.register(r'admin/events', EventAdminViewSet, basename='events_admin')
urlpatterns += event_admin_router.urls