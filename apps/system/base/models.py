from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# TODO colocar um warning que me fale quando eu não usei o self.get_queryset


class Base(models.Model):
    """
    Modelo base contendo campos padrão para controle interno do
    sistema, como data e hora de criação e alteração.
    """

    SIM_NAO = (
        ("S", "Sim"),
        ("N", "Não"),
    )

    ZERO_UM = (
        ("0", "0"),
        ("1", "1"),
    )

    ativo = models.CharField(
        _("ativo"),
        max_length=1,
        choices=SIM_NAO,
        default="S",
        help_text="Se o registro está ativo ou não",
    )

    data_criacao = models.DateField(
        _("data de criação"),
        auto_now_add=True,
        help_text="Data da criação do registro",
    )

    hora_criacao = models.TimeField(
        _("hora de criação"),
        auto_now_add=True,
        help_text="Hora da criação do registro",
    )

    data_ultima_alteracao = models.DateField(
        _("data da última alteração"),
        auto_now=True,
        help_text="Data da última alteração",
    )

    hora_ultima_alteracao = models.TimeField(
        _("hora da última alteração"),
        auto_now=True,
        help_text="Hora da última alteração",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("criador do registro"),
        on_delete=models.PROTECT,
        help_text="Usuário que criou o registro",
        related_name="%(app_label)s_%(class)s_criador",
    )

    class Meta:
        abstract = True


zero_um = Base.ZERO_UM
sim_nao = Base.SIM_NAO


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

    pais = models.CharField(_("País"), max_length=20, blank=True, default="Brasil")
    cep = models.CharField(_("Cep"), max_length=8)
    estado = models.CharField(_("Estado"), choices=ESTADOS, max_length=2)
    cidade = models.CharField(_("Cidade"), max_length=150)
    bairro = models.CharField(_("Bairro"), max_length=150)
    rua = models.CharField(_("Rua"), max_length=150)
    numero = models.CharField(_("Número"), max_length=8)
    complemento = models.CharField(
        _("Complemento"), max_length=100, blank=True, default=""
    )

    class Meta:
        abstract = True


estados = Endereco.ESTADOS
