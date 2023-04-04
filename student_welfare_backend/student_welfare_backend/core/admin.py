from django.contrib import admin

from student_welfare_backend.core.models import Club, Event, UserClubRelation

# Register your models here.
@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Admin for Club model."""

    list_display = [
        "id",
        "name",
        "is_chapter",
        "is_technical",
    ]
    list_filter = ["is_chapter", "is_technical"]


@admin.register(UserClubRelation)
class UserClubRelationAdmin(admin.ModelAdmin):
    """Admin for UserClubRelation model."""

    list_display = [
        "id",
        "user",
        "club",
        "role",
    ]
    list_filter = ["role"]


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