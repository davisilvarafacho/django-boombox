
from rest_framework import serializers
from rest_framework.fields import empty

from apps.users.serializers import OnwerSerializer


class BaseModelSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(instance, data, **kwargs)

        if self.context.get("action", None) in ("list", "retrieve"):
            self.fields["owner"] = OnwerSerializer()

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
