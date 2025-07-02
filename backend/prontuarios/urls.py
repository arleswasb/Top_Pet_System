from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Comentar temporariamente até implementar as views
# from .views import ProntuarioViewSet

router = DefaultRouter()
# router.register(r'prontuarios', ProntuarioViewSet, basename='prontuario')

urlpatterns = [
    # Inclui as URLs geradas pelo router
    path('', include(router.urls)),
]