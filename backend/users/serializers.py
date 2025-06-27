# users/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer para o perfil do usuário"""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = Profile
        fields = ['role', 'role_display', 'telefone', 'endereco', 'crmv', 'especialidade']
        
    def validate(self, data):
        """Validação personalizada para campos específicos de veterinário"""
        role = data.get('role')
        crmv = data.get('crmv')
        
        if role == Profile.Role.VETERINARIO and not crmv:
            raise serializers.ValidationError({
                'crmv': 'CRMV é obrigatório para veterinários.'
            })
        
        return data

class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer base para criação de usuários"""
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=Profile.Role.choices, default=Profile.Role.CLIENTE)
    telefone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    endereco = serializers.CharField(required=False, allow_blank=True)
    crmv = serializers.CharField(max_length=20, required=False, allow_blank=True)
    especialidade = serializers.CharField(max_length=100, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username', 'password', 'confirm_password', 'email', 
            'first_name', 'last_name', 'role', 'telefone', 
            'endereco', 'crmv', 'especialidade'
        ]
        
    def validate(self, data):
        """Validação de senha e campos específicos"""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'As senhas não coincidem.'
            })
        
        # Validação para veterinários
        if data.get('role') == Profile.Role.VETERINARIO and not data.get('crmv'):
            raise serializers.ValidationError({
                'crmv': 'CRMV é obrigatório para veterinários.'
            })
            
        return data

    def create(self, validated_data):
        # Remove campos que não pertencem ao modelo User
        profile_data = {
            'role': validated_data.pop('role', Profile.Role.CLIENTE),
            'telefone': validated_data.pop('telefone', ''),
            'endereco': validated_data.pop('endereco', ''),
            'crmv': validated_data.pop('crmv', ''),
            'especialidade': validated_data.pop('especialidade', ''),
        }
        
        # Remove confirm_password
        validated_data.pop('confirm_password')
        
        # Cria o usuário
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Cria o Profile associado (verifica se já existe)
        profile, created = Profile.objects.get_or_create(user=user, defaults=profile_data)
        if not created:
            # Se já existe, atualiza os dados
            for key, value in profile_data.items():
                setattr(profile, key, value)
            profile.save()
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer para visualização completa do usuário"""
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_active', 'date_joined', 'profile'
        ]
        read_only_fields = ['id', 'username', 'date_joined']


class UserAdminSerializer(serializers.ModelSerializer):
    """Serializer para operações administrativas de usuários"""
    profile = ProfileSerializer()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'is_active', 'date_joined', 'profile'
        ]
        read_only_fields = ['id', 'username', 'date_joined']
        
    def update(self, instance, validated_data):
        """Atualiza usuário e perfil"""
        profile_data = validated_data.pop('profile', {})
        
        # Atualiza dados do usuário
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Atualiza dados do perfil
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance

class UserSelfRegisterSerializer(UserCreateSerializer):
    """
    Serializer para auto-cadastro de usuários (público) - apenas CLIENTE
    
    CAMPOS OBRIGATÓRIOS: username, password, confirm_password, email, first_name, last_name
    CAMPOS OPCIONAIS: telefone, endereco
    """
    
    # Redefinindo campos para adicionar help_text específico para auto-cadastro
    username = serializers.CharField(
        max_length=150,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Nome de usuário único no sistema",
        style={'placeholder': 'Digite seu nome de usuário'}
    )
    password = serializers.CharField(
        write_only=True, 
        min_length=8,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Senha com no mínimo 8 caracteres",
        style={'input_type': 'password', 'placeholder': 'Digite sua senha'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Confirme a senha digitada",
        style={'input_type': 'password', 'placeholder': 'Confirme sua senha'}
    )
    email = serializers.EmailField(
        required=True,
        help_text="🔴 OBRIGATÓRIO: Email válido para contato",
        style={'placeholder': 'exemplo@email.com'}
    )
    first_name = serializers.CharField(
        max_length=150,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Primeiro nome",
        style={'placeholder': 'João'}
    )
    last_name = serializers.CharField(
        max_length=150,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Sobrenome",
        style={'placeholder': 'Silva'}
    )
    telefone = serializers.CharField(
        max_length=20, 
        required=False, 
        allow_blank=True,
        allow_null=True,
        help_text="⚪ OPCIONAL: Telefone de contato (pode ficar em branco)",
        style={'placeholder': '(11) 99999-9999'}
    )
    endereco = serializers.CharField(
        required=False, 
        allow_blank=True,
        allow_null=True,
        help_text="⚪ OPCIONAL: Endereço residencial (pode ficar em branco)",
        style={'placeholder': 'Rua das Flores, 123, São Paulo'}
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'password', 'confirm_password', 'email', 
            'first_name', 'last_name', 'telefone', 'endereco'
        ]
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'telefone': {'required': False},
            'endereco': {'required': False},
        }
        
    def validate(self, data):
        """Validação específica para auto-cadastro"""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'As senhas não coincidem.'
            })
        # Força o role como CLIENTE para auto-cadastro
        data['role'] = Profile.Role.CLIENTE
        return data
    
    def create(self, validated_data):
        """Cria usuário e perfil para auto-cadastro"""
        from django.db import IntegrityError
        from rest_framework import serializers as drf_serializers
        
        # Remove campos que não são do modelo User
        confirm_password = validated_data.pop('confirm_password', None)
        telefone = validated_data.pop('telefone', '')
        endereco = validated_data.pop('endereco', '')
        role = validated_data.pop('role', Profile.Role.CLIENTE)
        
        try:
            # Cria o usuário
            user = User.objects.create_user(**validated_data)
            
            # Cria o perfil
            Profile.objects.create(
                user=user,
                role=role,
                telefone=telefone,
                endereco=endereco
            )
            
            return user
        except IntegrityError:
            # Se houver erro de integridade (username duplicado), levanta ValidationError
            raise drf_serializers.ValidationError({
                'username': 'Este nome de usuário já existe.'
            })

class UserFuncionarioCreateSerializer(UserCreateSerializer):
    """Serializer para funcionários criarem usuários - CLIENTE, FUNCIONARIO ou VETERINARIO"""
    
    def validate_role(self, value):
        """Funcionários podem criar: CLIENTE, FUNCIONARIO, VETERINARIO"""
        allowed_roles = [Profile.Role.CLIENTE, Profile.Role.FUNCIONARIO, Profile.Role.VETERINARIO]
        if value not in allowed_roles:
            raise serializers.ValidationError(
                f"Funcionários só podem criar usuários dos tipos: {', '.join(allowed_roles)}"
            )
        return value

class UserAdminCreateSerializer(UserCreateSerializer):
    """Serializer para administradores criarem usuários - todos os tipos"""
    
    def validate_role(self, value):
        """Administradores podem criar qualquer tipo de usuário"""
        # Sem restrições para administradores
        return value