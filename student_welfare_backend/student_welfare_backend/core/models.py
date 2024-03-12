from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from student_welfare_backend.users.models import User


# Create your models here.
class Club(models.Model):
    """
    Model containing all data relating various clubs and chapters
    """

    class Meta:
        verbose_name = "Club"
        verbose_name_plural = "Clubs"

    name = models.CharField(_("Name of club/chapter"), max_length=100, unique=True)
    is_chapter = models.BooleanField(_("Chapter"), default=False)
    is_technical = models.BooleanField(_("Technical"), default=False)

    @property
    def chairperson(self):
        return UserClubRelation.objects.filter(club=self, role="chairperson").first()

    @property
    def faculty_coordinator(self):
        return UserClubRelation.objects.filter(
            club=self, role="faculty_coordinator"
        ).first()

    @property
    def board_members(self):
        return UserClubRelation.objects.filter(club=self, role="board_member").all()

    @property
    def members(self):
        return UserClubRelation.objects.filter(club=self, role="member").all()

    def __str__(self):
        return f"{self.name}"


class UserClubRelation(models.Model):
    """
    Model containing all User-Club relationships
    """

    class Meta:
        verbose_name = "User Club relation"
        verbose_name_plural = "User Club relations"
        unique_together = ("user", "club")

    # Choices for club roles
    CLUB_ROLE_CHOICES = [
        ("faculty_coordinator", "Faculty Coordinator"),
        ("chairperson", "Chair Person"),
        ("board_member", "Board member"),
        ("member", "member"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_club_relations"
    )
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="user_club_relations"
    )
    role = models.CharField(choices=CLUB_ROLE_CHOICES, default="member", max_length=50)


class Event(models.Model):
    """
    Model containing all data regarding events
    """

    event_status = [
        ("approval_pending", "Approval Pending"),
        ("faculty_approved", "Faculty Approved"),
        ("approved", "Approved"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        unique_together = ("name", "organizing_body")

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    organizing_body = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="events"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    venue = models.CharField(max_length=50)
    poster_link = models.CharField(max_length=255, null=True, blank=True)
    event_coordinators = models.JSONField(default=list)
    status = models.CharField(
        max_length=50, choices=event_status, default="approval_pending"
    )

    def __str__(self):
        return f"{self.name}"


class Spotlight(models.Model):
    """
    Model containing all the data of the articles that appear in spotlight
    """
    
    class Meta:
        verbose_name = "Spotlight Highlights"
        verbose_name_plural = "Spotlight Highlights"
        
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    time = models.DateTimeField()
    hightlight_type=models.CharField(max_length=50)
        
        