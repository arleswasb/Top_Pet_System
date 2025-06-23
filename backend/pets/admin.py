# pets/admin.py

from django.contrib import admin
from .models import Pet
from django.utils.translation import gettext_lazy as _ # Importar para traduções (opcional, mas bom)

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    """
    Configuração avançada para a visualização do modelo Pet no painel de administração.
    """
    # Campos que serão exibidos na lista de pets
    list_display = (
        'id',
        'nome',
        'tutor_username', # Método para exibir o username do tutor
        'especie',
        'raca',
        'sexo',           # Adicionado campo sexo
        'get_idade_display', # Método para exibir a idade
        'created_at',     # Adicionado campo created_at
        'updated_at',     # Adicionado campo updated_at
    )

    # Filtros que aparecerão na barra lateral direita
    list_filter = (
        'especie',
        'raca',
        'sexo',           # Adicionado filtro para sexo
        'tutor__username', # Permite filtrar pelo username do tutor
        'created_at',
        'updated_at',
    )

    # Campos pelos quais você poderá buscar
    search_fields = (
        'nome__icontains', # Busca por nome do pet (case-insensitive)
        'raca__icontains', # Busca por raça (case-insensitive)
        'tutor__username__icontains', # Busca por username do tutor (case-insensitive)
        'tutor__email__icontains',    # Busca por email do tutor (case-insensitive)
    )

    # Melhora a seleção do 'tutor' com um campo de autocompletar
    autocomplete_fields = ('tutor',)

    # Ordenação padrão da lista
    ordering = ('nome',)

    # Campos que serão somente leitura (não editáveis) no formulário
    readonly_fields = ('created_at', 'updated_at', 'get_idade_display') # 'idade' também deve ser readonly aqui

    # Organiza os campos no formulário de edição/criação
    fieldsets = (
        (_('Informações Essenciais do Pet'), {
            'fields': ('tutor', 'nome', 'especie', 'raca', 'sexo', 'data_de_nascimento', 'foto')
        }),
        (_('Detalhes Adicionais'), {
            'fields': ('observacoes',), # Adicionado observações
            'description': _('Informações complementares sobre o pet.')
        }),
        (_('Metadados'), {
            'fields': ('created_at', 'updated_at', 'get_idade_display'), # Adicionado metadados e idade (somente exibição)
            'classes': ('collapse',) # Deixa essa seção recolhida por padrão
        }),
    )

    # Métodos personalizados para exibir informações relacionadas ou calculadas
    @admin.display(description=_('Tutor'), ordering='tutor__username')
    def tutor_username(self, obj):
        return obj.tutor.username

    @admin.display(description=_('Idade (Anos)'))
    def get_idade_display(self, obj):
        # A propriedade 'idade' já está definida no modelo Pet e retorna None se a data for nula.
        return obj.idade if obj.idade is not None else _('N/A')