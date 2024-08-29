import os

from typing import Literal

EnviromentVar = Literal[
    "DJANGO_SECRET_KEY",
    "DJANGO_DEBUG",
    "DJANGO_MODE",
    "DJANGO_EXECUTION_MODE",
    "DATABASE_NAME",
    "DATABASE_USER",
    "DATABASE_PASSWORD",
    "DATABASE_HOST",
    "DATABASE_PORT",
    "EMAIL_PASSWORD",
    "RABBITMQ_HOST",
    "RABBITMQ_USER",
    "RABBITMQ_PSSWD",
    "RABBITMQ_PORT",
    "REDIS_HOST",
    "REDIS_PORT",
    "INTEGRATION_TOKEN",
]


environ_keys = EnviromentVars

def get_environ_var(key: EnviromentVar):
    return os.environ.get(key)
