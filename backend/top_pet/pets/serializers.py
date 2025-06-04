from rest_framework import serializers
from .models import Pet
from django.contrib.auth.models import User

# Serializer para o modelo User (apenas para exibição simples do tutor)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username'] # Apenas para mostrar o ID e nome de usuário do tutor

# Serializer para o modelo Pet
class PetSerializer(serializers.ModelSerializer):
    # Campo 'tutor' para exibir informações detalhadas do User em vez do ID
    tutor = UserSerializer(read_only=True)
    
    class Meta:
        model = Pet
        # Inclua todos os campos que você quer que apareçam na API
        fields = ['id', 'nome', 'especie', 'raca', 'idade', 'data_de_nascimento', 'foto', 'tutor']
        read_only_fields = ['tutor'] # O tutor será definido pela lógica da view, não pelo usuário enviando dados
