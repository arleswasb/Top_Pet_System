from django.urls import path
from .views import PetListCreateView, PetDetailUpdateDeleteView

urlpatterns = [
    path('pets/', PetListCreateView.as_view(), name='pet-list-create'),
    path('pets/<int:pk>/', PetDetailUpdateDeleteView.as_view(), name='pet-detail-update-delete'),
]
