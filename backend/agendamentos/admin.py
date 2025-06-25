# agendamentos/admin.py

from django.contrib import admin
from .models import Servico, Agendamento
from users.models import Profile

# Registra o modelo Servico para que ele apareça no painel de admin
@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'duracao', 'disponivel')
    list_filter = ('disponivel',)
    search_fields = ('nome', 'descricao')

# Também é uma boa ideia registrar o Agendamento para visualizá-lo
@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('pet', 'servico', 'data_hora', 'status', 'get_tutor_email')
    list_filter = ('status', 'servico', 'data_hora')
    search_fields = ('pet__nome', 'servico__nome', 'pet__tutor__email')
    list_select_related = ('pet', 'servico', 'pet__tutor') # Otimização de query
    raw_id_fields = ('pet',) # Melhora a UI quando há muitos pets

    @admin.display(description='Email do Tutor', ordering='pet__tutor__email')
    def get_tutor_email(self, obj):
        return obj.pet.tutor.email

    def get_queryset(self, request):
        """
        Filtra os agendamentos que o usuário pode ver.
        Admins e Funcionários veem tudo. Outros usuários (se houver) não veem nada.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.FUNCIONARIO):
            return qs
        # Por padrão, nega o acesso a outros, a menos que você queira que clientes vejam os seus.
        return qs.none()

    def get_readonly_fields(self, request, obj=None):
        """
        Funcionários não podem alterar o pet, serviço ou data de um agendamento existente.
        """
        if not request.user.is_superuser and obj: # 'obj' existe, então é uma edição
            return ('pet', 'servico', 'data_hora')
        return []

    def has_delete_permission(self, request, obj=None):
        """ Apenas superusuários podem deletar agendamentos. """
        return request.user.is_superuser