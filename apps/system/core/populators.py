import os

from django.utils.module_loading import import_string


class DefaultRecord:
    """Representação de um registro padrão do sistema."""

    def __init__(self, model, id_fields, ativo, raw_data):
        if isinstance(model, str):
            self.model = import_string(model)
        else:
            self.model = model

        self.ativo = model
        self.id_fields = id_fields
        self.raw = raw_data
        self._instance = None

        for chave, valor in raw_data.items():
            setattr(self, chave, valor)

        self.identifiers = {pk: raw_data[pk] for pk in id_fields}

    @property
    def model_instance(self):
        try:
            if self._instance is None:
                self._instance = self.model.objects.get(**self.identifiers)
            return self._instance
        except self.model.DoesNotExist:
            return None

    @property
    def exists(self):
        return self.model_instance is not None

    def create(self):
        instance = self.model(**self.raw)
        instance.save()
        return instance

    def delete(self):
        instance = self.model_instance
        if instance is None:
            raise self.model.DoesNotExists

        instance.delete()

    def __setattr__(self, __name, __value) -> None:
        setattr(self, __name, __value)
        self.raw[__name] = __value


class DatabasePopulator:
    """Classe responsável por popular o banco de dados com os
    dados padrões do sistema.
    """

    default_records_path = "data/default/records/"

    def populate_database(self):
        records = self.get_data()
        for data in records:
            model = data.pop("model", None)
            ids_fields = data.pop("ids_fields", None)

            if model is None or ids_fields is None:
                raise ValueError

            r = DefaultRecord(model, ids_fields, data)
    
    def get_data(self):
        files = self.get_files()

    def get_files(self):
        files = []
        for file_name in os.listdir(self.default_records_path):
            file = open(self.default_records_path + file_name)
            files.append(file)
        return files