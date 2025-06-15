from django.contrib import admin
from .models import Profile  # Importa o nosso modelo Profile

# Registra o modelo Profile na interface de administração
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role') # Campos que aparecerão na lista
    list_filter = ('role',) # Adiciona um filtro por papel