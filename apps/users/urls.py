from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    token_obtain_pair as token_obtain,
    token_refresh,
    token_verify,
)

from .views import UsuarioViewSet, custom_token_obtain_pair_view

router = DefaultRouter()
router.register("usuarios", UsuarioViewSet, "usuarios")

urlpatterns = [
    path("", include(router.urls)),
    path("api/token/obtain/", custom_token_obtain_pair_view, name="token_obtain"),
    path("api/token/refresh/", token_refresh, name="token_refresh"),
    path("api/token/verify/", token_verify, name="token_verify"),
]
