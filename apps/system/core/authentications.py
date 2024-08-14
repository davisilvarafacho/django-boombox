from django.conf import settings

from rest_framework_simplejwt.authentication import JWTAuthentication


class JwtHeaderTenantAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        settings.DATABASES["default"]["NAME"] = validated_token["user_tenant"]

        return self.get_user(validated_token), validated_token


class JwtQueryParamTenantAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = self.get_raw_token(request)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        settings.DATABASES["default"]["NAME"] = validated_token["user_tenant"]

        return self.get_user(validated_token), validated_token

    def get_raw_token(self, request):
        return request.query_params.get(settings.AUTH_QUERY_PARAM_NAME, None)
