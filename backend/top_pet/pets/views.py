from rest_framework import generics, permissions
from .models import Pet
from .serializers import PetSerializer
from django.contrib.auth.models import User # Não será usado diretamente aqui, mas é bom ter em mente

# View para Listar e Criar Pets
# Permite que apenas usuários autenticados vejam/criem seus próprios pets
class PetListCreateView(generics.ListCreateAPIView):
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated] # Apenas usuários autenticados podem acessar

    def get_queryset(self):
        # Retorna apenas os pets do usuário autenticado
        return Pet.objects.filter(tutor=self.request.user)

    def perform_create(self, serializer):
        # Vincula o pet ao usuário autenticado automaticamente na criação
        serializer.save(tutor=self.request.user)

# View para Obter Detalhes, Editar e Deletar Pets
# Permite que apenas o tutor do pet acesse/modifique/delete
class PetDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated] # Apenas usuários autenticados podem acessar
    queryset = Pet.objects.all() # Inicialmente, o queryset abrange todos os pets

    def get_queryset(self):
        # Garante que um usuário só pode acessar/modificar/deletar SEUS PRÓPRIOS pets
        # Isso é uma camada extra de segurança, mesmo que a permissão já restrinja
        return Pet.objects.filter(tutor=self.request.user)
