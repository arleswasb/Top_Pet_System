# pets/serializers.py

from datetime import date

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from users.models import Profile

from .models import Pet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class PetSerializer(serializers.ModelSerializer):
    tutor_detail = UserSerializer(source="tutor", read_only=True)
    tutor = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True), write_only=True
    )
    idade = serializers.SerializerMethodField()
    foto = serializers.ImageField(
        required=False,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
    )

    class Meta:
        model = Pet
        fields = [
            "id",
            "nome",
            "especie",
            "raca",
            "idade",
            "data_de_nascimento",
            "sexo",
            "foto",
            "tutor",
            "tutor_detail",
        ]

    def get_idade(self, obj):
        if obj.data_de_nascimento:
            today = date.today()
            return (
                today.year
                - obj.data_de_nascimento.year
                - (
                    (today.month, today.day)
                    < (
                        obj.data_de_nascimento.month,
                        obj.data_de_nascimento.day,
                    )
                )
            )
        return None

    def validate_tutor(self, value):
        """Custom validation: only clients can be tutors"""
        if not hasattr(value, "profile"):
            raise serializers.ValidationError(
                "The selected user does not have an associated profile."
            )
        if value.profile.role != Profile.Role.CLIENTE:
            raise serializers.ValidationError("The tutor must be a client.")
        return value