from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogFileView, UserCreateView, UserAdminViewSet

# Create a router for viewsets
router = DefaultRouter()
router.register(r'admin/users', UserAdminViewSet, basename='user-admin')

urlpatterns = [
    path('logs/', LogFileView.as_view(), name='get-logs'),
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('', include(router.urls)),
]