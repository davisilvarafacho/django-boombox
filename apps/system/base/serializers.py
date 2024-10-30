from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from apps.users.serializers import OnwerSerializer
from apps.system.tenants.serializers import TenantSerializer


class BaseModelSerializer(ModelSerializer):
    empresa = TenantSerializer(read_only=True)
    owner = OnwerSerializer(read_only=True)

    def get_fields(self):
        fields = super().get_fields()
        action = self.context.get("action", None)

        if action in ("list", "retrieve"):
            for field_name in fields:
                fields[field_name].read_only = True

        elif action in ("create", "update", "partial_update"):
            for field_name in fields:
                field_cls = fields[field_name].__class__
                if issubclass(field_cls, ModelSerializer):
                    model = field_cls.Meta.model
                    method = getattr(self, f"get_{field_name}_queryset", None)
                    if method:
                        fields[field_name] = PrimaryKeyRelatedField(queryset=method(model))
                    else:
                        fields[field_name] = PrimaryKeyRelatedField(queryset=model.objects.all())
            fields["owner"].read_only = True

        return fields
