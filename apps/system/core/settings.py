import os

from django.conf import settings
from django.test.signals import setting_changed
from django.utils.translation import gettext_lazy as _
from rest_framework.settings import APISettings


USER_SETTINGS = getattr(settings, "BOOMBOX", None)

DEFAULTS = {
    "DEFAULT_DATA_PATH": os.path.join(settings.BASE_DIR, "apps/system/core/data/json/default/"),
    "SEND_EMAIL_ON_LOGIN_FAIL": False,
    "SEND_EMAIL_ON_LOGIN_SUCCESS": False,
}

IMPORT_STRINGS = ()

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):
    global api_settings

    setting, value = kwargs["setting"], kwargs["value"]

    if setting == "SIMPLE_JWT":
        api_settings = APISettings(value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_api_settings)
