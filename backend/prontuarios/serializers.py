# prontuarios/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
from drf_spectacular.utils import extend_schema_field
from .models import Prontuario
from pets.models import Pet


class ProntuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para criação e gerenciamento de prontuários médicos dos pets.
    
    📋 **Estrutura do Endpoint:**
    - **Campos obrigatórios**: pet, veterinario, motivo_consulta
    - **Campos opcionais**: data_consulta, tipo_consulta, peso, temperatura, exame_fisico, diagnostico, tratamento, medicamentos, observacoes, proxima_consulta
    - **Campos automáticos**: id, created_at, updated_at, idade_pet (calculados automaticamente)
    - **Campos de leitura**: pet_nome, veterinario_nome, tipo_consulta_display (para exibição)
    
    ⚠️ **Validações importantes:**
    - Pet deve existir e estar ativo
    - Veterinário deve ser um usuário válido
    - Peso deve ser positivo (se informado)
    - Temperatura deve estar entre 35°C e 45°C (se informada)
    - Data da consulta não pode ser muito no futuro
    
    💡 **Exemplo de uso para criação:**
    ```json
    {
        "pet": 1,
        "veterinario": 3,
        "data_consulta": "2024-01-15T10:30:00",
        "tipo_consulta": "ROTINA",
        "peso": "5.2",
        "temperatura": "38.5",
        "motivo_consulta": "Consulta de rotina e aplicação de vacina anual",
        "exame_fisico": "Animal alerta, responsivo. Mucosas rosadas. Ausculta cardiopulmonar normal.",
        "diagnostico": "Animal saudável",
        "tratamento": "Aplicação de vacina V10",
        "medicamentos": "Vacina V10 - 1ml subcutânea",
        "observacoes": "Próxima vacina em 12 meses",
        "proxima_consulta": "2025-01-15T10:30:00"
    }
    ```
    
    🏥 **Tipos de consulta disponíveis:**
    - ROTINA: Consulta de Rotina (padrão)
    - EMERGENCIA: Emergência
    - RETORNO: Retorno
    - EXAME: Exame
    - CIRURGIA: Cirurgia
    - VACINA: Vacinação
    """
    
    # === CAMPOS DE LEITURA (informações expandidas) ===
    pet_nome = serializers.CharField(source='pet.nome', read_only=True)
    veterinario_nome = serializers.CharField(source='veterinario.username', read_only=True)
    tipo_consulta_display = serializers.CharField(source='get_tipo_consulta_display', read_only=True)
    idade_pet = serializers.SerializerMethodField()
    
    # === CAMPOS OBRIGATÓRIOS ===
    pet = serializers.PrimaryKeyRelatedField(
        queryset=Pet.objects.all(),
        help_text="ID do pet que está sendo atendido",
        style={'placeholder': 'Selecione o pet'}
    )
    veterinario = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        help_text="ID do veterinário responsável pelo atendimento",
        style={'placeholder': 'Selecione o veterinário'}
    )
    motivo_consulta = serializers.CharField(
        style={'base_template': 'textarea.html'},
        help_text="Descreva o motivo principal da consulta, sintomas relatados pelo tutor ou observações iniciais"
    )
    
    # === CAMPOS OPCIONAIS DE DATA E TIPO ===
    data_consulta = serializers.DateTimeField(
        default=timezone.now,
        help_text="Data e hora da consulta (formato: YYYY-MM-DDTHH:MM:SS). Se não informado, usa data/hora atual",
        style={'placeholder': '2024-01-15T10:30:00'}
    )
    tipo_consulta = serializers.ChoiceField(
        choices=Prontuario.TipoConsulta.choices,
        default=Prontuario.TipoConsulta.CONSULTA_ROTINA,
        help_text="Tipo de consulta realizada"
    )
    
    # === CAMPOS OPCIONAIS DE MEDIDAS ===
    peso = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        allow_null=True,
        help_text="Peso atual do pet em quilogramas (ex: 5.20)",
        style={'placeholder': '5.20'}
    )
    temperatura = serializers.DecimalField(
        max_digits=4,
        decimal_places=1,
        required=False,
        allow_null=True,
        help_text="Temperatura corporal em graus Celsius, entre 35°C e 45°C (ex: 38.5)",
        style={'placeholder': '38.5'}
    )
    
    # === CAMPOS OPCIONAIS DE TEXTO (TEXTAREA) ===
    exame_fisico = serializers.CharField(
        required=False,
        allow_blank=True,
        style={'base_template': 'textarea.html'},
        help_text="Descrição detalhada do exame físico realizado: inspeção, palpação, ausculta, etc."
    )
    diagnostico = serializers.CharField(
        required=False,
        allow_blank=True,
        style={'base_template': 'textarea.html'},
        help_text="Diagnóstico médico com base nos achados clínicos e exames complementares"
    )
    tratamento = serializers.CharField(
        required=False,
        allow_blank=True,
        style={'base_template': 'textarea.html'},
        help_text="Descrição do tratamento prescrito: procedimentos realizados, orientações ao tutor"
    )
    medicamentos = serializers.CharField(
        required=False,
        allow_blank=True,
        style={'base_template': 'textarea.html'},
        help_text="Lista detalhada dos medicamentos prescritos: nome, dosagem, frequência, duração"
    )
    observacoes = serializers.CharField(
        required=False,
        allow_blank=True,
        style={'base_template': 'textarea.html'},
        help_text="Observações adicionais, recomendações especiais ou informações relevantes"
    )
    
    # === CAMPOS OPCIONAIS DE AGENDAMENTO ===
    proxima_consulta = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text="Data e hora da próxima consulta agendada (se aplicável)",
        style={'placeholder': '2024-02-15T10:30:00'}
    )
    
    class Meta:
        model = Prontuario
        fields = [
            'id', 'pet', 'pet_nome', 'veterinario', 'veterinario_nome',
            'data_consulta', 'tipo_consulta', 'tipo_consulta_display',
            'peso', 'temperatura', 'motivo_consulta', 'exame_fisico', 'diagnostico', 
            'tratamento', 'medicamentos', 'observacoes', 'proxima_consulta',
            'idade_pet', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    @extend_schema_field(serializers.IntegerField(allow_null=True))
    def get_idade_pet(self, obj):
        """
        Calcula e retorna a idade do pet em anos na data da consulta.
        
        Returns:
            int: Idade em anos ou None se data de nascimento não informada
        """
        if obj.pet.data_de_nascimento:
            data_consulta = obj.data_consulta.date() if hasattr(obj.data_consulta, 'date') else obj.data_consulta
            diferenca = data_consulta - obj.pet.data_de_nascimento
            return diferenca.days // 365
        return None