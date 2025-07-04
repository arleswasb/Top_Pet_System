# top_pet/api_urls.py
"""
URLs para views utilitárias da API principal.
"""

from django.urls import path
from .views import api_status, api_info, api_root

urlpatterns = [
    path('', api_root, name='api-root'),
    path('status/', api_status, name='api-status'),
    path('info/', api_info, name='api-info'),
]
