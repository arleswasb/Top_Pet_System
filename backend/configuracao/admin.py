from django.contrib import admin
from .models import HorarioFuncionamento, Feriado

@admin.register(HorarioFuncionamento)
class HorarioFuncionamentoAdmin(admin.ModelAdmin):
    list_display = ['get_dia_semana_display', 'hora_abertura', 'hora_fechamento', 'ativo']
    list_filter = ['ativo', 'dia_semana']
    ordering = ['dia_semana']
    list_editable = ['ativo']
    
    def get_dia_semana_display(self, obj):
        return obj.get_dia_semana_display()
    get_dia_semana_display.short_description = 'Dia da Semana'

@admin.register(Feriado)
class FeriadoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data', 'recorrente', 'ativo']
    list_filter = ['recorrente', 'ativo', 'data']
    search_fields = ['nome']
    ordering = ['data']
    list_editable = ['ativo', 'recorrente']
    date_hierarchy = 'data'
