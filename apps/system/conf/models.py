from typing import Literal

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.system.base.models import Base


class Configuracao(Base):
    owner = None

    class opcoes_configuracoes:
        pass

    primitive_types_codes_map = {}

    configuracao_sistema = Literal[""]

    cf_codigo = models.CharField(_("código"), max_length=40 , unique=True, editable=False)
    cf_descricao = models.CharField(_("descrição"), max_length=100)
    cf_valor = models.CharField(_("valor"), max_length=25)

    @classmethod
    def normalize_value(cls, codigo: configuracao_sistema, valor: str):
        tipo_valor_parametro = cls.primitive_types_codes_map[codigo]
        if tipo_valor_parametro == str:
            return valor

        elif tipo_valor_parametro == int:
            return int(valor)

        elif tipo_valor_parametro == float:
            return float(valor)

        elif tipo_valor_parametro == bool:
            return True if valor == "True" else False

        else:
            raise Exception

    @classmethod
    def get_configuracao(cls, codigo: configuracao_sistema):
        param = cls.objects.get(cf_codigo=codigo)
        return cls.normalize_value(codigo, param.cf_valor)

    class Meta:
        db_table = "configuracao"
        ordering = ["-id"]
        verbose_name = _("Configuração")
        verbose_name_plural = _("Configurações")

    def __str__(self):
        return self.cf_codigo


configuracoes = Configuracao.opcoes_configuracoes
configuracao_sistema = Configuracao.configuracao_sistema
