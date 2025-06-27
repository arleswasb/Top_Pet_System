# users/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

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
    """Serializer para auto-cadastro de usuários (público) - apenas CLIENTE"""
    
    # Redefinindo campos para adicionar help_text específico para auto-cadastro
    telefone = serializers.CharField(
        max_length=20, 
        required=False, 
        allow_blank=True,
        help_text="Telefone de contato (opcional)"
    )
    endereco = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text="Endereço residencial (opcional)"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove campos específicos de outros tipos de usuário
        self.fields.pop('role', None)
        self.fields.pop('crmv', None)  # CRMV só para veterinários
        self.fields.pop('especialidade', None)  # Especialidade só para veterinários
        
        # Atualizar help_text dos campos obrigatórios
        self.fields['username'].help_text = "Nome de usuário único (obrigatório)"
        self.fields['password'].help_text = "Senha com no mínimo 8 caracteres (obrigatório)"
        self.fields['confirm_password'].help_text = "Confirme a senha digitada (obrigatório)"
        self.fields['email'].help_text = "Email válido para contato (obrigatório)"
        self.fields['first_name'].help_text = "Primeiro nome (obrigatório)"
        self.fields['last_name'].help_text = "Sobrenome (obrigatório)"
        
    def validate(self, data):
        """Validação específica para auto-cadastro"""
        data = super().validate(data)
        # Força o role como CLIENTE para auto-cadastro
        data['role'] = Profile.Role.CLIENTE
        return data

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