# Generated by Django 5.0 on 2024-05-23 19:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("conf", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="configuracao",
            name="owner",
            field=models.ForeignKey(
                help_text="Usuário que criou o registro",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_criador",
                to=settings.AUTH_USER_MODEL,
                verbose_name="criador do registro",
            ),
        ),
    ]
