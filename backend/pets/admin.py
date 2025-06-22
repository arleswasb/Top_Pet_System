# pets/admin.py

from django.contrib import admin
from .models import Pet

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    """
    Configuração para a visualização do modelo Pet no painel de administração.
    """
    # Campos que serão exibidos na lista de pets
    list_display = ('id', 'nome', 'tutor', 'especie', 'raca', 'idade')

    # Filtros que aparecerão na barra lateral direita
    list_filter = ('especie', 'raca', 'tutor')

    # Campos pelos quais você poderá buscar
    # Permite buscar pelo nome do pet ou pelo nome de usuário do tutor
    search_fields = ('nome', 'tutor__username')

    # Melhora a seleção do 'tutor' em vez de um dropdown gigante,
    # especialmente se você tiver muitos usuários.
    autocomplete_fields = ('tutor',)

    # Organiza os campos no formulário de edição/criação
    fieldsets = (
        ('Informações do Pet', {
            'fields': ('nome', 'foto', 'especie', 'raca')
        }),
        ('Detalhes Adicionais', {
            'fields': ('idade', 'data_de_nascimento')
        }),
        ('Proprietário', {
            'fields': ('tutor',)
        }),
    )