from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.system.base.views import BaseViewSet

from .authentications import TokenIntegracaoAuthenticaton
from .serializers import CriarTenantSerialier
from .services import TenantManager


class TenantsViewSet(BaseViewSet):
    authentication_classes = [TokenIntegracaoAuthenticaton]
    permission_classes = [AllowAny]

    @action(methods=["post"], detail=False)
    def criar_tenant(self, request):
        serializer = CriarTenantSerialier(data=request.data)
        serializer.is_valid(raise_exception=True)
        manager = TenantManager(serializer.data)
        manager.criar_tenant()
        return Response()
