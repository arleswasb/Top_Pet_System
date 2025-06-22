from django.urls import path
from .views import LogFileView

urlpatterns = [
    path('logs/', LogFileView.as_view(), name='get-logs'),
    path('register/', UserCreateView.as_view(), name='user-register'),
]