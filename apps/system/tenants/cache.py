from django.conf import settings

from cachalot.utils import get_query_cache_key, get_table_cache_key
from threadlocals.threadlocals import get_current_request

from utils.jwt import decode_jwt


prefixo_nome_db = settings.MULTITENANCY_DATABASE_PREFIX


def get_tenant():
    request = get_current_request()
    try:
        token = request.headers[settings.AUTH_QUERY_PARAM_NAME]
        payload = decode_jwt(token)
        return payload["user_tenant"]
    except KeyError:
        token = request.GET.get(settings.AUTH_QUERY_PARAM_NAME, None)
        payload = decode_jwt(token)
        return payload["user_tenant"]


def gen_query_cache_key(*args, **kwargs):
    try:
        tenant = get_tenant()
        return tenant + get_query_cache_key(*args, **kwargs)
    except:
        return f"{prefixo_nome_db}-{get_query_cache_key(*args, **kwargs)}"


def gen_query_table_key(*args, **kwargs):
    try:
        tenant = get_tenant()
        return tenant + get_table_cache_key(*args, **kwargs)
    except:
        return f"{prefixo_nome_db}-{get_table_cache_key(*args, **kwargs)}"
