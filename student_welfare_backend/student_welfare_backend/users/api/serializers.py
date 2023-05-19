from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url", "is_faculty"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }



class UserLoginSerializer(serializers.ModelSerializer):
    # access_token = serializers.CharField()
    # refresh_token = serializers.CharField()

    class Meta:
        model = User
        fields = ["username", "name", "is_faculty", "verified"]