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
    
    @classmethod
    def get_horario_dia(cls, dia_semana):
        """Retorna o horário de funcionamento para um dia específico"""
        try:
            return cls.objects.get(dia_semana=dia_semana, ativo=True)
        except cls.DoesNotExist:
            return None
    
    def is_horario_valido(self, hora):
        """Verifica se uma hora está dentro do horário de funcionamento"""
        return self.hora_abertura <= hora <= self.hora_fechamento

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
    
    @classmethod
    def is_feriado(cls, data):
        """Verifica se uma data é feriado"""
        return cls.objects.filter(data=data, ativo=True).exists()
    
    @classmethod
    def get_feriados_mes(cls, ano, mes):
        """Retorna todos os feriados de um mês específico"""
        return cls.objects.filter(
            data__year=ano,
            data__month=mes,
            ativo=True
        ).order_by('data')