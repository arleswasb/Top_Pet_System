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
    🌟 SERIALIZER PARA AUTO-CADASTRO DE USUÁRIOS (PÚBLICO) - APENAS CLIENTE
    
    Este endpoint permite que novos usuários se cadastrem no sistema como CLIENTE.
    Perfeito para donos de pets que querem agendar consultas.
    
    📋 EXEMPLO DE USO:
    {
        "username": "maria_silva",
        "password": "minhasenha123",
        "confirm_password": "minhasenha123",
        "email": "maria@email.com",
        "first_name": "Maria",
        "last_name": "Silva",
        "telefone": "(11) 99999-9999",
        "endereco": "Rua das Flores, 123, São Paulo - SP"
    }
    
    🎯 RESULTADO: Usuário criado automaticamente como CLIENTE, pronto para usar o sistema.
    """
    
    # ===============================
    # 🔴 CAMPOS OBRIGATÓRIOS
    # ===============================
    username = serializers.CharField(
        max_length=150,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Nome de usuário único no sistema. Será usado para fazer login.",
        style={
            'placeholder': 'Exemplo: maria_silva, joao123, ana_santos',
            'input_type': 'text'
        }
    )
    
    password = serializers.CharField(
        write_only=True, 
        min_length=8,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Senha segura com no mínimo 8 caracteres. Use letras, números e símbolos.",
        style={
            'input_type': 'password', 
            'placeholder': 'Digite uma senha forte com 8+ caracteres'
        }
    )
    
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Digite a mesma senha para confirmar. Deve ser idêntica à senha acima.",
        style={
            'input_type': 'password', 
            'placeholder': 'Repita a senha digitada acima'
        }
    )
    
    email = serializers.EmailField(
        required=True,
        help_text="🔴 OBRIGATÓRIO: Email válido para contato e recuperação de senha. Exemplo: nome@provedor.com",
        style={
            'placeholder': 'Exemplo: maria@gmail.com, joao@outlook.com',
            'input_type': 'email'
        }
    )
    
    first_name = serializers.CharField(
        max_length=150,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Primeiro nome do usuário. Como você gostaria de ser chamado(a).",
        style={
            'placeholder': 'Exemplo: Maria, João, Ana, Carlos'
        }
    )
    
    last_name = serializers.CharField(
        max_length=150,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Sobrenome do usuário. Seu nome de família.",
        style={
            'placeholder': 'Exemplo: Silva, Santos, Oliveira, Pereira'
        }
    )
    
    # ===============================
    # ⚪ CAMPOS OPCIONAIS
    # ===============================
    telefone = serializers.CharField(
        max_length=20, 
        required=False, 
        allow_blank=True,
        allow_null=True,
        help_text="⚪ OPCIONAL: Telefone para contato (pode ficar em branco). Inclua DDD.",
        style={
            'placeholder': 'Exemplo: (11) 99999-9999, (21) 88888-8888'
        }
    )
    
    endereco = serializers.CharField(
        required=False, 
        allow_blank=True,
        allow_null=True,
        help_text="⚪ OPCIONAL: Endereço residencial completo (pode ficar em branco). Rua, número, bairro, cidade.",
        style={
            'base_template': 'textarea.html',
            'placeholder': 'Exemplo: Rua das Flores, 123, Centro, São Paulo - SP, CEP: 01234-567'
        }
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
            
            # Atualiza o perfil criado automaticamente pelo signal
            user.profile.role = role
            user.profile.telefone = telefone
            user.profile.endereco = endereco
            user.profile.save()
            
            return user
        except IntegrityError:
            # Se houver erro de integridade (username duplicado), levanta ValidationError
            raise drf_serializers.ValidationError({
                'username': 'Este nome de usuário já existe.'
            })

class UserFuncionarioCreateSerializer(UserCreateSerializer):
    """
    🌟 SERIALIZER PARA CRIAÇÃO DE USUÁRIOS POR FUNCIONÁRIOS
    
    Permite que funcionários do sistema criem novos usuários dos tipos:
    CLIENTE, FUNCIONARIO ou VETERINARIO
    
    📋 EXEMPLO DE USO:
    {
        "username": "novousuario",
        "password": "minhasenha123",
        "confirm_password": "minhasenha123",
        "email": "user@example.com",
        "first_name": "Maria",
        "last_name": "Santos",
        "role": "CLIENTE",
        "telefone": "(11) 88888-8888",
        "endereco": "Av. Principal, 456, São Paulo",
        "crmv": "SP-12345",
        "especialidade": "Clínica Geral"
    }
    
    💡 DICA: Para veterinários, o campo CRMV é obrigatório!
    """
    
    # ===============================
    # 🔴 CAMPOS OBRIGATÓRIOS
    # ===============================
    username = serializers.CharField(
        max_length=150,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Nome de usuário único no sistema para login",
        style={
            'placeholder': 'Exemplo: maria_silva, dr_joao, func_ana'
        }
    )
    
    password = serializers.CharField(
        write_only=True, 
        min_length=8,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Senha segura com no mínimo 8 caracteres",
        style={
            'input_type': 'password',
            'placeholder': 'Digite uma senha forte'
        }
    )
    
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Confirme a senha digitada acima",
        style={
            'input_type': 'password',
            'placeholder': 'Repita a senha'
        }
    )
    
    email = serializers.EmailField(
        required=True,
        help_text="🔴 OBRIGATÓRIO: Email válido para contato profissional",
        style={
            'placeholder': 'usuario@clinica.com.br'
        }
    )
    
    first_name = serializers.CharField(
        max_length=150,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Primeiro nome do usuário",
        style={
            'placeholder': 'Maria, João, Ana'
        }
    )
    
    last_name = serializers.CharField(
        max_length=150,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Sobrenome do usuário",
        style={
            'placeholder': 'Silva, Santos, Oliveira'
        }
    )
    
    # ===============================
    # 🟡 CAMPO TIPO DE USUÁRIO
    # ===============================
    role = serializers.ChoiceField(
        choices=[
            (Profile.Role.CLIENTE, "Cliente - Dono de pet"),
            (Profile.Role.FUNCIONARIO, "Funcionário - Atendente/Recepção"),
            (Profile.Role.VETERINARIO, "Veterinário - Profissional médico")
        ], 
        default=Profile.Role.CLIENTE,
        help_text="🟡 ESCOLHA: Tipo de usuário que será criado. Define as permissões no sistema.",
        style={
            'base_template': 'select.html'
        }
    )
    
    # ===============================
    # ⚪ CAMPOS OPCIONAIS - CONTATO
    # ===============================
    telefone = serializers.CharField(
        max_length=20, 
        required=False, 
        allow_blank=True,
        allow_null=True,
        help_text="⚪ OPCIONAL: Telefone de contato. Recomendado para funcionários e veterinários.",
        style={
            'placeholder': '(11) 99999-9999'
        }
    )
    
    endereco = serializers.CharField(
        required=False, 
        allow_blank=True,
        allow_null=True,
        help_text="⚪ OPCIONAL: Endereço residencial ou comercial completo",
        style={
            'base_template': 'textarea.html',
            'placeholder': 'Rua, número, bairro, cidade - estado'
        }
    )
    
    # ===============================
    # 🔵 CAMPOS ESPECÍFICOS VETERINÁRIOS
    # ===============================
    crmv = serializers.CharField(
        max_length=20, 
        required=False, 
        allow_blank=True,
        allow_null=True,
        help_text="🔵 VETERINÁRIO: OBRIGATÓRIO para veterinários. Número do CRMV com estado (ex: SP-12345)",
        style={
            'placeholder': 'SP-12345, RJ-67890, MG-54321'
        }
    )
    
    especialidade = serializers.CharField(
        max_length=100, 
        required=False, 
        allow_blank=True,
        allow_null=True,
        help_text="🔵 VETERINÁRIO: Especialidade médica (opcional)",
        style={
            'placeholder': 'Clínica Geral, Cirurgia, Dermatologia, Cardiologia'
        }
    )
    
    class Meta:
        model = User
        fields = [
            # Campos principais (obrigatórios)
            'username',
            'password', 
            'confirm_password',
            'email',
            'first_name',
            'last_name',
            # Tipo de usuário
            'role',
            # Campos opcionais de contato
            'telefone',
            'endereco',
            # Campos específicos para veterinários
            'crmv',
            'especialidade'
        ]
    
    def validate_role(self, value):
        """Funcionários podem criar: CLIENTE, FUNCIONARIO, VETERINARIO"""
        allowed_roles = [Profile.Role.CLIENTE, Profile.Role.FUNCIONARIO, Profile.Role.VETERINARIO]
        if value not in allowed_roles:
            raise serializers.ValidationError(
                f"Funcionários só podem criar usuários dos tipos: {', '.join(allowed_roles)}"
            )
        return value

class UserAdminCreateSerializer(UserCreateSerializer):
    """
    🌟 SERIALIZER PARA CRIAÇÃO DE USUÁRIOS POR ADMINISTRADORES
    
    Administradores podem criar usuários de QUALQUER tipo no sistema:
    CLIENTE, FUNCIONARIO, VETERINARIO ou ADMIN
    
    📋 EXEMPLO DE USO:
    {
        "username": "ATEJhFGqAim",
        "password": "minhasenha123",
        "confirm_password": "minhasenha123",
        "email": "user@example.com",
        "first_name": "João",
        "last_name": "Silva",
        "role": "VETERINARIO",
        "telefone": "(11) 99999-9999",
        "endereco": "Rua das Flores, 123, São Paulo",
        "crmv": "SP-12345",
        "especialidade": "Clínica Geral"
    }
    
    🔑 PRIVILÉGIOS: Admins têm acesso total - podem criar inclusive outros admins!
    """
    
    # ===============================
    # 🔴 CAMPOS OBRIGATÓRIOS
    # ===============================
    username = serializers.CharField(
        max_length=150,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Nome de usuário único no sistema para login",
        style={
            'placeholder': 'admin_joao, dr_maria, func_ana, cliente_carlos'
        }
    )
    
    password = serializers.CharField(
        write_only=True, 
        min_length=8,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Senha segura com no mínimo 8 caracteres",
        style={
            'input_type': 'password',
            'placeholder': 'Digite uma senha forte e segura'
        }
    )
    
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Confirme a senha digitada acima para validação",
        style={
            'input_type': 'password',
            'placeholder': 'Repita exatamente a senha acima'
        }
    )
    
    email = serializers.EmailField(
        required=True,
        help_text="🔴 OBRIGATÓRIO: Email válido para contato e recuperação de conta",
        style={
            'placeholder': 'nome@clinica.com.br, admin@empresa.com'
        }
    )
    
    first_name = serializers.CharField(
        max_length=150,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Primeiro nome do usuário",
        style={
            'placeholder': 'João, Maria, Carlos, Ana'
        }
    )
    
    last_name = serializers.CharField(
        max_length=150,
        required=True,
        help_text="🔴 OBRIGATÓRIO: Sobrenome do usuário",
        style={
            'placeholder': 'Silva, Santos, Oliveira, Costa'
        }
    )
    
    # ===============================
    # 🟡 CAMPO TIPO DE USUÁRIO
    # ===============================
    role = serializers.ChoiceField(
        choices=Profile.Role.choices, 
        default=Profile.Role.CLIENTE,
        help_text="🟡 ESCOLHA: Tipo de usuário no sistema. Admins podem criar qualquer tipo, inclusive outros admins.",
        style={
            'base_template': 'select.html'
        }
    )
    
    # ===============================
    # ⚪ CAMPOS OPCIONAIS - CONTATO
    # ===============================
    telefone = serializers.CharField(
        max_length=20, 
        required=False, 
        allow_blank=True,
        allow_null=True,
        help_text="⚪ OPCIONAL: Telefone de contato. Inclua DDD para melhor comunicação.",
        style={
            'placeholder': '(11) 99999-9999, (21) 88888-8888'
        }
    )
    
    endereco = serializers.CharField(
        required=False, 
        allow_blank=True,
        allow_null=True,
        help_text="⚪ OPCIONAL: Endereço residencial ou comercial completo",
        style={
            'base_template': 'textarea.html',
            'placeholder': 'Rua das Flores, 123, Centro\nSão Paulo - SP\nCEP: 01234-567'
        }
    )
    
    # ===============================
    # 🔵 CAMPOS ESPECÍFICOS VETERINÁRIOS
    # ===============================
    crmv = serializers.CharField(
        max_length=20, 
        required=False, 
        allow_blank=True,
        allow_null=True,
        help_text="🔵 VETERINÁRIO: OBRIGATÓRIO apenas para veterinários. Número do CRMV com estado.",
        style={
            'placeholder': 'SP-12345, RJ-67890, MG-54321, RS-11111'
        }
    )
    
    especialidade = serializers.CharField(
        max_length=100, 
        required=False, 
        allow_blank=True,
        allow_null=True,
        help_text="🔵 VETERINÁRIO: Especialidade médica veterinária (opcional)",
        style={
            'placeholder': 'Clínica Geral, Cirurgia, Dermatologia, Cardiologia, Oncologia'
        }
    )
    
    class Meta:
        model = User
        fields = [
            # Campos principais (obrigatórios)
            'username',
            'password', 
            'confirm_password',
            'email',
            'first_name',
            'last_name',
            # Tipo de usuário
            'role',
            # Campos opcionais de contato
            'telefone',
            'endereco',
            # Campos específicos para veterinários
            'crmv',
            'especialidade'
        ]
    
    def validate_role(self, value):
        """Administradores podem criar qualquer tipo de usuário"""
        # Sem restrições para administradores
        return value