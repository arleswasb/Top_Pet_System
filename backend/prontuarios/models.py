# prontuarios/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from pets.models import Pet


class Prontuario(models.Model):
    """
    Modelo para armazenar prontuários médicos dos pets
    """
    
    class TipoConsulta(models.TextChoices):
        CONSULTA_ROTINA = 'ROTINA', 'Consulta de Rotina'
        EMERGENCIA = 'EMERGENCIA', 'Emergência'
        RETORNO = 'RETORNO', 'Retorno'
        EXAME = 'EXAME', 'Exame'
        CIRURGIA = 'CIRURGIA', 'Cirurgia'
        VACINA = 'VACINA', 'Vacinação'
    
    pet = models.ForeignKey(
        'pets.Pet',
        on_delete=models.CASCADE,
        related_name='prontuarios',
        verbose_name='Pet'
    )
    
    veterinario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='prontuarios_veterinario',
        verbose_name='Veterinário'
    )
    
    data_consulta = models.DateTimeField(
        default=timezone.now,
        verbose_name='Data da Consulta'
    )
    
    tipo_consulta = models.CharField(
        max_length=20,
        choices=TipoConsulta.choices,
        default=TipoConsulta.CONSULTA_ROTINA,
        verbose_name='Tipo de Consulta'
    )
    
    peso = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Peso (kg)',
        null=True,
        blank=True
    )
    
    temperatura = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal('35.0')),
            MaxValueValidator(Decimal('45.0'))
        ],
        verbose_name='Temperatura (°C)',
        null=True,
        blank=True
    )
    
    motivo_consulta = models.TextField(
        verbose_name='Motivo da Consulta',
        help_text='Descreva o motivo da consulta'
    )
    
    exame_fisico = models.TextField(
        verbose_name='Exame Físico',
        help_text='Descrição do exame físico realizado',
        blank=True
    )
    
    diagnostico = models.TextField(
        verbose_name='Diagnóstico',
        help_text='Diagnóstico médico',
        blank=True
    )
    
    tratamento = models.TextField(
        verbose_name='Tratamento',
        help_text='Descrição do tratamento prescrito',
        blank=True
    )
    
    medicamentos = models.TextField(
        verbose_name='Medicamentos',
        help_text='Lista de medicamentos prescritos',
        blank=True
    )
    
    observacoes = models.TextField(
        verbose_name='Observações',
        help_text='Observações adicionais',
        blank=True
    )
    
    proxima_consulta = models.DateTimeField(
        verbose_name='Próxima Consulta',
        null=True,
        blank=True,
        help_text='Data da próxima consulta (se aplicável)'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )
    
    class Meta:
        verbose_name = 'Prontuário'
        verbose_name_plural = 'Prontuários'
        ordering = ['-data_consulta']
    
    def __str__(self):
        return f"Prontuário {self.id} - {self.pet.nome} - {self.data_consulta.strftime('%d/%m/%Y')}"
