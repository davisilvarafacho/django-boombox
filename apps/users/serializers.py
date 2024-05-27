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
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)    
        return token
