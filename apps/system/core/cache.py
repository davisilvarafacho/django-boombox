from cachalot.utils import get_query_cache_key, get_table_cache_key

def gen_query_cache_key(*args, **kwargs):
    return "db-" + get_query_cache_key(*args, **kwargs)

def gen_query_table_key(*args, **kwargs):
    return "db-" + get_table_cache_key(*args, **kwargs)

