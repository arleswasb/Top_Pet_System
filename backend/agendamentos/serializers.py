from rest_framework import serializers
from .models import Agendamento
from pets.serializers import PetSerializer # Vamos reusar o serializer de Pet

class AgendamentoSerializer(serializers.ModelSerializer):
    # Usamos o PetSerializer para mostrar os detalhes do pet,
    # em vez de apenas o ID. 'read_only=True' significa que não
    # podemos criar um pet por aqui, apenas ler seus dados.
    pet = PetSerializer(read_only=True)

    # Campo extra para receber o ID do pet ao criar um novo agendamento.
    # 'write_only=True' significa que este campo só é usado para escrever
    # dados (no POST), e não aparecerá na resposta JSON.
    pet_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Agendamento
        # Listamos todos os campos que queremos que apareçam na API
        fields = [
            'id',
            'pet',
            'pet_id',
            'data_hora',
            'servico',
            'status',
            'observacoes',
        ]