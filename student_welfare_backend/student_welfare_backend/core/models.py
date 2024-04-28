import calendar
from bs4 import BeautifulSoup
from django.db import models
from django.db.models import Case, When, Value, CharField
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


from student_welfare_backend.users.models import User


# Create your models here.
class Organization(models.Model):
    """
    Model containing all data relating various clubs, chapters, teams and other organizations.
    """

    organization_type_choices = [
        ("student_welfare", "Student Welfare"),
        ("student_council", "Student Council"),
        ("club", "Club"),
        ("chapter", "Chapter"),
        ("team", "Team"),
        ("greviance_cell", "Greviance Cell"),
        ("counselling_division", "Counselling Division"),
        ("other", "Other"),
    ]

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    name = models.CharField(_("Name of Organization"), max_length=100, unique=True)
    logo_link = models.CharField(_("Logo link"), max_length=255, null=True, blank=True)
    type = models.CharField(_("Type"), max_length=50, choices=organization_type_choices, default="club")
    sub_type = models.CharField(_("Sub Type"), max_length=50, null=True, blank=True)
    description = models.TextField(_("Description"), null=True, blank=True)

    @property
    def chairperson(self):
        if UserOrganizationRelation.objects.filter(organization=self, role="chairperson").exists():
            return UserOrganizationRelation.objects.filter(organization=self, role="chairperson").first()
        return None

    @property
    def faculty_coordinator(self):
        if UserOrganizationRelation.objects.filter(organization=self, role="faculty_coordinator").exists():
            return UserOrganizationRelation.objects.filter(organization=self, role="faculty_coordinator").first()
        return None

    @property
    def board_members(self):
        return UserOrganizationRelation.objects.filter(organization=self, role="board_member").all()

    @property
    def members(self):
        members_queryset = UserOrganizationRelation.objects.filter(organization=self, role="member")
        if self.type == "student_welfare":
             # Define custom sorting order based on positions for student welfare organization members
            member_priority = {
                "Director, Students' Welfare": 1,
                # Add more positions and their priorities as needed
            }

            order_by_case = Case(
                *[When(position=pos, then=Value(priority)) for pos, priority in member_priority.items()],
                default=Value(999),  # Default value for any unknown positions
                output_field=CharField()
            )

            members_queryset = members_queryset.annotate(
                member_position_priority=order_by_case
            ).order_by('member_position_priority')
            
        return members_queryset.all()

    def __str__(self):
        return f"{self.name}"


class UserOrganizationRelation(models.Model):
    """
    Model containing all User-Organization relationships
    """

    class Meta:
        verbose_name = "User Organization relation"
        verbose_name_plural = "User Organization relations"
        unique_together = ("user", "organization")

    # Choices for organization roles
    ORGANIZATION_ROLE_CHOICES = [
        ("faculty_coordinator", "Faculty Coordinator"),
        ("chairperson", "Chair Person"),
        ("board_member", "Board member"),
        ("member", "member"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_organization_relations")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="user_organization_relations")
    role = models.CharField(choices=ORGANIZATION_ROLE_CHOICES, default="member", max_length=50)
    position = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.organization.name} - {self.user.name}"


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
    organizing_body = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="events")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    venue = models.CharField(max_length=50)
    poster_link = models.CharField(max_length=255, null=True, blank=True)
    event_coordinators = models.JSONField(default=list, blank=True, null=True)
    status = models.CharField(max_length=50, choices=event_status, default="approval_pending")

    def __str__(self):
        return f"{self.name}"


class Spotlight(models.Model):
    """
    Model containing all the data of the articles that appear in spotlight
    """

    hightlight_type_choices = [
        ("alert", "Alert"),
        ("event", "Event"),
    ]

    class Meta:
        verbose_name = "Spotlight Highlights"
        verbose_name_plural = "Spotlight Highlights"

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    time = models.DateTimeField()
    hightlight_type = models.CharField(max_length=50, choices=hightlight_type_choices, default="event")

    @property
    def sub_heading(self):
        # Convert html to normal text
        soup = BeautifulSoup(self.description, "html.parser")
        return soup.get_text()[:100]

    def __str__(self):
        return f"{self.name} - {self.time}"


class Newsletter(models.Model):
    """
    Model containing all the data of newsletters
    """

    month_names = [(month_name.lower(), month_name) for _, month_name in enumerate(calendar.month_name)][1:]

    class Meta:
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletters"
        unique_together = ("year", "month")

    year = models.CharField(
        max_length=4, validators=[RegexValidator(regex="^\d{4}$", message="Year must be 4 digits long")]
    )
    month = models.CharField(max_length=10, choices=month_names)
    cover_page = models.CharField(max_length=255, null=True, blank=True)
    link = models.CharField(max_length=255, null=True, blank=True)


class SpecialFile(models.Model):
    """
    Model containing all the data of special files
    """

    file_type_options = [
        ("events", "Events"),
        ("program_representatives", "Program Representatives"),
    ]

    class Meta:
        verbose_name = "Special File"
        verbose_name_plural = "Special Files"

    year = models.CharField(
        max_length=4, validators=[RegexValidator(regex="^\d{4}$", message="Year must be 4 digits long")]
    )
    type = models.CharField(max_length=100, choices=file_type_options)
    file_link = models.CharField(max_length=255)


class FAQ(models.Model):
    """
    Model containing all the data of FAQs
    """

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    question = models.CharField(max_length=255)
    answer = models.TextField()