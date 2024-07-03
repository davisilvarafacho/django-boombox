from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.system.core.classes import Email

from .serializers import Usuario, UsuarioSerializer


class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def perform_create(self, serializer):
        serializer.save(is_active=False)
        self.enviar_email_confirmacao(serializer.instance.email)
    
    def enviar_email_confirmacao(self, email):
        email = Email(_("Confirme seu email"), corpo="Clique no link abaixo para confirmar sua conta", destinatarios=[email])
        email.send()

    @action(methods=['get'], detail=False)
    def verificar_cadastro_email(self, request, pk):
        email_usuario = pk  # estou passando o email do usuário no lugar da pk
        try:
            Usuario.objects.get(email=email_usuario)
            return Response()
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True)
    def confirmar_email(self, request, pk):
        instance = self.get_object()
        if instance.is_active:
            return Response({
                "mensagem": _("Esse usuário já está ativo")
            }, status=status.HTTP_400_BAD_REQUEST)

        instance.is_active = True
        instance.save()
        return Response()

    @action(methods=['post'], detail=True)
    def reenviar_email(self, request, pk):
        instance = self.get_object()
        if instance.is_active:
            return Response({
                "mensagem": _("Esse usuário já está ativo")
            }, status=status.HTTP_400_BAD_REQUEST)

        self.enviar_email_confirmacao(instance.email)
        return Response()