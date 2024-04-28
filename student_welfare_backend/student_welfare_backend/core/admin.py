from django.contrib import admin

from student_welfare_backend.core.models import Organization, Event, Spotlight, UserOrganizationRelation, Newsletter, FAQ, SpecialFile


# Register your models here.
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin for Organization model."""

    list_display = [
        "id",
        "name",
        "type",
        "sub_type",
    ]
    list_filter = ["type", "sub_type"]
    search_fields = ["name", "type", "sub_type"]


@admin.register(UserOrganizationRelation)
class UserOrganizationRelationAdmin(admin.ModelAdmin):
    """Admin for UserOrganizationRelation model."""

    list_display = [
        "id",
        "user",
        "organization",
        "role",
        "position"
    ]
    list_filter = ["role", "position"]
    search_fields = ["user__name", "organization__name", "role", "position"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin for Event model."""

    list_display = [
        "id",
        "name",
        "organizing_body",
        "start_time",
        "end_time",
    ]
    list_filter = ["organizing_body"]
    search_fields = ["name", "organizing_body__name"]


@admin.register(Spotlight)
class SpotlightAdmin(admin.ModelAdmin):
    """Admin for Spotlight model."""

    list_display = [
        "id",
        "name",
        "time",
        "hightlight_type",
    ]
    list_filter = ["name", "hightlight_type"]
    search_fields = ["name", "hightlight_type"]


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Admin for Newsletter model."""

    list_display = [
        "id",
        "year",
        "month",
        "link"
    ]
    list_filter = ["year", "month"]
    search_fields = ["year", "month"]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Admin for FAQ model."""

    list_display = [
        "id",
        "question",
        "answer"
    ]
    search_fields = ["question", "answer"]
    ordering = ["question"]


@admin.register(SpecialFile)
class SpecialFileAdmin(admin.ModelAdmin):
    """Admin for SpecialFile model."""

    list_display = [
        "id",
        "year",
        "type",
        "file_link"
    ]
    list_filter = ["year", "type"]
    search_fields = ["year", "type"]
    ordering = ["-year"]


