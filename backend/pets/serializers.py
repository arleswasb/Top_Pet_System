# pets/serializers.py

from rest_framework import serializers
from .models import Pet
from django.contrib.auth.models import User

# Serializer para o modelo User (apenas para exibição simples do tutor)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# Serializer para o modelo Pet
class PetSerializer(serializers.ModelSerializer):
    # Campo para LEITURA (GET): mostra os detalhes do tutor.
    tutor = UserSerializer(read_only=True)
    tutor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='tutor',
        write_only=True
    )

    class Meta:
        model = Pet
        # Adicione 'tutor_id' à lista de fields
        fields = ['id', 'nome', 'especie', 'raca', 'idade', 'data_de_nascimento', 'foto', 'tutor', 'tutor_id']