from rest_framework import serializers
from .models import Pet
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class PetSerializer(serializers.ModelSerializer):
    tutor = UserSerializer(read_only=True)
    tutor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True),
        source='tutor',
        write_only=True,
        error_messages={
            'does_not_exist': 'O tutor especificado não existe ou está inativo.'
        }
    )
    idade = serializers.SerializerMethodField(read_only=True)
    foto = serializers.ImageField(
        required=False,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )

    class Meta:
        model = Pet
        fields = [
            'id', 'nome', 'especie', 'raca', 
            'idade', 'data_de_nascimento', 
            'foto', 'tutor', 'tutor_id'
        ]

    def get_idade(self, obj):
        if obj.data_de_nascimento:
            return (date.today() - obj.data_de_nascimento).days // 365
        return None

    def validate_tutor_id(self, value):
        """Validação customizada se necessário"""
        if value.profile.role != 'CL':  # Se quiser restringir a clientes
            raise serializers.ValidationError("O tutor deve ser um cliente.")
        return value