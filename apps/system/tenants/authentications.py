from rest_framework.exceptions import AuthenticationFailed

from utils.env import get_env_var


class TokenIntegracaoAuthenticaton:
    def authenticate(self, request):
        token_integracao = request.headers["Authorization"].split(" ")[1]
        if token_integracao != get_env_var("TOKEN_INTEGRACAO"):
            raise AuthenticationFailed({"mensagem": "O token de integração não é válido"}, code="invalid_token")

        return None, token_integracao

    def authenticate_header(self, request):
        return "Bearer"
