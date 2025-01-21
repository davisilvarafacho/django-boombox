from rest_framework import serializers

from rest_flex_fields import FlexFieldsModelSerializer


class BaseModelSerializer(FlexFieldsModelSerializer):
    pass

    # def get_field_verbose_name(self, field_name):
    #     # Retorna o verbose_name do campo ou o próprio nome do campo se não existir
    #     return self.Meta.model._meta.get_field(field_name).verbose_name

    # def run_validation(self, data=serializers.empty):
    #     try:
    #         return super().run_validation(data)
    #     except serializers.ValidationError as e:
    #         errors = e.detail
    #         new_errors = {}
    #         for field_name, field_errors in errors.items():
    #             # Usa o verbose_name no erro
    #             verbose_name = self.get_field_verbose_name(field_name)
    #             new_errors[verbose_name] = field_errors
    #         raise serializers.ValidationError(new_errors)
