# prontuarios/serializers.py

from rest_framework import serializers
from django.utils import timezone
from datetime import date
from .models import Prontuario


class ProntuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Prontuario
    """
    pet_nome = serializers.CharField(source='pet.nome', read_only=True)
    veterinario_nome = serializers.CharField(source='veterinario.username', read_only=True)
    tipo_consulta_display = serializers.CharField(source='get_tipo_consulta_display', read_only=True)
    idade_pet = serializers.SerializerMethodField()
    
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
    
    def get_idade_pet(self, obj):
        """Retorna a idade do pet na data da consulta"""
        if obj.pet.data_de_nascimento:
            data_consulta = obj.data_consulta.date() if hasattr(obj.data_consulta, 'date') else obj.data_consulta
            diferenca = data_consulta - obj.pet.data_de_nascimento
            return diferenca.days // 365
        return None