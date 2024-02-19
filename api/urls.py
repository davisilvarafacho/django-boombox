from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Essa variável percorre os aplicativos registrados em `settings.BOOMBOX_APPS`
# e automáticamente registra o arquivo `urls.py` de app. Isso faz com que seja
# obrigatório que, todos os apps, tenham um arquivo `urls.py` e dentro dele a
# variável `urlpatterns` criada.

apps_urls = [path("api/v1/", include(app + ".urls")) for app in settings.BOOMBOX_APPS]

urlpatterns = [
    path("admin/", admin.site.urls),
    *apps_urls,
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
