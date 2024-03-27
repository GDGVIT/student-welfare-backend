from django.urls import path
from rest_framework.routers import DefaultRouter
from student_welfare_backend.core.api.views.organizations import (
    OrganizationViewSet,
    SpecialOrganizationsAPIView,
    OrganizationAdminViewSet,
    OrganizationsListView,
    OrganizationBulkUploadView,
    OrganizationBulkDownloadView,
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
from student_welfare_backend.core.api.views.newsletters import (
    NewsletterViewSet,
    NewsletterAdminViewSet,
    NewsletterBulkUploadView,
    NewsletterBulkDownloadView
)
from student_welfare_backend.core.api.views.faqs import (
    FAQViewSet, 
    FAQAdminViewSet,
)
from student_welfare_backend.core.api.views.special_files import (
    SpecialFileViewSet,
    SpecialFileAdminViewSet,
    SpecialFilesBulkUploadView,
    SpecialFilesBulkDownloadView
)
from student_welfare_backend.core.api.views.notifications import PushNotificationView

# URL PATTERNS
urlpatterns = [
    # LISTS
    path("organizations/titles/", OrganizationsListView.as_view(), name="organizations_titles"),
    path("special_organizations/", SpecialOrganizationsAPIView.as_view(), name="special_organizations"),
    # BULK UPLOAD
    path(
        "admin/organizations/bulk_upload/",
        OrganizationBulkUploadView.as_view(),
        name="organizations_bulk_upload",
    ),
    path(
        "admin/organizations/bulk_download/",
        OrganizationBulkDownloadView.as_view(),
        name="organizations_bulk_download",
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
    path(
        "admin/newsletters/bulk_upload/",
        NewsletterBulkUploadView.as_view(),
        name="newsletters_bulk_upload",

    ),
    path(
        "admin/newsletters/bulk_download/",
        NewsletterBulkDownloadView.as_view(),
        name="newsletters_bulk_download",
    ),
    path(
        "admin/special_files/bulk_upload/",
        SpecialFilesBulkUploadView.as_view(),
        name="special_files_bulk_upload",
    ),
    path(
        "admin/special_files/bulk_download/",
        SpecialFilesBulkDownloadView.as_view(),
        name="special_files_bulk_download",
    ),
    # NOTIFICATIONS
    path(
        "admin/notifications/push/",
        PushNotificationView.as_view(),
        name="push_notification",
    ),
]


# ORGANIZATIONS
organization_router = DefaultRouter()
organization_router.register(r"organizations", OrganizationViewSet, basename="organizations")
urlpatterns += organization_router.urls

organization_admin_router = DefaultRouter()
organization_admin_router.register(r"admin/organizations", OrganizationAdminViewSet, basename="organizations_admin")
urlpatterns += organization_admin_router.urls


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


# NEWSLETTER
newsletter_router = DefaultRouter()
newsletter_router.register(r"newsletters", NewsletterViewSet, basename="newsletters")
urlpatterns += newsletter_router.urls

newsletter_admin_router = DefaultRouter()
newsletter_admin_router.register(r"admin/newsletters", NewsletterAdminViewSet, basename="newsletters_admin")
urlpatterns += newsletter_admin_router.urls


# FAQ
faq_router = DefaultRouter()
faq_router.register(r"faqs", FAQViewSet, basename="faqs")
urlpatterns += faq_router.urls

faq_admin_router = DefaultRouter()
faq_admin_router.register(r"admin/faqs", FAQAdminViewSet, basename="faqs_admin")
urlpatterns += faq_admin_router.urls


# SPECIAL FILES
special_file_router = DefaultRouter()
special_file_router.register(r"special_files", SpecialFileViewSet, basename="special_files")
urlpatterns += special_file_router.urls

special_file_admin_router = DefaultRouter()
special_file_admin_router.register(r"admin/special_files", SpecialFileAdminViewSet, basename="special_files_admin")
urlpatterns += special_file_admin_router.urls