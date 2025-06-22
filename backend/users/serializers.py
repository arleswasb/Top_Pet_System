# users/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

# ... (seus outros serializers) ...

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        # Cria o usuário
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        # Cria o Profile associado com a role de CLIENTE
        Profile.objects.create(user=user, role=Profile.Role.CLIENTE)
        return user