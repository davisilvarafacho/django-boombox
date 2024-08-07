import os

from typing import Literal


API_ENV_KEYS = (
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
)

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
]


class EnviromentVars:
    DJANGO_SECRET_KEY = "DJANGO_SECRET_KEY"
    DJANGO_DEBUG = "DJANGO_DEBUG"
    DJANGO_MODE = "DJANGO_MODE"
    DJANGO_EXECUTION_MODE = "DJANGO_EXECUTION_MODE"
    DATABASE_NAME = "DATABASE_NAME"
    DATABASE_USER = "DATABASE_USER"
    DATABASE_PASSWORD = "DATABASE_PASSWORD"
    DATABASE_HOST = "DATABASE_HOST"
    DATABASE_PORT = "DATABASE_PORT"
    EMAIL_PASSWORD = "EMAIL_PASSWORD"
    RABBITMQ_HOST = "RABBITMQ_HOST"
    RABBITMQ_USER = "RABBITMQ_USER"
    RABBITMQ_PSSWD = "RABBITMQ_PSSWD"
    RABBITMQ_PORT = "RABBITMQ_PORT"
    REDIS_HOST = "REDIS_HOST"
    REDIS_PORT = "REDIS_PORT"


environ_keys = EnviromentVars


def get_environ_var(key: EnviromentVar):
    if key not in API_ENV_KEYS:
        raise KeyError(f"{key} não é uma varíavel de ambiente válida")

    return os.environ.get(key)
