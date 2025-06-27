from django.contrib import admin
from .models import Prontuario


@admin.register(Prontuario)
class ProntuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'pet', 'data_consulta', 'veterinario', 'tipo_consulta', 'created_at']
    list_filter = ['data_consulta', 'veterinario', 'tipo_consulta', 'created_at']
    search_fields = ['pet__nome', 'veterinario__username', 'motivo_consulta', 'diagnostico']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('pet', 'veterinario', 'data_consulta', 'tipo_consulta')
        }),
        ('Exame', {
            'fields': ('peso', 'temperatura', 'motivo_consulta', 'exame_fisico')
        }),
        ('Diagnóstico e Tratamento', {
            'fields': ('diagnostico', 'tratamento', 'medicamentos', 'observacoes')
        }),
        ('Acompanhamento', {
            'fields': ('proxima_consulta',)
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    date_hierarchy = 'data_consulta'
