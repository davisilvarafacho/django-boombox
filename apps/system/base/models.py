import json

from django.conf import settings
from django.db import models
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _

from django_multitenant.models import TenantModel


class SimNao(models.TextChoices):
    SIM = "S", _("Sim")
    NAO = "N", _("Não")


class Base(TenantModel):
    """
    Modelo base contendo campos padrão para controle interno do
    sistema, como data e hora de criação e alteração.
    """

    tenant_id = "ambiente_id"
    
    ativo = models.CharField(
        _("ativo"),
        max_length=1,
        choices=SimNao,
        default="S",
    )

    data_criacao = models.DateField(
        _("data de criação"),
        auto_now_add=True,
    )

    hora_criacao = models.TimeField(
        _("hora de criação"),
        auto_now_add=True,
    )

    data_ultima_alteracao = models.DateField(
        _("data da última alteração"),
        auto_now=True,
    )

    hora_ultima_alteracao = models.TimeField(
        _("hora da última alteração"),
        auto_now=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("criador do registro"),
        on_delete=models.PROTECT,
    )

    ambiente = models.ForeignKey(
        "tenants.Tenant",
        verbose_name=_("tenant"),
        on_delete=models.PROTECT,
    )

    @property
    def json(self):
        data = model_to_dict(self)
        return json.dumps(data, default=str)


    class Meta:
        abstract = True


class Endereco(models.Model):
    ESTADOS = (
        ("RO", "Rondônia"),
        ("AC", "Acre"),
        ("AM", "Amazonas"),
        ("RR", "Roraima"),
        ("PA", "Pará"),
        ("AP", "Amapá"),
        ("TO", "Tocantins"),
        ("MA", "Maranhão"),
        ("PI", "Piauí"),
        ("CE", "Ceará"),
        ("RN", "Rio Grande do Norte"),
        ("PB", "Paraíba"),
        ("PE", "Pernambuco"),
        ("AL", "Alagoas"),
        ("SE", "Sergipe"),
        ("BA", "Bahia"),
        ("MG", "Minas Gerais"),
        ("ES", "Espírito Santo"),
        ("RJ", "Rio de Janeiro"),
        ("SP", "São Paulo"),
        ("PR", "Paraná"),
        ("SC", "Santa Catarina"),
        ("RS", "Rio Grande do Sul"),
        ("MS", "Mato Grosso do Sul"),
        ("MT", "Mato Grosso"),
        ("GO", "Goiás"),
        ("DF", "Distrito Federal"),
        ("EX", "Exterior"),
    )

    pais = models.CharField(_("país"), max_length=20, blank=True, default="Brasil")
    cep = models.CharField(_("cep"), max_length=8)
    estado = models.CharField(_("estado"), choices=ESTADOS, max_length=2)
    cidade = models.CharField(_("cidade"), max_length=150)
    bairro = models.CharField(_("bairro"), max_length=150)
    rua = models.CharField(_("rua"), max_length=150)
    numero = models.CharField(_("número"), max_length=8)
    complemento = models.CharField(_("complemento"), max_length=100, blank=True, default="")

    class Meta:
        abstract = True


estados = Endereco.ESTADOS
