from django.urls import path
from .views import LogFileView

urlpatterns = [
    path('logs/', LogFileView.as_view(), name='get-logs'),
]