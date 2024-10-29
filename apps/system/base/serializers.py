from rest_framework import serializers

from apps.users.serializers import OnwerSerializer


class BaseModelSerializer(serializers.ModelSerializer):
    owner = OnwerSerializer(read_only=True)
    empresa = serializers.PrimaryKeyRelatedField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        action = self.context["action"]
        if action in ("list", "retrieve"):
            for field_name in self.get_fields():
                self.fields[field_name].read_only = True
