from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from rest_framework_simplejwt.exceptions import AuthenticationFailed

from django_multitenant.utils import set_current_tenant

from .models import Tenant


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        if not hasattr(self, "authenticator"):
            from rest_framework_simplejwt.authentication import JWTAuthentication

            self.authenticator = JWTAuthentication()

            try:
                user, _ = self.authenticator.authenticate(request)  # type: ignore
                request.user = user
            except Exception:
                return self.get_response(request)

        try:
            tenant, host = self.get_tenant(request)
            if tenant is None:
                raise AuthenticationFailed({"mensagem": "Tenant não encontrada"})

            request.tenant = tenant  # type: ignore
            request.host = host  # type: ignore

            set_current_tenant(tenant)
        except Exception:
            return self.get_response(request)

        return self.get_response(request)

    def get_tenant(self, request: WSGIRequest) -> tuple[Tenant | None, str]:
        host = self.get_host(request).split(".")[0]
        tenant = Tenant.objects.filter(tn_subdominio=host).first()
        return tenant, host

    def get_host(self, request: WSGIRequest) -> str:
        if settings.IN_DEVELOPMENT:
            return "zettabyte.wcommanda.com.br"
        return request.get_host()
