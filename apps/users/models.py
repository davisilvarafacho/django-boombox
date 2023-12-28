from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.db import models


"""Sobreescrita do usuário.

Aqui, estamos sobrescrevendo o usuário padrão do Django, para o usuário não tenha
mais os campos first_name, last_name e username, e sim, apenas o campo nome e email,
removendo a dependência do username, que é um campo obrigatório no Django.
"""

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
    nome = models.CharField(_("nome"), max_length=100)
    email = models.EmailField(_("email"), unique=True)

    username = None
    first_name = None
    last_name = None

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome"]

    objects = UsuarioManager()

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = "usuario"
        ordering = ["id"]
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")
