# users/urls.py

from django.urls import path
# Importe TODAS as views que você usa neste arquivo
from .views import LogFileView, UserCreateView

urlpatterns = [
    path('logs/', LogFileView.as_view(), name='get-logs'),
    path('register/', UserCreateView.as_view(), name='user-register'),
    
]