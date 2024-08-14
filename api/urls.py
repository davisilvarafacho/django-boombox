from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

apps_urls = [path("api/", include(app + ".urls")) for app in settings.BOOMBOX_APPS]

urlpatterns = [
    path("admin/", admin.site.urls),
    *apps_urls,
]

if settings.IN_DEVELOPMENT:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
