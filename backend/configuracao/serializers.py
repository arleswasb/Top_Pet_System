# backend/configuracao/serializers.py

from rest_framework import serializers
from .models import HorarioFuncionamento, Feriado

class HorarioFuncionamentoSerializer(serializers.ModelSerializer):
    dia_semana_display = serializers.CharField(source='get_dia_semana_display', read_only=True)
    
    class Meta:
        model = HorarioFuncionamento
        fields = ['id', 'dia_semana', 'dia_semana_display', 'hora_abertura', 'hora_fechamento', 'ativo']
    
    def validate(self, attrs):
        """Validação para garantir que hora_fechamento > hora_abertura"""
        hora_abertura = attrs.get('hora_abertura')
        hora_fechamento = attrs.get('hora_fechamento')
        
        if hora_abertura and hora_fechamento and hora_fechamento <= hora_abertura:
            raise serializers.ValidationError({
                'hora_fechamento': 'Hora de fechamento deve ser posterior à hora de abertura.'
            })
        return attrs

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
    
    def validate_nome(self, value):
        """Validação para nome do feriado"""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Nome do feriado deve ter pelo menos 3 caracteres.")
        return value.strip()