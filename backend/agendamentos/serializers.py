# agendamentos/serializers.py

from rest_framework import serializers
from .models import Agendamento, Servico
from pets.models import Pet
from pets.serializers import PetSerializer

class ServicoSerializer(serializers.ModelSerializer):
    """
    Serializer para criação e listagem de serviços oferecidos pelo pet shop.
    
    📋 **Estrutura do Endpoint:**
    - **Campos obrigatórios**: nome, preco
    - **Campos opcionais**: descricao, duracao, disponivel
    - **Validações especiais**: nome único, preço positivo
    
    💡 **Exemplo de uso:**
    ```json
    {
        "nome": "Banho e Tosa Completa",
        "descricao": "Banho com produtos especializados, tosa higiênica e corte de unhas",
        "duracao": "01:30:00",
        "preco": "45.00",
        "disponivel": true
    }
    ```
    """
    nome = serializers.CharField(
        max_length=100,
        help_text="Nome do serviço oferecido (ex: Banho e Tosa, Consulta Veterinária)"
    )
    descricao = serializers.CharField(
        required=False,
        allow_blank=True,
        style={'base_template': 'textarea.html'},
        help_text="Descrição detalhada do serviço incluindo o que está incluído"
    )
    duracao = serializers.DurationField(
        required=False,
        help_text="Duração estimada do serviço no formato HH:MM:SS (ex: 01:30:00 para 1h30min)",
        style={'placeholder': '01:30:00'}
    )
    preco = serializers.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Valor do serviço em reais (ex: 45.00)",
        style={'placeholder': '45.00'}
    )
    disponivel = serializers.BooleanField(
        default=True,
        help_text="Marque se o serviço está sendo oferecido atualmente"
    )

    class Meta:
        model = Servico
        fields = ['id', 'nome', 'descricao', 'duracao', 'preco', 'disponivel']


class AgendamentoSerializer(serializers.ModelSerializer):
    """
    Serializer para criação e gerenciamento de agendamentos de serviços para pets.
    
    📋 **Estrutura do Endpoint:**
    - **Campos obrigatórios**: pet_id, servico_id, data_hora
    - **Campos opcionais**: observacoes, status
    - **Campos automáticos**: id (gerado automaticamente)
    - **Campos de leitura**: pet (dados completos), servico (dados completos)
    
    ⚠️ **Validações importantes:**
    - Pet deve existir e estar ativo
    - Serviço deve estar disponível
    - Data/hora deve ser futura
    - Não pode haver conflito de horários
    
    💡 **Exemplo de uso para criação:**
    ```json
    {
        "pet_id": 1,
        "servico_id": 2,
        "data_hora": "2024-01-15T14:30:00",
        "observacoes": "Pet tem medo de barulho, favor usar equipamentos silenciosos"
    }
    ```
    
    📊 **Status disponíveis:**
    - AGENDADO: Agendamento confirmado (padrão)
    - CONCLUIDO: Serviço realizado
    - CANCELADO: Agendamento cancelado
    """
    
    # === CAMPOS PARA LEITURA (GET) ===
    pet = PetSerializer(read_only=True)
    servico = ServicoSerializer(read_only=True)

    # === CAMPOS PARA ESCRITA (POST/PATCH) ===
    pet_id = serializers.PrimaryKeyRelatedField(
        queryset=Pet.objects.all(),
        source='pet',
        write_only=True,
        help_text="ID do pet que receberá o serviço",
        style={'placeholder': 'Selecione o pet'}
    )
    servico_id = serializers.PrimaryKeyRelatedField(
        queryset=Servico.objects.filter(disponivel=True),
        source='servico',
        write_only=True,
        help_text="ID do serviço a ser agendado (apenas serviços disponíveis)",
        style={'placeholder': 'Selecione o serviço'}
    )
    
    # === CAMPOS PRINCIPAIS ===
    data_hora = serializers.DateTimeField(
        help_text="Data e hora do agendamento (formato: YYYY-MM-DDTHH:MM:SS)",
        style={'placeholder': '2024-01-15T14:30:00'}
    )
    status = serializers.ChoiceField(
        choices=Agendamento.StatusChoices.choices,
        default=Agendamento.StatusChoices.AGENDADO,
        help_text="Status atual do agendamento"
    )
    
    # === CAMPOS OPCIONAIS ===
    observacoes = serializers.CharField(
        required=False,
        allow_blank=True,
        style={'base_template': 'textarea.html'},
        help_text="Informações adicionais sobre o agendamento, cuidados especiais ou observações importantes"
    )

    class Meta:
        model = Agendamento
        fields = [
            'id',
            'data_hora',
            'status',
            'observacoes',
            'pet',
            'servico',
            'pet_id',
            'servico_id',
        ]


class HorarioDisponivelSerializer(serializers.Serializer):
    """
    Serializer para resposta de horários disponíveis.
    Usado apenas para documentação da API.
    """
    horarios = serializers.ListField(
        child=serializers.CharField(max_length=5),
        help_text="Lista de horários disponíveis no formato HH:MM"
    )

    class Meta:
        swagger_schema_fields = {
            "type": "object",
            "properties": {
                "horarios": {
                    "type": "array",
                    "items": {"type": "string", "format": "time"},
                    "example": ["08:00", "09:00", "10:00", "14:00", "15:00"]
                }
            }
        }