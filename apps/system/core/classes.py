import os
import json

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.core.signing import Signer, BadSignature


class SingletonMeta(type):
    """
    Metaclass paras Singleton
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DinamicAttrs:
    """Objeto de utilidade para acessar atributos via `.` ao invés
    da inteface de `[<chave>]`
    """

    def __init__(self, dados):
        self.raw = dados
        for chave, valor in dados.items():
            if isinstance(valor, dict):
                valor = DinamicAttrs(valor)
            setattr(self, chave, valor)


class JSONDinamicAttrs(DinamicAttrs):
    """Adaptação da classe `DinamicAttrs` para utilizar um arquivo JSON"""

    def __init__(self, path):
        dados = json.loads(open(path).read())
        super().__init__(dados)


class CachedFile:
    """Singleton para cachear um arquivo. Sempre que for necessário
    abrir um arquivo, se o seu path já tiver sido utilizado, irá
    retornar uma instância no cache em vez de abrir o arquivo novamente.
    """

    __files = {}

    def __new__(cls, path, **kwargs):
        mode = kwargs.get("mode", "r")
        if cls.__files.get(path, None) is None:
            file = open(path, mode)
            cls.__files[path] = file

        return cls.__files[path]


class Email:
    """Classe construção e envio de email."""

    def __init__(self, titulo, mensagem="", destinatarios=[], from_email=settings.EMAIL_HOST_USER):
        self._titulo = titulo
        self._mensagem = mensagem
        self.destinatarios = destinatarios

        self._template = None
        self._from_email = from_email

    def add_template(self, path, **context):
        if self._template is not None:
            raise Exception("Um template já foi adicionado")

        self._template = get_template(path)
        self._template.render(context)
        return self

    def add_destinatario(self, destinatario):
        if destinatario in self.destinatarios:
            raise Exception("Destinatário já foi adicionado")

        if len(self.destinatarios) == 100:
            raise Exception("Número máximo de destinatários atingido")

        self.destinatarios.append(destinatario)
        return self

    def enviar(self):
        if len(self.destinatarios) == 0:
            raise Exception("Informe ao menos um destinatário")

        email = EmailMultiAlternatives(
            self._titulo, self._mensagem, self._from_email, self.destinatarios
        )
        if self._template is not None:
            email.attach_alternative(self._template, "text/html")

        email.send(fail_silently=False)


class Encryptor(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._secret_key = os.environ.get("DJANGO_SECRET_KEY")
        self._signer = Signer(self._secret_key)

    def encrypt(self, value):
        return self._signer.sign(value)

    def decrypt(self, value):
        try:
            return self._signer.unsign(value)
        except BadSignature:
            return None
