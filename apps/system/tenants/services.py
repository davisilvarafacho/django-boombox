from django.conf import settings
from django.core.management import call_command
from django.db import connection, connections

from apps.system.core.records import DefaultRecordsManger

from apps.users.models import Usuario


class TenantManager:
    DEAFULT_DATABASE_NAME = None

    def __init__(self, dados):
        self.dados = dados
        self.cursor = connection.cursor()
    
    def criar_tenant(self):
        self.criar_banco_dados()
        self.alterar_conexao_db()
        self.migrar_banco_dados()
        self.criar_usuario_root()
        self.popular_registros_padroes()
        self.reiniciar_conexao_db()

    def criar_banco_dados(self):
        self.cursor.execute(f"CREATE DATABASE {self.dados['nome_banco_dados']};")

    def criar_usuario_root(self):
        usuario = Usuario()
        usuario.first_name = self.dados["nome_usuario"]
        usuario.last_name = self.dados["sobrenome_usuario"]
        usuario.email = self.dados["email_usuario"]
        usuario.password = self.dados["senha_usuario"]
        usuario.save()

    def migrar_banco_dados(self):
        call_command("migrate")

    def popular_registros_padroes(self):
        manager = DefaultRecordsManger()
        manager.populate()

    def alterar_conexao_db(self):
        connection.close()
        settings.DATABASES["default"]["NAME"] = self.dados["nome_banco_dados"]
        connections["default"].close()
        connection.ensure_connection()

    def reiniciar_conexao_db(self):
        connection.close()
        settings.DATABASES["default"]["NAME"] = self.DEAFULT_DATABASE_NAME
        connections["default"].close()
        connection.ensure_connection()
