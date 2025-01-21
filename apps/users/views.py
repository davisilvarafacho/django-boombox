from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView

from apps.system.base.views import BaseViewSet

from .serializers import (
    Usuario,
    UsuarioSerializer,
    ReenviaEmailConfirmacaoSerializer,
    ConfirmarEmailSerializer,
    EnviarEmailRedefinicaoSenhaSerializer,
    ConfirmarCodigoRedefinirSenhaSerializer,
    RedefinirSenhaSerializer,
)


class LoginViewSet(TokenObtainPairView):
    authentication_classes = []
    permission_classes = [AllowAny]


class AuthViewSet(BaseViewSet):
    serializer_class = UsuarioSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_classes = {
        "cadastro": UsuarioSerializer,
        "confirmar_email": ConfirmarEmailSerializer,
        "reenviar_email_confirmacao": ReenviaEmailConfirmacaoSerializer,
        "enviar_email_redefinicao_senha": EnviarEmailRedefinicaoSenhaSerializer,
        "confirmar_codigo_redefinir_senha": ConfirmarCodigoRedefinirSenhaSerializer,
        "redefinir_senha": RedefinirSenhaSerializer,
    }

    @action(methods=["get"], detail=False)
    def validar_cadastro_email(self, request):
        email = request.query_params.get("email", None)
        if email is None:
            raise ValidationError({"email": "Essa query é obrigatória"})

        try:
            Usuario.objects.get(email=email)
            return Response({"cadastrado": True})
        except Usuario.DoesNotExist:
            return Response({"cadastrado": False})

    @action(methods=["post"], detail=False)
    def cadastro(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["post"], detail=False)
    def confirmar_email(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=False)
    def reenviar_email_confirmacao(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=False)
    def enviar_email_redefinicao_senha(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

    @action(methods=["post"], detail=False)
    def confirmar_codigo_redefinir_senha(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response()

    @action(methods=["post"], detail=False)
    def redefinir_senha(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()
