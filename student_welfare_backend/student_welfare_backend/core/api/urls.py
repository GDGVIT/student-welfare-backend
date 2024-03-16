from django.urls import path
from rest_framework.routers import DefaultRouter
from student_welfare_backend.core.api.views.clubs import (
    ClubViewSet,
    SpecialOrganizationsAPIView,
    ClubAdminViewSet,
    ClubsListView,
    ClubBulkUploadView,
    ClubBulkDownloadView,
)
from student_welfare_backend.core.api.views.events import (
    EventViewSet,
    EventAdminViewSet,
    EventBulkUploadView,
    EventBulkDownloadView,
)
from student_welfare_backend.core.api.views.spotlights import (
    SpotlightViewSet,
    SpotlightAdminViewSet,
)
from student_welfare_backend.core.api.views.notifications import PushNotificationView

# URL PATTERNS
urlpatterns = [
    # LISTS
    path("clubs/titles/", ClubsListView.as_view(), name="clubs_titles"),
    path("special_organizations/", SpecialOrganizationsAPIView.as_view(), name="special_organizations"),
    # BULK UPLOAD
    path(
        "admin/clubs/bulk_upload/",
        ClubBulkUploadView.as_view(),
        name="clubs_bulk_upload",
    ),
    path(
        "admin/clubs/bulk_download/",
        ClubBulkDownloadView.as_view(),
        name="clubs_bulk_download",
    ),
    path(
        "admin/events/bulk_upload/",
        EventBulkUploadView.as_view(),
        name="events_bulk_upload",
    ),
    path(
        "admin/events/bulk_download/",
        EventBulkDownloadView.as_view(),
        name="events_bulk_download",
    ),
    # NOTIFICATIONS
    path(
        "admin/notifications/push/",
        PushNotificationView.as_view(),
        name="push_notification",
    ),
]

# CLUBS
club_router = DefaultRouter()
club_router.register(r"clubs", ClubViewSet, basename="clubs")
urlpatterns += club_router.urls

club_admin_router = DefaultRouter()
club_admin_router.register(r"admin/clubs", ClubAdminViewSet, basename="clubs_admin")
urlpatterns += club_admin_router.urls


# EVENTS
event_router = DefaultRouter()
event_router.register(r"events", EventViewSet, basename="events")
urlpatterns += event_router.urls

event_admin_router = DefaultRouter()
event_admin_router.register(r"admin/events", EventAdminViewSet, basename="events_admin")
urlpatterns += event_admin_router.urls

# SPOTLIGHT
spotlight_router = DefaultRouter()
spotlight_router.register(r"spotlights", SpotlightViewSet, basename="spotlights")
urlpatterns += spotlight_router.urls

spotlight_admin_router = DefaultRouter()
spotlight_admin_router.register(r"admin/spotlights", SpotlightAdminViewSet, basename="spotlights_admin")
urlpatterns += spotlight_admin_router.urls
