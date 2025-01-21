from calendar import monthrange

from django.utils import timezone


def gerar_primeiro_e_ultimo_dia_mes(data=None):
    if data is None:
        data = timezone.now()
    primeiro_dia = data.replace(day=1)
    _, numero_ultimo_dia = monthrange(data.year, data.month)
    ultimo_dia = data.replace(day=numero_ultimo_dia)
    return primeiro_dia, ultimo_dia
