from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import generics, status, permissions, viewsets
from rest_framework.decorators import action
from .serializers import UserCreateSerializer, UserAdminSerializer
from django.conf import settings
from .permissions import IsAdminRole # Importa nossa nova permissão
import os

class LogFileView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]

    def get(self, request, *args, **kwargs):
        log_file_path = os.path.join(settings.BASE_DIR, 'logs', 'debug.log')
        try:
            with open(log_file_path, 'r') as log_file:
                # Lê as últimas 100 linhas para não sobrecarregar
                lines = log_file.readlines()[-100:]
                log_content = "".join(lines)
            return Response(log_content, status=status.HTTP_200_OK, content_type='text/plain')
        except FileNotFoundError:
            return Response("Arquivo de log não encontrado.", status=status.HTTP_404_NOT_FOUND)
        
class UserCreateView(generics.CreateAPIView):
    """
    Endpoint público para novos usuários se registrarem.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny] # <-- Permite que qualquer um acesse


class UserAdminViewSet(viewsets.ModelViewSet):
    """
    ViewSet for admin user management operations
    """
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """
        Toggle user active status
        """
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)