import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.models import TenantModel
from django_multitenant.fields import TenantForeignKey


from apps.system.base.models import Base


class Tenant(TenantModel):
    tenant_id = "id"

    uuid = models.UUIDField(_("uuid"), default=uuid.uuid4, editable=False)
    tn_subdominio = models.CharField(_("subdomínio"), max_length=30, unique=True)
    tn_nome = models.CharField(_("nome"), max_length=100)

    class Meta:
        db_table = "tenant"
        ordering = ["-id"]
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")


class UsuarioTenant(Base):
    usuario = TenantForeignKey(
        verbose_name=_("usuário"),
        to="users.Usuario",
        on_delete=models.PROTECT,
        null=True,
        related_name="tenants_usuario",
    )

    empresa = models.ForeignKey(
        verbose_name=_("tenant"),
        to="tenants.Tenant",
        on_delete=models.PROTECT,
        null=True,
        related_name="usuarios_tenant",
    )

    class Meta:
        db_table = "usuario_tenant"
        unique_together = ["id", "empresa"]
        verbose_name = _("Usuário da Empresa")
        verbose_name_plural = _("Usuários das Empresas")
        constraints = [
            models.UniqueConstraint(fields=["id", "empresa"], name="id_usuario_tenant_unique"),
            models.UniqueConstraint(fields=["empresa", "usuario"], name="empresa_usuario_unique"),
        ]
