from rest_framework.exceptions import AuthenticationFailed

TOKEN_INTEGRACAO = "67104cf3-6c90-42e7-a253-489d645babf6"   


class TokenIntegracaoAuthenticaton:
    def authenticate(self, request):
        token_integracao = request.headers["Authorization"].split(" ")[1]
        if token_integracao != TOKEN_INTEGRACAO:
            raise AuthenticationFailed({"mensagem": "O token de integração não é válido"}, code="invalid_token")

        return None, token_integracao

    def authenticate_header(self, request):
        return "Bearer"
