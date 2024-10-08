import datetime
import os
import warnings
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from django.utils.translation import gettext_lazy as _

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
    # dev
    "127.0.0.1",
    "localhost",
    # prod
]

CSRF_TRUSTED_ORIGINS = [
    # dev
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    # prod
]

CSRF_TRUSTED_ORIGINS = []


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
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


AUTH_QUERY_PARAM_NAME = "jwt"


MULTITENANCY_DATABASE_PREFIX = "boombox"


RABBITMQ_HOST = get_env_var("RABBITMQ_HOST")

RABBITMQ_USER = get_env_var("RABBITMQ_USER")

RABBITMQ_PSSWD = get_env_var("RABBITMQ_PSSWD")

RABBITMQ_PORT = get_env_var("RABBITMQ_PORT")


CORS_ALLOW_ALL_ORIGINS = True


HEADLESS_ONLY = True


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

CACHALOT_QUERY_KEYGEN = "apps.system.tenants.cache.gen_query_cache_key"

CACHALOT_TABLE_KEYGEN = "apps.system.tenants.cache.gen_query_table_key"


HEADLESS_FRONTEND_URLS = {
    "account_confirm_email": "https://app.domain.com/account/verify-email/{key}",
    "account_reset_password_from_key": "https://domain.com/account/password/reset/key/{key}",
    "account_signup": "https://domain.com/account/signup",
}


SPECTACULAR_SETTINGS = {
    "TITLE": "Django-Boombox API Docs",
    "DESCRIPTION": "Documentação auto generativa com drf-spetacular",
    "VERSION": "0.0.1-beta",
    "SERVE_INCLUDE_SCHEMA": False,
}
