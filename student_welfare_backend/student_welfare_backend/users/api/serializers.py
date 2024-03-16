from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url", "is_faculty"]

        extra_kwargs = {"url": {"view_name": "api:user-detail", "lookup_field": "username"}}


class UserLoginSerializer(serializers.ModelSerializer):
    # access_token = serializers.CharField()
    # refresh_token = serializers.CharField()

    class Meta:
        model = User
        fields = ["username", "name", "is_faculty", "verified"]


class SWTeamSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
                  "username", 
                  "name",
                  "email", 
                  "phone_no", 
                  "is_faculty", 
                  "role",
                  "tenure",
                  ]
    
    def get_role(self, obj):
        if obj.is_dsw:
            return "dsw"
        elif obj.is_adsw:
            return "adsw"
        elif obj.is_faculty:
            return "faculty"
        else:
            return "student"

class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "email",
            "phone_no",
            "is_faculty",
            "verified",
            "tenure",
        ]


class UserAdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "email",
            "verified",
        ]
