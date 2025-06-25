# agendamentos/serializers.py

from rest_framework import serializers
from .models import Agendamento, Servico
from django.db.models import F, ExpressionWrapper, DateTimeField, Q

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = '__all__'

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = '__all__'

    def validate(self, data):
        """
        Validação para impedir agendamentos sobrepostos para o mesmo pet.
        """
        pet = data.get('pet')
        data_hora_inicio = data.get('data_hora')
        servico = data.get('servico')
        
        if not all([pet, data_hora_inicio, servico]):
            # Se algum dos campos chave não estiver presente, a validação de campo do DRF já vai pegar.
            # Retornamos aqui para evitar erros na lógica abaixo.
            return data

        data_hora_fim = data_hora_inicio + servico.duracao

        # Expressão para calcular o horário de término de agendamentos existentes no banco
        end_time_expression = ExpressionWrapper(F('data_hora') + F('servico__duracao'), output_field=DateTimeField())

        # Busca por agendamentos sobrepostos
        # Um conflito existe se:
        # 1. Um agendamento existente começa durante o novo agendamento.
        # 2. Um agendamento existente termina durante o novo agendamento.
        # 3. Um agendamento existente "envolve" completamente o novo agendamento.
        # A query abaixo cobre todos esses casos.
        conflitos = Agendamento.objects.annotate(
            horario_fim=end_time_expression
        ).filter(
            pet=pet,
            status__in=[Agendamento.StatusChoices.AGENDADO, Agendamento.StatusChoices.CONCLUIDO],
            data_hora__lt=data_hora_fim,      # O agendamento existente começa ANTES do novo terminar
            horario_fim__gt=data_hora_inicio  # E o agendamento existente termina DEPOIS do novo começar
        )

        if self.instance: # Se for uma atualização, exclui o próprio objeto da verificação
            conflitos = conflitos.exclude(pk=self.instance.pk)

        if conflitos.exists():
            raise serializers.ValidationError(f"O pet {pet.nome} já possui um agendamento conflitante neste horário.")

        return data