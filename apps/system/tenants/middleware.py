from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from rest_framework.exceptions import AuthenticationFailed

from django_multitenant.utils import set_current_tenant
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Ambiente


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.authenticator = JWTAuthentication()

    def __call__(self, request: WSGIRequest):
        try:
            user, _ = self.authenticator.authenticate(request)  # type: ignore
            request.user = user

            tenant, host = self.get_tenant(request)
            if tenant is None:
                raise AuthenticationFailed({"mensagem": "Esse ambiente não existe"})

            request.tenant = tenant  # type: ignore
            request.host = host  # type: ignore

            set_current_tenant(tenant)
        except Exception:
            return self.get_response(request)

        return self.get_response(request)

    def get_tenant(self, request: WSGIRequest) -> tuple[Ambiente | None, str]:
        host = self.get_host(request)

        if host is None:
            return None, ""

        host = host.split(":")[0]
        tenant = Ambiente.objects.filter(mb_subdominio=host).first()
        return tenant, host

    def get_host(self, request: WSGIRequest) -> str | None:
        if settings.IN_DEVELOPMENT:
            return "domain.com"
        return request.headers.get(settings.TENANT_HOST_HEADER, None)
