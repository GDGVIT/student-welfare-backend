from rest_framework import serializers

from student_welfare_backend.core.models import (
    Event, 
    Organization, 
    UserOrganizationRelation, 
    Spotlight, 
    Newsletter, 
    FAQ, 
    SpecialFile,
)
from student_welfare_backend.users.api.serializers import UserDetailSerializer


class UserOrganizationRelationSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = UserOrganizationRelation
        fields = ["user", "role", "position"]


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "type",
            "sub_type",
            "logo_link",
        ]


class OrganizationDetailSerializer(serializers.ModelSerializer):
    chairperson = UserOrganizationRelationSerializer()
    faculty_coordinator = UserOrganizationRelationSerializer()
    board_members = UserOrganizationRelationSerializer(many=True)
    members = UserOrganizationRelationSerializer(many=True)

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "type",
            "sub_type",
            "chairperson",
            "faculty_coordinator",
            "board_members",
            "members",
        ]


class EventListSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = Event
        exclude = ["description", "event_coordinators"]


class EventDetailSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = Event
        fields = "__all__"


class SpotlightListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spotlight
        exclude = ["description"]


class SpotlightDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spotlight
        fields = "__all__"


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = "__all__"


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


class SpecialFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialFile
        fields = "__all__"