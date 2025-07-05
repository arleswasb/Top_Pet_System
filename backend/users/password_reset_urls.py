# users/password_reset_urls.py

from django.urls import path
from .password_reset_views import (
    CustomResetPasswordRequestToken,
    CustomResetPasswordConfirm, 
    CustomResetPasswordValidateToken
)

# URLs customizadas para o reset de senha com tags corretas no Swagger
urlpatterns = [
    path('', CustomResetPasswordRequestToken.as_view(), name="reset-password-request"),
    path('confirm/', CustomResetPasswordConfirm.as_view(), name="reset-password-confirm"),
    path('validate_token/', CustomResetPasswordValidateToken.as_view(), name="reset-password-validate"),
]
