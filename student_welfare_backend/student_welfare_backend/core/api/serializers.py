from rest_framework import serializers

from student_welfare_backend.core.models import (
    Event, 
    Club, 
    UserClubRelation, 
    Spotlight, 
    Newsletter, 
    FAQ, 
    SpecialFile,
)
from student_welfare_backend.users.api.serializers import UserLoginSerializer


class UserClubRelationSerializer(serializers.ModelSerializer):
    user = UserLoginSerializer()

    class Meta:
        model = UserClubRelation
        fields = ["user", "role", "position"]


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = [
            "id",
            "name",
            "is_chapter",
            "is_technical",
        ]


class ClubDetailSerializer(serializers.ModelSerializer):
    chairperson = UserClubRelationSerializer()
    faculty_coordinator = UserClubRelationSerializer()
    board_members = UserClubRelationSerializer(many=True)
    members = UserClubRelationSerializer(many=True)

    class Meta:
        model = Club
        fields = [
            "id",
            "name",
            "is_chapter",
            "is_technical",
            "chairperson",
            "faculty_coordinator",
            "board_members",
            "members",
        ]


class EventListSerializer(serializers.ModelSerializer):
    organizing_body = ClubSerializer()

    class Meta:
        model = Event
        exclude = ["description", "event_coordinators"]


class EventDetailSerializer(serializers.ModelSerializer):
    organizing_body = ClubSerializer()

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