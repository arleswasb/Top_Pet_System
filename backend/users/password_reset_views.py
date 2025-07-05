# users/password_reset_views.py

from django_rest_passwordreset.views import (
    ResetPasswordRequestToken,
    ResetPasswordConfirm,
    ResetPasswordValidateToken
)
from drf_spectacular.utils import extend_schema
from .swagger_schemas import (
    PASSWORD_RESET_REQUEST_SCHEMA,
    PASSWORD_RESET_CONFIRM_SCHEMA,
    PASSWORD_RESET_VALIDATE_SCHEMA
)


# Views customizadas para agrupar na tag "Autenticação"

@extend_schema(
    summary=PASSWORD_RESET_REQUEST_SCHEMA['summary'],
    description=PASSWORD_RESET_REQUEST_SCHEMA['description'],
    tags=PASSWORD_RESET_REQUEST_SCHEMA['tags']
)
class CustomResetPasswordRequestToken(ResetPasswordRequestToken):
    """View customizada para solicitar reset de senha com documentação Swagger."""
    pass


@extend_schema(
    summary=PASSWORD_RESET_CONFIRM_SCHEMA['summary'],
    description=PASSWORD_RESET_CONFIRM_SCHEMA['description'],
    tags=PASSWORD_RESET_CONFIRM_SCHEMA['tags']
)
class CustomResetPasswordConfirm(ResetPasswordConfirm):
    """View customizada para confirmar reset de senha com documentação Swagger."""
    pass


@extend_schema(
    summary=PASSWORD_RESET_VALIDATE_SCHEMA['summary'],
    description=PASSWORD_RESET_VALIDATE_SCHEMA['description'],
    tags=PASSWORD_RESET_VALIDATE_SCHEMA['tags']
)
class CustomResetPasswordValidateToken(ResetPasswordValidateToken):
    """View customizada para validar token de reset com documentação Swagger."""
    pass
