import uuid

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string

from rest_framework import serializers
from rest_framework import exceptions

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    PasswordField,
)

from apps.system.core.classes import Email

from .models import Usuario


REDEFINIR_SENHA_CACHE_KEY = "reset-password-%s"

CONFIRMAR_EMAIL_CACHE_KEY = "email-confirm-%s"


def enviar_email_confirmacao_email(email):
    codigo_confirmacao = str(uuid.uuid4())[:8].upper()
    cache.set(CONFIRMAR_EMAIL_CACHE_KEY % email, codigo_confirmacao)

    email = Email(
        titulo="Confirmação de Email",
        corpo="Esse é o código de confirmação: %s" % codigo_confirmacao,
        destinatarios=[email],
    )

    email.send()


class UsuarioSerializer(serializers.ModelSerializer):
    password = PasswordField()

    def validate_password(self, password):
        validate_password(password)
        return make_password(password)

    def create(self, validated_data):
        instance = super().create(validated_data)
        enviar_email_confirmacao_email(instance.email)
        return instance

    class Meta:
        model = Usuario
        exclude = (
            "is_superuser",
            "groups",
            "user_permissions",
            "is_staff",
        )


class OnwerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
        )


class ReenviaEmailConfirmacaoSerializer(serializers.Serializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

    def validate_usuario(self, value):
        if value.email_verified:
            raise serializers.ValidationError(
                {"usuario": "Esse usuário já possui o email confirmado"}
            )
        return value

    def save(self):
        enviar_email_confirmacao_email(self.validated_data["usuario"].email)


class ConfirmarEmailSerializer(serializers.Serializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    codigo = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        usuario = validated_data["usuario"]

        if usuario.email_verified:
            raise serializers.ValidationError(
                {"mensagem": _("O usuário já confirmou o email")},
                code="invalid_request",
            )

        codigo = validated_data["codigo"]

        cache_key = CONFIRMAR_EMAIL_CACHE_KEY % usuario.email
        codigo_cache = cache.get(cache_key, None)
        if codigo_cache is None:
            raise serializers.ValidationError(
                {"mensagem": _("O código de confirmação expirou")}, code="expired_code"
            )

        if codigo != codigo_cache:
            raise serializers.ValidationError(
                {"mensagem": _("O código informado não é inválido")}
            )

        cache.delete(cache_key)

        return validated_data

    def save(self):
        validated_data = self.validated_data
        usuario = validated_data["usuario"]
        usuario.email_confirmed = True
        usuario.save()


class EnviarEmailRedefinicaoSenhaSerializer(serializers.Serializer):
    usuario = serializers.SlugRelatedField(
        queryset=Usuario.objects.all(),
        slug_field="email",
    )

    def save(self):
        usuario = self.validated_data["usuario"]

        cache_key = REDEFINIR_SENHA_CACHE_KEY % usuario.email

        codigo = uuid.uuid4().hex[:8].upper()
        cache.set(cache_key, codigo, 60 * 10)

        email = Email(
            titulo="Redefinição de senha",
            corpo="Esse é o código da redefinição de senha: %s" % codigo,
            destinatarios=[usuario.email],
        )

        email.send()


class ConfirmarCodigoRedefinirSenhaSerializer(serializers.Serializer):
    usuario = serializers.SlugRelatedField(
        queryset=Usuario.objects.all(), slug_field="email"
    )
    codigo = serializers.CharField()

    def validate(self, attrs):
        dados = super().validate(attrs)

        codigo = dados["codigo"]
        usuario = dados["usuario"]

        cache_key = REDEFINIR_SENHA_CACHE_KEY % usuario.email
        codigo_cache = cache.get(cache_key, None)

        if codigo_cache is None:
            raise serializers.ValidationError(
                {"mensagem": _("A redefinição de senha expirou")}
            )

        if codigo != codigo_cache:
            raise serializers.ValidationError(
                {"mensagem": _("O código informado é inválido")}
            )

        cache.delete(cache_key)

        return dados


class RedefinirSenhaSerializer(serializers.Serializer):
    usuario = serializers.SlugRelatedField(
        queryset=Usuario.objects.all(), slug_field="email"
    )
    nova_senha = serializers.CharField()

    def validate_nova_senha(self, value):
        validate_password(value)
        return value

    def save(self):
        validated_data = self.validated_data
        nova_senha = validated_data["nova_senha"]
        usuario = validated_data["usuario"]

        usuario.password = make_password(nova_senha)
        usuario.save()


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }

        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        usuario = Usuario.objects.filter(
            email=authenticate_kwargs[self.username_field]
        ).first()

        if not usuario:
            raise exceptions.AuthenticationFailed(
                {
                    "mensagem": _(
                        "Esse email não está cadastrado em nossa base de dados"
                    )
                },
                "not_found_account",
            )

        if not usuario.is_active:
            raise exceptions.AuthenticationFailed(
                {"mensagem": _("Esse usuário está inativado")},
                "inactive_account",
            )

        self.user = authenticate(**authenticate_kwargs)

        authentication_rule = import_string(
            settings.SIMPLE_JWT["USER_AUTHENTICATION_RULE"]
        )

        if not authentication_rule(self.user):
            raise exceptions.AuthenticationFailed(
                {"mensagem": _("A senha informada está incorreta")},
                "incorret_password",
            )

        data = {}
        token = self.get_token(self.user)
        data["access"] = str(token.access_token)

        if settings.SIMPLE_JWT["UPDATE_LAST_LOGIN"]:
            update_last_login(None, self.user)

        return data

    @classmethod
    def get_token(cls, user):  # , assinatura
        token = super().get_token(user)
        token["user_name"] = user.first_name
        token["user_last_name"] = user.last_name
        token["user_full_name"] = user.get_full_name()
        return token
