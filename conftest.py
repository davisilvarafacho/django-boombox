import os

import dotenv
import pytest
from auditlog.registry import auditlog

dotenv.load_dotenv()

os.environ["DJANGO_MODE"] = "testing"


@pytest.fixture(autouse=True)
def use_test_database(settings):
    settings.DATABASES["default"]["NAME"] = "test_django_boombox"


@pytest.fixture(autouse=True)
def disable_auditlog_fixture():
    for model in auditlog.get_models():
        auditlog.unregister(model)


@pytest.fixture(autouse=True)
def use_dummy_cache_backend(settings):
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
