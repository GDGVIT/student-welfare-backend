from rest_framework import serializers

from student_welfare_backend.core.models import Event, Club, UserClubRelation,Spotlight


class UserClubRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClubRelation
        fields = ["user", "role"]


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
    chairperson = UserClubRelationSerializer
    faculty_coordinator = UserClubRelationSerializer
    board_members = UserClubRelationSerializer
    members = UserClubRelationSerializer

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
        model=Spotlight
        exclude=["description"]
        
class SpotlightDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Spotlight
        fields = "__all__"
    