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
    """
    Serializer para criação e atualização de pets.
    
    Exemplo de uso:
    {
        "nome": "Rex",
        "especie": "Cão", 
        "raca": "Golden Retriever",
        "data_de_nascimento": "2020-05-15",
        "sexo": "MACHO",
        "observacoes": "Pet muito dócil e brincalhão"
    }
    """
    # Campos somente leitura
    tutor_detail = UserSerializer(source='tutor', read_only=True)
    tutor = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True),
        write_only=True,
        required=False,  # Deixe como False, a view irá validar conforme o perfil
        help_text="ID do usuário que será o tutor do pet (obrigatório para funcionários)"
    )
    idade = serializers.SerializerMethodField(help_text="Idade formatada do pet (ex: '2 anos e 3 meses')")
    
    # Campos do modelo com documentação
    nome = serializers.CharField(
        max_length=100,
        help_text="Nome do pet"
    )
    especie = serializers.CharField(
        max_length=50,
        help_text="Espécie do pet (ex: Cão, Gato, Pássaro)"
    )
    raca = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
        help_text="Raça do pet (opcional)"
    )
    data_de_nascimento = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="Data de nascimento do pet (formato: YYYY-MM-DD)"
    )
    sexo = serializers.ChoiceField(
        choices=Pet.Gender.choices,
        default=Pet.Gender.UNKNOWN,
        help_text="Sexo do pet"
    )
    foto = serializers.ImageField(
        required=False,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        help_text="Upload de foto do pet (JPG, JPEG ou PNG)"
    )
    observacoes = serializers.CharField(
        required=False,
        allow_blank=True,
        style={'base_template': 'textarea.html'},
        help_text="Observações adicionais sobre o pet"
    )

    class Meta:
        model = Pet
        fields = [
            # Campos principais (obrigatórios)
            'nome',
            'especie', 
            # Campos opcionais de identificação
            'raca',
            'data_de_nascimento',
            'sexo',
            'foto',
            'observacoes',
            # Campo de relacionamento
            'tutor_detail',
            'tutor',
            # Campos somente leitura
            'id',
            'idade',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'idade', 'tutor_detail', 'created_at', 'updated_at']

    @extend_schema_field(serializers.CharField(default="Idade não informada"))
    def get_idade(self, obj):
        """
        Retorna a idade formatada do pet.
        Ex: "1 ano e 5 meses", "3 meses e 10 dias", "15 dias".
        """
        detalhes = obj.idade_detalhada
        if detalhes is None:
            return "Idade não informada"

        anos = detalhes["anos"]
        meses = detalhes["meses"]
        dias = detalhes["dias"]

        parts = []
        if anos > 0:
            parts.append(f"{anos} ano{'s' if anos > 1 else ''}")
        if meses > 0:
            parts.append(f"{meses} {'mês' if meses == 1 else 'meses'}")
        # Só mostrar dias se o pet tiver menos de 1 ano
        if anos == 0 and dias > 0:
            parts.append(f"{dias} dia{'s' if dias > 1 else ''}")
        
        # Se for um recém-nascido (menos de 1 dia de idade)
        if not parts:
            return "Recém-nascido"
            
        return " e ".join(parts)

    def validate_tutor(self, value):
        """Validação customizada: apenas clientes ou veterinários podem ser tutores"""
        if not hasattr(value, 'profile'):
            raise serializers.ValidationError("O usuário selecionado não possui um perfil associado.")
        # Permitir CLIENTE ou VETERINARIO como tutor
        if value.profile.role not in [Profile.Role.CLIENTE, Profile.Role.VETERINARIO]:
            raise serializers.ValidationError("O tutor deve ser um cliente ou veterinário.")
        return value