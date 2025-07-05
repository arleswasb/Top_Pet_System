#!/usr/bin/env python
"""
Teste simples para verificar sintaxe da view
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
django.setup()

try:
    from agendamentos.views import horarios_disponiveis
    print("✅ View importada com sucesso!")
    
    # Testar importações
    from datetime import date, datetime, time, timedelta
    print("✅ Imports datetime OK")
    
    from rest_framework.decorators import api_view, permission_classes
    print("✅ Imports DRF decorators OK")
    
    from rest_framework import viewsets, permissions, serializers, status
    print("✅ Imports DRF OK")
    
    from rest_framework.response import Response
    print("✅ Imports Response OK")
    
    from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
    print("✅ Imports drf-spectacular utils OK")
    
    from drf_spectacular.types import OpenApiTypes
    print("✅ Imports drf-spectacular types OK")
    
    print("\n🎉 Todas as importações estão funcionando!")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro: {e}")
    sys.exit(1)
