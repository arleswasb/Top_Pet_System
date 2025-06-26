"""User views."""

import os

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdminRole
from .serializers import UserCreateSerializer


class LogFileView(APIView):
    """View to see log files."""

    permission_classes = [permissions.IsAuthenticated, IsAdminRole]

    def get(self, request, *args, **kwargs):
        """Return log file content."""
        log_file_path = os.path.join(settings.BASE_DIR, "logs", "debug.log")
        try:
            with open(log_file_path, "r") as log_file:
                # Lê as últimas 100 linhas para não sobrecarregar
                lines = log_file.readlines()[-100:]
                log_content = "".join(lines)
            return Response(
                log_content,
                status=status.HTTP_200_OK,
                content_type="text/plain",
            )
        except FileNotFoundError:
            return Response(
                "Arquivo de log não encontrado.",
                status=status.HTTP_404_NOT_FOUND,
            )


class UserCreateView(generics.CreateAPIView):
    """Endpoint for new users to register."""

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [
        permissions.AllowAny
    ]  # <-- Allows anyone to access