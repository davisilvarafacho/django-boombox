from rest_framework.viewsets import ModelViewSet


class BaseMultiTenantViewSet(ModelViewSet):
    """
    Classe base para todas as viewsets multi-tenant
    """

    def get_queryset(self):
        return super().get_queryset().filter(criador=self.request.user)
