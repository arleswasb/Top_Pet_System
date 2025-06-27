# pets/serializers.py

from rest_framework import serializers
from .models import Pet # Pet está em pets.models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from drf_spectacular.utils import extend_schema_field
from datetime import date
from users.models import Profile # <--- CORRIGIDO AQUI! Importe Profile de 'users.models'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class PetSerializer(serializers.ModelSerializer):
    tutor_detail = UserSerializer(source='tutor', read_only=True)
    tutor = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True),
        write_only=True,
        required=False
    )
    idade = serializers.SerializerMethodField()
    foto = serializers.ImageField(
        required=False,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )

    class Meta:
        model = Pet
        fields = [
            'id', 'nome', 'especie', 'raca',
            'idade', 'data_de_nascimento',
            'sexo',
            'foto',
            'observacoes',
            'tutor',
            'tutor_detail',
            'created_at',
            'updated_at'
        ]

    @extend_schema_field(serializers.IntegerField)
    def get_idade(self, obj) -> int:
        # A propriedade 'idade' já está definida no modelo Pet.
        # Não é necessário reimplementar aqui, a menos que você queira um comportamento diferente.
        # Se for o mesmo, pode remover este método e a asserção no teste.
        # No entanto, se o campo 'idade' no modelo for uma propriedade,
        # o SerializerMethodField é a forma correta de expô-lo via API.
        if obj.data_de_nascimento:
            today = date.today()
            return today.year - obj.data_de_nascimento.year - \
                   ((today.month, today.day) < (obj.data_de_nascimento.month, obj.data_de_nascimento.day))
        return None

    def validate_tutor(self, value):
        """Validação customizada: apenas clientes podem ser tutores"""
        if not hasattr(value, 'profile'):
            raise serializers.ValidationError("O usuário selecionado não possui um perfil associado.")
        # Agora Profile.Role.CLIENTE deve ser acessível corretamente
        if value.profile.role != Profile.Role.CLIENTE:
            raise serializers.ValidationError("O tutor deve ser um cliente.")
        return value