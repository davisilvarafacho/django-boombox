import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.models import TenantModel


class Ambiente(TenantModel):
    tenant_id = "id"

    uuid = models.UUIDField(_("uuid"), default=uuid.uuid4, editable=False)
    mb_subdominio = models.CharField(_("subdomínio"), max_length=30, unique=True)
    mb_nome = models.CharField(_("nome"), max_length=100)

    class Meta:
        db_table = "ambiente"
        ordering = ["-id"]
        verbose_name = _("Ambiente")
        verbose_name_plural = _("Ambientes")
