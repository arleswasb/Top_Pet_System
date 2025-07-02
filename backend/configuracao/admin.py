from django.contrib import admin
from .models import HorarioFuncionamento, Feriado

@admin.register(HorarioFuncionamento)
class HorarioFuncionamentoAdmin(admin.ModelAdmin):
    list_display = ['dia_semana', 'get_dia_semana_display', 'hora_abertura', 'hora_fechamento', 'ativo']
    list_filter = ['ativo', 'dia_semana']
    ordering = ['dia_semana']

@admin.register(Feriado)
class FeriadoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data', 'recorrente', 'ativo']
    list_filter = ['recorrente', 'ativo']
    search_fields = ['nome']
    ordering = ['data']
