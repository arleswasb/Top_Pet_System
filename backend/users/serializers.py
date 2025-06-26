"""User serializers."""

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user."""

    password = serializers.CharField(write_only=True)

    class Meta:
        """Meta class."""

        model = User
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        )

    def create(self, validated_data):
        """Create a new user."""
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email", ""),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        Profile.objects.create(user=user, role=Profile.Role.CLIENTE)
        return user