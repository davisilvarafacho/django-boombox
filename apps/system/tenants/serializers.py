from rest_framework import serializers


class CriarTenantSerialier(serializers.Serializer):
    nome_banco_dados = serializers.CharField()
    email_usuario = serializers.EmailField()
    senha_usuario = serializers.CharField()
    nome_usuario = serializers.CharField()
    sobrenome_usuario = serializers.CharField()
