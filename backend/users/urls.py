from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LogFileView, UserCreateView, UserAdminViewSet, UserFuncionarioViewSet, UserProfileView,
    CustomResetPasswordRequestToken, CustomResetPasswordConfirm, CustomResetPasswordValidateToken
)

# Create a router for viewsets
router = DefaultRouter()
router.register(r'admin/users', UserAdminViewSet, basename='user-admin')
router.register(r'funcionario/users', UserFuncionarioViewSet, basename='user-funcionario')

urlpatterns = [
    path('logs/', LogFileView.as_view(), name='get-logs'),
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    
    # Password Reset URLs com tag Autenticação
    path('auth/password-reset/', CustomResetPasswordRequestToken.as_view(), name='password_reset_request'),
    path('auth/password-reset/confirm/', CustomResetPasswordConfirm.as_view(), name='password_reset_confirm'),
    path('auth/password-reset/validate_token/', CustomResetPasswordValidateToken.as_view(), name='password_reset_validate'),
    
    path('', include(router.urls)),
]