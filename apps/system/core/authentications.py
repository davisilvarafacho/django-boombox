from typing import Optional, Tuple

from rest_framework.request import Request

from rest_framework_simplejwt.authentication import JWTAuthentication, Token, AuthUser


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        token = request.query_params.get("jwt", None)
        if token:
            validated_token = self.get_validated_token(token)

            return self.get_user(validated_token), validated_token

        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token
