# agendamentos/serializers.py

from rest_framework import serializers

from pets.models import Pet
from pets.serializers import PetSerializer

from .models import Agendamento, Servico


class ServicoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Servico.
    """

    class Meta:
        model = Servico
        fields = ["id", "nome", "descricao", "duracao", "preco"]


class AgendamentoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Agendamento.
    """

    # Nested serializers para leitura (GET)
    pet = PetSerializer(read_only=True)
    servico = ServicoSerializer(read_only=True)

    # PrimaryKeyRelatedFields para escrita (POST/PUT)
    pet_id = serializers.PrimaryKeyRelatedField(
        queryset=Pet.objects.all(), source="pet", write_only=True
    )
    servico_id = serializers.PrimaryKeyRelatedField(
        queryset=Servico.objects.filter(disponivel=True),
        source="servico",
        write_only=True,
    )

    class Meta:
        model = Agendamento
        fields = [
            "id",
            "data_hora",
            "status",
            "observacoes",
            "pet",
            "servico",
            "pet_id",
            "servico_id",
        ]