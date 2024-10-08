from django.core.validators import MinLengthValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from auditlog.registry import auditlog


class UsuarioManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    username = None

    first_name = models.CharField(_("nome"), max_length=30)
    last_name = models.CharField(_("sobrenome"), max_length=60)
    email = models.EmailField(_("email"), unique=True)
    cellphone = models.CharField(
        _("celular"), validators=(MinLengthValidator(11),), null=True
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "cellphone"]

    objects = UsuarioManager()

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = "usuario"
        ordering = ["id"]
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")
        indexes = [
            models.Index(fields=["email"], name="email_idx"),
        ]


auditlog.register(Usuario)
