# Generated by Django 5.1.3 on 2025-01-21 20:18

import django_multitenant.mixins
import django_multitenant.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ambiente",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, verbose_name="uuid"
                    ),
                ),
                (
                    "mb_subdominio",
                    models.CharField(
                        max_length=30, unique=True, verbose_name="subdomínio"
                    ),
                ),
                ("mb_nome", models.CharField(max_length=100, verbose_name="nome")),
            ],
            options={
                "verbose_name": "Ambiente",
                "verbose_name_plural": "Ambientes",
                "db_table": "ambiente",
                "ordering": ["-id"],
            },
            bases=(django_multitenant.mixins.TenantModelMixin, models.Model),
            managers=[
                ("objects", django_multitenant.models.TenantManager()),
            ],
        ),
    ]
