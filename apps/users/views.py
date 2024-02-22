from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from apps.system.core.classes import Email

from .throttles import LoginThrottle
from .serializers import Usuario, UsuarioSerializer


class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [LoginThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            if settings.SEND_EMAIL_ON_LOGIN_FAIL:
                self.send_email_on_fail(request.data["username"])

            raise InvalidToken(e.args[0])

        if settings.SEND_EMAIL_ON_LOGIN_SUCCESS:
                self.send_email_on_success(request.data["username"])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def send_email_on_fail(self, email_usuario: str) -> None:
        email = Email(_("Login falhou"), _("Houve uma tentativa de login na sua conta".format(email_usuario)))
        email.add_destinatario(email_usuario)
        email.enviar()

    def send_email_on_success(self, email_usuario: str) -> None:
        email = Email(_("Login realizado"), _("O usuário {} realizou login".format(email_usuario)))
        email.add_destinatario(email_usuario)
        email.enviar()


custom_token_obtain_pair_view = CustomTokenObtainPairView.as_view()
