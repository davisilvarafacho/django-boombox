from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Exibe no console todos os modelos de seus aplicativos"

    def handle(self, *args, **options):
        for app in settings.BOOMBOX_APPS:
            app_name = app.split(".")[-1]
            for model in apps.get_app_config(app_name).get_models():
                print(app, "|", model)
