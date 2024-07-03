from typing import Optional, Tuple

from rest_framework.request import Request

from rest_framework_simplejwt.authentication import JWTAuthentication, Token, AuthUser


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token

    def get_raw_token(self, header: bytes, request: Request) -> bytes | None:
        token = super().get_raw_token(header)
        if token is None:
            token = request.query_params.get("jwt", None)
        return token
    
