# users/urls.py

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
# Importe TODAS as views que você usa neste arquivo
from .views import LogFileView, UserCreateView

urlpatterns = [
    path('login/', obtain_auth_token, name='api-token-auth'),
    path('logs/', LogFileView.as_view(), name='get-logs'),
    path('register/', UserCreateView.as_view(), name='user-register'),
    
]