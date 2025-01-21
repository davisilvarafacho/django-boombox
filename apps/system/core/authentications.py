import warnings

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.authentication import JWTAuthentication as SimpleJWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings


class JWTAuthentication(SimpleJWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token, request)

        return self.get_user(validated_token, request), validated_token

    def get_user(self, validated_token, request):
        user = super().get_user(validated_token)
        subdominio = self.get_subdominio(request)
        ambiente_usuario = user.ambiente
        if ambiente_usuario.mb_subdominio != subdominio:
            raise AuthenticationFailed(
                {"mensagem": "O usuário não tem permissão para acessar este ambiente"}, code="authentication_failed"
            )
        return user

    def get_validated_token(self, raw_token, request):
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:  # type: ignore
            try:
                return AuthToken(raw_token, request=request)
            except TokenError as e:
                messages.append(
                    {
                        "token_class": AuthToken.__name__,
                        "token_type": AuthToken.token_type,
                        "message": e.args[0],
                    }
                )

        raise InvalidToken(
            {
                "detail": _("Given token not valid for any token type"),
                "messages": messages,
            }
        )

    def get_subdominio(self, request):
        host = request.headers.get(settings.TENANT_HOST_HEADER, "")
        return host.split(".")[0]


class JWTQueryParamAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = self.get_raw_token(request)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token, request=request)

        user = self.get_user(validated_token, request)

        try:
            emails_admins = (tupla[1] for tupla in settings.ADMINS)
            if user.email not in emails_admins:
                return None
        except Exception:
            warnings.warn("Atributo 'ADMINS' foi removido do settings.py", stacklevel=2)

        return user, validated_token

    def get_raw_token(self, request) -> bytes:
        token = request.query_params.get(settings.AUTH_QUERY_PARAM_NAME, None)
        return token
