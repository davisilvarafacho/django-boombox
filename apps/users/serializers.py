from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string

from rest_framework import exceptions
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField

from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    password = PasswordField()

    class Meta:
        model = Usuario
        exclude = (
            "is_superuser",
            "groups",
            "user_permissions",
            "is_staff",
        )


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

        usuario = Usuario.objects.filter(email=authenticate_kwargs[self.username_field]).first()
        if not usuario:
            raise exceptions.AuthenticationFailed(
                {"mensagem": _("Esse email não está cadastrado em nossa base de dados")},
                "not_found_account",
            )

        if not usuario.is_active:
            raise exceptions.AuthenticationFailed(
                {"mensagem": _("Esse usuário está inativado")},
                "inactive_account",
            )

        self.user = authenticate(**authenticate_kwargs)

        authentication_rule = import_string(settings.SIMPLE_JWT["USER_AUTHENTICATION_RULE"])
        if not authentication_rule(self.user):
            raise exceptions.AuthenticationFailed(
                {"mensagem": _("A senha informada está incorreta")},
                "incorret_password",
            )
    
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["access"] = str(refresh.access_token)

        if settings.SIMPLE_JWT["UPDATE_LAST_LOGIN"]:
            update_last_login(None, self.user)

        return data
        
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
