class DefaultData:
    """Representação de um dado padrão do sistema.
    """

    def __init__(self, model, raw_data, pk_fields):
        self.model = model
        self.raw = raw_data
        self.pk_fields = pk_fields

        for chave, valor in raw_data.items():
            setattr(self, chave, valor)

        self.identifiers = {pk: raw_data[pk] for pk in pk_fields}
    
    def __setattr__(self, __name, __value) -> None:
        setattr(self, __name, __value)
        self.raw[__name] = __value

    def get_model_instance(self):
        return self.model.objects.get(**self.identifiers)


class DatabasePopulator:
    """Classe responsável por popular o banco de dados com os
    dados padrões do sistema.
    """

    def __init__(self, data=None, **kwargs):
        if not data:
            import os
            from django.conf import settings

            defaulf_data_path = None
            try:
                defaulf_data_path = settings.BOOMBOX['DEFAULT_DATA_PATH']
            except AttributeError as exc:
                raise AttributeError('A variável BOOMBOX["DEFAULT_DATA_PATH"] não pode ficar em branco no arquivo settings.py') from exc


    def start_populating(self):
        """Inicia o processo de popular o banco de dados.
        """
        self._populate()
    
    def _populate(self):
        """Popula o banco de dados com os dados padrões do sistema.
        """
