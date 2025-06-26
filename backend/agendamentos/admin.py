# agendamentos/admin.py

from django.contrib import admin
from .models import Servico, Agendamento

# Registra o modelo Servico para que ele apareça no painel de admin
@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'duracao', 'disponivel')
    list_filter = ('disponivel',)
    search_fields = ('nome',)

# Também é uma boa ideia registrar o Agendamento para visualizá-lo
@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('pet', 'servico', 'data_hora', 'status')
    list_filter = ('status', 'servico')
    search_fields = ('pet__nome',)