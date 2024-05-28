from django.core.management.base import BaseCommand

from apps.system.core.records import DefaultRecordsManger


class Command(BaseCommand):
    help = 'Popula os novos registros e exclui os inativos'

    def handle(self, *args, **options):
        populator = DefaultRecordsManger()
        populator.apply_records_changes()
