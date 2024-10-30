from apps.system.base.serializers import BaseModelSerializer

from .models import Tenant


class TenantSerializer(BaseModelSerializer):
    class Meta:
        model = Tenant
        fields = "__all__"
