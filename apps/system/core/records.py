import json
import logging
import os

from django.utils.module_loading import import_string

from django_multitenant.utils import set_current_tenant

from apps.system.tenants.models import Ambiente

logger = logging.getLogger(__name__)


class DefaultRecord:
    def __init__(self, model, id_fields, active, raw_data):
        if isinstance(model, str):
            self.model = import_string(model)
        else:
            self.model = model

        self.id_fields = id_fields
        self.active = active
        self.raw = raw_data
        self._model_instance = None

        for chave, valor in raw_data.items():
            setattr(self, chave, valor)

        self.identifiers = {pk: raw_data[pk] for pk in id_fields}

    @property
    def model_instance(self):
        try:
            if self._model_instance is None:
                self._model_instance = self.model.objects.get(**self.identifiers)
            return self._model_instance
        except self.model.DoesNotExist:
            return None

    @property
    def exists(self):
        return self.model_instance is not None

    @property
    def inactive(self):
        return not self.active

    def create(self, **save_kwargs):
        instance = self.model(**self.raw)
        instance.save(**save_kwargs)
        self._model_instance = instance
        return instance

    def delete(self):
        instance = self.model_instance
        if instance is None:
            raise self.model.DoesNotExists

        instance.delete()

    def __str__(self):
        ids = " ".join([f"{chave}='{valor}'" for chave, valor in self.identifiers.items()])
        return f"<DefaultRecord model={self.model.__name__} {ids}>"


class DefaultRecordsManger:
    default_records_path = "data/default/records/"

    def __init__(self):
        self.__cached_models = {}

    def multitenant_apply_updates(self):
        ambientes = Ambiente.objects.all()
        for ambiente in ambientes:
            set_current_tenant(ambiente)
            self.apply_updates()

    def apply_updates(self):
        records = self.get_records()
        try:
            for record in records:
                if record.active and not record.exists:
                    record.create()

                elif not record.active and record.exists:
                    record.delete()
        except Exception:
            logger.error("Erro ao criar registro do sistema!")

    def get_records(self):
        files = self.get_files()
        records = []
        for file in files:
            records_to_insert = json.load(file)
            for dataset in records_to_insert:
                model = self.get_model(dataset["model"])
                data = dataset["data"]
                id_fields_map = dataset["id_fields_map"]
                active = dataset["active"]

                default_record = DefaultRecord(
                    model=model,
                    id_fields=id_fields_map,
                    active=active,
                    raw_data=data,
                )

                records.append(default_record)
        return tuple(records)

    def get_files(self):
        files = []
        for file_name in os.listdir(self.default_records_path):
            path = self.default_records_path + file_name
            file = open(path)
            files.append(file)
        return tuple(files)

    def delete_inactives(self):
        records = self.get_records()
        for record in records:
            if not record.exists or record.inactive:
                continue

            record.delete()

    def populate(self):
        records = self.get_records()
        for record in records:
            if record.exists or record.inactive:
                continue

            record.create()

    def get_model(self, path):
        if path not in self.__cached_models:
            self.__cached_models[path] = import_string(path)
        return self.__cached_models[path]
