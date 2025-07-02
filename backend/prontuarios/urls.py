from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProntuarioViewSet

router = DefaultRouter()
router.register(r'', ProntuarioViewSet, basename='prontuario')

urlpatterns = [
    # Inclui as URLs geradas pelo router
    path('', include(router.urls)),
]