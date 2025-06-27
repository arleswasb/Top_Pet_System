# prontuarios/serializers.py

from rest_framework import serializers
from .models import Prontuario, Exame, Vacina
from pets.models import Pet
from django.contrib.auth.models import User


class ExameSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Exame"""
    
    tipo_exame_display = serializers.CharField(source='get_tipo_exame_display', read_only=True)
    
    class Meta:
        model = Exame
        fields = [
            'id', 'tipo_exame', 'tipo_exame_display', 'data_realizacao', 
            'data_resultado', 'resultado', 'valores_referencia', 
            'observacoes', 'arquivo_resultado', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class VacinaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Vacina"""
    
    pet_nome = serializers.CharField(source='pet.nome', read_only=True)
    veterinario_nome = serializers.CharField(source='veterinario.get_full_name', read_only=True)
    
    class Meta:
        model = Vacina
        fields = [
            'id', 'pet', 'pet_nome', 'veterinario', 'veterinario_nome',
            'nome_vacina', 'fabricante', 'lote', 'data_aplicacao', 
            'data_vencimento', 'proxima_dose', 'observacoes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProntuarioSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Prontuario"""
    
    pet_nome = serializers.CharField(source='pet.nome', read_only=True)
    veterinario_nome = serializers.CharField(source='veterinario.get_full_name', read_only=True)
    tipo_consulta_display = serializers.CharField(source='get_tipo_consulta_display', read_only=True)
    exames = ExameSerializer(many=True, read_only=True)
    
    class Meta:
        model = Prontuario
        fields = [
            'id', 'pet', 'pet_nome', 'veterinario', 'veterinario_nome',
            'data_consulta', 'tipo_consulta', 'tipo_consulta_display',
            'peso', 'temperatura', 'sintomas', 'diagnostico', 
            'tratamento', 'medicamentos', 'observacoes', 
            'retorno_recomendado', 'exames', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'data_consulta', 'created_at', 'updated_at']

    def validate_pet(self, value):
        """Valida se o pet existe e se o usuário tem permissão para acessá-lo"""
        user = self.context['request'].user
        
        # Administradores e veterinários podem acessar qualquer pet
        if user.profile.role in ['ADMIN', 'FUNCIONARIO']:
            return value
            
        # Clientes só podem acessar seus próprios pets
        if user.profile.role == 'CLIENTE' and value.tutor != user:
            raise serializers.ValidationError("Você não tem permissão para acessar este pet.")
            
        return value

    def validate_veterinario(self, value):
        """Valida se o veterinário tem permissão para criar prontuários"""
        if value.profile.role not in ['ADMIN', 'FUNCIONARIO']:
            raise serializers.ValidationError("Apenas veterinários podem ser responsáveis por prontuários.")
        return value


class ProntuarioCreateSerializer(serializers.ModelSerializer):
    """Serializer simplificado para criação de prontuários"""
    
    class Meta:
        model = Prontuario
        fields = [
            'pet', 'veterinario', 'tipo_consulta', 'peso', 'temperatura',
            'sintomas', 'diagnostico', 'tratamento', 'medicamentos',
            'observacoes', 'retorno_recomendado'
        ]

    def validate_pet(self, value):
        """Valida se o pet existe e se o usuário tem permissão para acessá-lo"""
        user = self.context['request'].user
        
        # Administradores e veterinários podem acessar qualquer pet
        if user.profile.role in ['ADMIN', 'FUNCIONARIO']:
            return value
            
        # Clientes só podem acessar seus próprios pets
        if user.profile.role == 'CLIENTE' and value.tutor != user:
            raise serializers.ValidationError("Você não tem permissão para acessar este pet.")
            
        return value


class VacinaCreateSerializer(serializers.ModelSerializer):
    """Serializer simplificado para criação de vacinas"""
    
    class Meta:
        model = Vacina
        fields = [
            'pet', 'veterinario', 'nome_vacina', 'fabricante', 'lote',
            'data_aplicacao', 'data_vencimento', 'proxima_dose', 'observacoes'
        ]

    def validate_pet(self, value):
        """Valida se o pet existe e se o usuário tem permissão para acessá-lo"""
        user = self.context['request'].user
        
        # Administradores e veterinários podem acessar qualquer pet
        if user.profile.role in ['ADMIN', 'FUNCIONARIO']:
            return value
            
        # Clientes só podem acessar seus próprios pets
        if user.profile.role == 'CLIENTE' and value.tutor != user:
            raise serializers.ValidationError("Você não tem permissão para acessar este pet.")
            
        return value
