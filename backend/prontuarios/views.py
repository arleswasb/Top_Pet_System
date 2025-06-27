from rest_framework.decorators import action
from rest_framework import viewsets
from .models import Prontuario
from .serializers import ProntuarioSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdminOrVet
from rest_framework.response import Response


class ProntuarioViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Prontuario instances.
    """
    serializer_class = ProntuarioSerializer
    queryset = Prontuario.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrAdminOrVet]

    @action(detail=False, methods=["get"], url_path=r"por-pet/(?P<pet_id>\d+)")
    def por_pet(self, request, pet_id=None):
        """
        Retorna todos os prontuários de um pet específico.
        """
        prontuarios = self.get_queryset().filter(pet_id=pet_id)
        serializer = self.get_serializer(prontuarios, many=True)
        return Response(serializer.data)