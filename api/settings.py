import ast
import datetime
import os
import warnings

from django.utils.translation import gettext_lazy as _
from django.core.management.utils import get_random_secret_key

from pathlib import Path


def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.environ[name]
        try:
            return ast.literal_eval(value)
        except ValueError as exc:
            raise ValueError(f"'{value}' não é um valor válido para '{name}'") from exc
    return default_value


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = get_bool_from_env("DJANGO_DEBUG", True)

MODE = os.environ.get("DJANGO_MODE", "development")

IN_DEVELOPMENT = MODE == "development"

IN_PRODUCTION = MODE == "production"


if not SECRET_KEY and DEBUG:
    warnings.warn("'SECRET_KEY' não foi configurada, using a random temporary key.")
    SECRET_KEY = get_random_secret_key()


ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
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
    "rest_framework",
    "corsheaders",
    "cachalot",
    "django_filters",
    "django_extensions",
]

BOOMBOX_APPS = [
    "apps.system.base",
    "apps.system.core",
    "apps.system.conf",
    "apps.users",
]

INSTALLED_APPS = DJANGO_APPS + LIBS_APPS + BOOMBOX_APPS


DJANGO_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

LIBS_MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
]

BOOMBOX_MIDDLEWARE = []

if DEBUG:
    BOOMBOX_MIDDLEWARE.append("apps.system.core.middlewares.DevMiddleware")

MIDDLEWARE = DJANGO_MIDDLEWARE + LIBS_MIDDLEWARE + BOOMBOX_MIDDLEWARE


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
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT"),
    },
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}",
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

EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")

DEFAULT_FROM_EMAIL = None


RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")

RABBITMQ_USER = os.environ.get("RABBITMQ_USER")

RABBITMQ_PSSWD = os.environ.get("RABBITMQ_PSSWD")

RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT")


DJANGO_EXECUTION_MODE = os.environ.get("DJANGO_EXECUTION_MODE")


CORS_ALLOW_ALL_ORIGINS = True


REST_FRAMEWORK = {
    "PAGE_SIZE": 30,
    "DEFAULT_PAGINATION_CLASS": "apps.system.core.pagination.CustomPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}


SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=90 if MODE == "development" else 1),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=120 if MODE == "development" else 3),
    "TOKEN_OBTAIN_SERIALIZER": "apps.users.serializers.LoginSerializer",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "sub",
    "AUDIENCE": None,
    "ISSUER": None,
}
