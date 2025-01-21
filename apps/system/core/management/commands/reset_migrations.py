from os import makedirs
from os.path import exists
from shutil import rmtree

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection


class Comand(BaseCommand):
    help = "Reseta o histórico de migrações do banco de dados do sistema"

    def handle(self, *args, **options):
        self.reset_migrations_folders()

    def reset_migrations_folders(self):
        self.delete_all_migrations_folders()
        self.create_all_migrations_folders()
        self.clean_django_migrations_table()
        self.do_make_migrations()
        self.apply_migrations()

    def delete_all_migrations_folders(self):
        for app in settings.BOOMBOX_APPS:
            app_path = app.replace(".", "/")
            migration_path = app_path + "/migrations"

            if exists(migration_path):
                rmtree(migration_path)


    def create_all_migrations_folders(self):
        for app in settings.BOOMBOX_APPS:
            app_path = app.replace(".", "/")
            migration_path = app_path + "/migrations"
            init_path = migration_path + "/__init__.py"

            if not exists(init_path):
                makedirs(migration_path)

            if not exists(init_path):
                with open(init_path, "x") as f:
                    f.close()

    def clean_django_migrations_table(self):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM django_migrations")
        rows = cursor.fetchall()

        for row in rows:
            id, app, name, _ = row
            system_apps = ("admin", "auth", "contenttypes", "sessions", "accounts", "authtoken")
            if app not in system_apps and name != "0001_initial":
                cursor.execute("DELETE FROM django_migrations WHERE id = %s", [id])

    def do_make_migrations(self):
        call_command("makemigrations")

    def apply_migrations(self):
        call_command("migrate")
