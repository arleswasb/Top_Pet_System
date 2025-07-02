# backend/configuracao/serializers.py

from rest_framework import serializers
from .models import HorarioFuncionamento, Feriado

class HorarioFuncionamentoSerializer(serializers.ModelSerializer):
    dia_semana_display = serializers.CharField(source='get_dia_semana_display', read_only=True)
    
    class Meta:
        model = HorarioFuncionamento
        fields = ['id', 'dia_semana', 'dia_semana_display', 'hora_abertura', 'hora_fechamento', 'ativo']

class FeriadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feriado
        fields = ['id', 'nome', 'data', 'recorrente', 'ativo']
        
    def validate_data(self, value):
        """Validação customizada para data do feriado"""
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("A data do feriado não pode ser no passado.")
        return value