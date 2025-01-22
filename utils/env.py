import ast
import os
from typing import Literal

EnviromentVar = Literal[
    # api
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
    "REDIS_HOST",
    "REDIS_PORT",
    # rabbit
    "RABBITMQ_CONNECTION_STRING",
    # cloudflare
    "CLOUDFLARE_API_TOKEN",
    # sentry
    "SENTRY_DSN",
    # google
    "GOOGLE_OAUTH2_CLIENT_ID",
    "GOOGLE_OAUTH2_CLIENT_SECRET",
    "GOOGLE_OAUTH2_PROJECT_ID",
    # papertrail
    "PAPERTRAIL_HOSTNAME",
    "PAPERTRAIL_PORT",
    # twilio
    "TWILIO_ACCOUNT_SID",
    "TWILIO_AUTH_TOKEN",
    "TWILIO_PHONE_NUMBER",
    # backblaze
    "BACKBLAZE_APPLICATION_ID",
    "BACKBLAZE_APPLICATION_KEY",
    "BACKBLAZE_BUCKET_NAME",
]


def get_env_var(key: EnviromentVar) -> str:
    return os.environ.get(key) # type: ignore


def get_bool_from_env(name: EnviromentVar, default_value=False) -> bool:
    if name in os.environ:
        value = os.environ[name]
        try:
            return ast.literal_eval(value)
        except ValueError as exc:
            raise ValueError(
                f"'{value}' não é um valor válido para '{name}'") from exc
    return default_value
