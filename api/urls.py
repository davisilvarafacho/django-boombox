from django.contrib import admin
from django.urls import path, include
from django.conf import settings

apps_urls = [path("api/v1/", include(app + ".urls")) for app in settings.BOOMBOX_APPS]

urlpatterns = [
    path("admin/", admin.site.urls),
] + apps_urls
