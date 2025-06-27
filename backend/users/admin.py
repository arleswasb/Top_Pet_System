from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile
from django.utils.translation import gettext_lazy as _

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Advanced configuration for Profile model in admin interface"""
    
    list_display = (
        'user_email', 
        'user_username', 
        'formatted_role', 
        'get_user_is_active', # Modificado: usará um método para acessar user.is_active
        'date_joined'
    )
    list_filter = (
        'role', 
        'user__is_active',
        'user__date_joined'
    )
    search_fields = (
        'user__username__exact', 
        'user__email__exact',
        'user__first_name',
        'user__last_name'
    )
    list_select_related = ('user',)
    raw_id_fields = ('user',)
    list_per_page = 25
    # list_editable = ('is_active',) # REMOVIDO: 'is_active' não é um campo direto do Profile
    # Você não pode ter list_editable para campos que não são diretamente do modelo registrado.
    # A edição de 'is_active' será feita através do CustomUserAdmin.
    date_hierarchy = 'user__date_joined'
    
    fieldsets = (
        (None, {
            # 'fields': ('user', 'is_active') # REMOVIDO 'is_active' aqui
            'fields': ('user',) # Apenas 'user', já que 'is_active' pertence ao User
        }),
        (_('Role Settings'), {
            'fields': ('role',),
            'description': _('Define user access level')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at') # Estes são campos do Profile e estão corretos
    
    @admin.display(description=_('Email'), ordering='user__email')
    def user_email(self, obj):
        return obj.user.email
    
    @admin.display(description=_('Username'))
    def user_username(self, obj):
        return obj.user.username
    
    @admin.display(description=_('Role'), ordering='role')
    def formatted_role(self, obj):
        return obj.get_role_display()
    
    @admin.display(description=_('Active?'), boolean=True, ordering='user__is_active') # Adicionado ordering
    def get_user_is_active(self, obj): # Renomeado para evitar conflito e ser mais claro
        return obj.user.is_active
    
    @admin.display(description=_('Date Joined'), ordering='user__date_joined') # Adicionado ordering
    def date_joined(self, obj):
        return obj.user.date_joined

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = _('Profile')
    verbose_name_plural = _('Profile Settings')
    fields = (
        'role', 
        # 'is_active', # REMOVIDO: 'is_active' não é um campo direto do Profile
        ('created_at', 'updated_at')
    )
    # AQUI ESTAVA O SEU ERRO: readonly_fields só podem referenciar campos DIRETOS do modelo Profile ou métodos do ProfileInline.
    # Como 'is_active' não é um campo do Profile, ele não pode estar aqui.
    readonly_fields = ('created_at', 'updated_at') # Estes são campos do Profile e estão corretos
    classes = ('collapse',)

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'is_staff', 
        'is_active', # is_active JÁ É um campo do User e pode ser exibido e editado aqui
        'profile_role',
        'date_joined'
    )
    list_filter = (
        'is_staff', 
        'is_superuser', 
        'is_active', 
        'profile__role'
    )
    list_select_related = ('profile',)
    
    @admin.display(description=_('Role'))
    def profile_role(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.get_role_display()
        return _('Not set')
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

# Unregister and re-register User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Optional: Custom admin site header
admin.site.site_header = _('Pet System Administration')
admin.site.site_title = _('Pet System Admin')
admin.site.index_title = _('Welcome to Pet System Admin')