from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, empty


class BaseModelSerializer(ModelSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        exclude_fields = kwargs.pop("exclude_fields", None)

        action = kwargs.get("context", {}).get("action", None)
        if action in ("list", "retrieve"):
            self.Meta.read_only_fields = self._declared_fields

        super().__init__(instance, data, **kwargs)

        if exclude_fields is not None:
            for field_name in exclude_fields:
                self.fields.pop(field_name, None)

        action = self.context.get("action", None)

        if action in ("create", "update", "partial_update"):
            for field_name in self.fields:
                field_cls = self.fields[field_name].__class__

                if issubclass(field_cls, ModelSerializer):
                    model = field_cls.Meta.model
                    method = getattr(self, f"get_{field_name}_queryset", None)

                    if method:
                        self.fields[field_name] = PrimaryKeyRelatedField(queryset=method(model), required=False)
                    else:
                        self.fields[field_name] = PrimaryKeyRelatedField(queryset=model.objects.all(), required=False)
