# backend/configuracao/models.py

from django.db import models

class HorarioFuncionamento(models.Model):
    DIAS_SEMANA = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    dia_semana = models.IntegerField(choices=DIAS_SEMANA, unique=True)
    hora_abertura = models.TimeField()
    hora_fechamento = models.TimeField()
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Horário de Funcionamento"
        verbose_name_plural = "Horários de Funcionamento"
        ordering = ['dia_semana']
    
    def __str__(self):
        return f"{self.get_dia_semana_display()}: {self.hora_abertura} - {self.hora_fechamento}"

class Feriado(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField(unique=True)
    recorrente = models.BooleanField(default=False, help_text="Se marcado, o feriado se repete anualmente")
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Feriado"
        verbose_name_plural = "Feriados"
        ordering = ['data']
    
    def __str__(self):
        return f"{self.nome} - {self.data}"