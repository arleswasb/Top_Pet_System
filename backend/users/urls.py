from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LogFileView, UserCreateView, UserAdminViewSet, 
    UserFuncionarioCreateView, UserAdminCreateView, UserProfileView
)

# Create a router for viewsets
router = DefaultRouter()
router.register(r'admin/users', UserAdminViewSet, basename='user-admin')

urlpatterns = [
    path('logs/', LogFileView.as_view(), name='get-logs'),
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('funcionario/create-user/', UserFuncionarioCreateView.as_view(), name='funcionario-create-user'),
    path('admin/create-user/', UserAdminCreateView.as_view(), name='admin-create-user'),
    path('', include(router.urls)),
]