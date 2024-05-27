from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.system.base.models import Base


class Configuracao(Base):
    codigo = models.CharField(
        _("código"), max_length=125, unique=True, help_text="Nome padronizado do código"
    )

    descricao = models.CharField(
        _("descrição"), max_length=350, help_text="Descrição da utilidade dessa configuração"
    )

    valor = models.CharField(
        _("valor"), max_length=50, help_text="Valor da configuração"
    )

    class Meta:
        db_table = "configuracao"
        ordering = ["-id"]
        verbose_name = _("Configuração")
        verbose_name_plural = _("Configurações")

    def __str__(self):
        return self.codigo
