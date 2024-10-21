import ast
import os

from typing import Literal

EnviromentVar = Literal[
    "DJANGO_SECRET_KEY",
    "DJANGO_DEBUG",
    "DJANGO_MODE",
    "DJANGO_EXECUTION_MODE",
    "DJANGO_LOG_LEVEL",
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


def get_env_var(key: EnviromentVar) -> str:
    return os.environ.get(key)


def get_bool_from_env(name: EnviromentVar, default_value=False) -> bool:
    if name in os.environ:
        value = os.environ[name]
        try:
            return ast.literal_eval(value)
        except ValueError as exc:
            raise ValueError(f"'{value}' não é um valor válido para '{name}'") from exc
    return default_value
