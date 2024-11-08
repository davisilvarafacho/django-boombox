import datetime
import os
import logging
import warnings

from pathlib import Path

from django.core.management.utils import get_random_secret_key
from django.utils.translation import gettext_lazy as _

from corsheaders.defaults import default_headers

from utils.env import get_bool_from_env, get_env_var

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = get_env_var("DJANGO_SECRET_KEY")

DEBUG = get_bool_from_env("DJANGO_DEBUG", True)

MODE = get_env_var("DJANGO_MODE")

IN_DEVELOPMENT = MODE == "development"

IN_PRODUCTION = MODE == "production"

EXECUTION = get_env_var("DJANGO_EXECUTION_MODE")


if not SECRET_KEY and DEBUG:
    warnings.warn("'SECRET_KEY' não foi configurada, using a random temporary key.")
    SECRET_KEY = get_random_secret_key()


ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]


SITE_ID = 1

ADMINS = [("Davi Silva Rafacho", "davi.s.rafacho@gmail.com")]

MANAGERS = ADMINS


if IN_PRODUCTION:
    import sentry_sdk

    sentry_sdk.init(
        dsn=get_env_var("SENTRY_DSN"),
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
]

LIBS_APPS = [
    "auditlog",
    "cachalot",
    "corsheaders",
    "django_filters",
    "django_extensions",
    "rest_framework",
]

BOOMBOX_APPS = [
    "apps.system.base",
    "apps.system.core",
    "apps.system.conf",
    "apps.users",
]

INSTALLED_APPS = DJANGO_APPS + LIBS_APPS + BOOMBOX_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]


ROOT_URLCONF = "api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_env_var("DATABASE_NAME"),
        "USER": get_env_var("DATABASE_USER"),
        "PASSWORD": get_env_var("DATABASE_PASSWORD"),
        "HOST": get_env_var("DATABASE_HOST"),
        "PORT": get_env_var("DATABASE_PORT"),
    },
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{get_env_var('REDIS_HOST')}:{get_env_var('REDIS_PORT')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


AUTH_USER_MODEL = "users.Usuario"


DATE_FORMAT = "d/m/Y"

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_TZ = True


USE_I18N = True

LANGUAGES = [
    ("pt-br", _("Português (Brasil)")),
    ("en", _("Inglês")),
    ("es", _("Espanhol")),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]


STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = None

EMAIL_PORT = None

EMAIL_HOST_USER = None

EMAIL_HOST_PASSWORD = get_env_var("EMAIL_PASSWORD")

DEFAULT_FROM_EMAIL = None


LOGGING_ROOT = os.path.join(BASE_DIR, "logs/")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(levelname)s %(message)s"},
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
        "api_formatter": {
            "format": "%(asctime)s [%(levelname)s] %(name)s - LOG - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
        "error_formatter": {
            "format": "%(asctime)s [%(levelname)s] %(name)s - ERROR - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
        "cloud_formatter": {
            "format": "%(asctime)s boombox %(name)s: [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
    },
    "filters": {
        "warnings_filter": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda record: record.levelno == logging.WARNING,
        },
        "api_filter": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda record: record.levelno >= logging.INFO,
        },
        "error_filter": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda record: record.levelno >= logging.ERROR,
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "api_formatter",
        },
        "api_activity": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_ROOT, "api_activity.log"),
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 10,
            "formatter": "api_formatter",
            "filters": ["api_filter"],
        },
        "api_warnings": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_ROOT, "warnings.log"),
            "maxBytes": 1024 * 1024 * 10,
            "backupCount": 2,
            "formatter": "api_formatter",
            "filters": ["warnings_filter"],
        },
        "api_errors": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_ROOT, "errors.log"),
            "maxBytes": 1024 * 1024 * 50,
            "backupCount": 10,
            "formatter": "error_formatter",
            "filters": ["error_filter"],
        },
        "api_errors_mail": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "error_formatter",
            "filters": ["error_filter"],
        },
        "api_cloud_log": {
            "level": "DEBUG",
            "class": "logging.handlers.SysLogHandler",
            "formatter": "cloud_formatter",
            "address": (get_env_var("PAPERTRAIL_HOSTNAME"), get_env_var("PAPERTRAIL_PORT")),
        },
    },
}


if IN_PRODUCTION:
    LOGGING["root"]["handlers"] += ["api_cloud_log", "api_errors_mail"]


# django-boombox
AUTH_QUERY_PARAM_NAME = "jwt"

TENANT_HOST_HEADER = "X-Tenant-Host"


# corsheaders
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = list(default_headers) + [TENANT_HOST_HEADER]


# rest_framework
REST_FRAMEWORK = {
    "PAGE_SIZE": 30,
    "DEFAULT_PAGINATION_CLASS": "apps.system.core.pagination.CustomPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "apps.system.core.authentications.JwtHeaderTenantAuthentication",
        "apps.system.core.authentications.JwtQueryParamTenantAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
}


# rest_framework_simplejwt
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=365 if IN_DEVELOPMENT else 1),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=365 if IN_DEVELOPMENT else 3),
    "TOKEN_OBTAIN_SERIALIZER": "apps.users.serializers.LoginSerializer",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "UPDATE_LAST_LOGIN": True,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "sub",
    "AUDIENCE": None,
    "ISSUER": None,
}


# django-axes
AXES_FAILURE_LIMIT = 7

AXES_COOLOFF_TIME = datetime.timedelta(minutes=30)

AXES_RESET_ON_SUCCESS = True

AXES_USERNAME_FORM_FIELD = "login"


# drf-flex-fields
EXPAND_PARAM = "display"

MAXIMUM_EXPANSION_DEPTH = 3

FIELDS_PARAM = "fields"

OMIT_PARAM = "supress"
