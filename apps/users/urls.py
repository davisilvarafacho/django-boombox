from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import token_obtain_pair as login_view

from .views import UsuarioViewSet

router_v1 = DefaultRouter()
router_v1.register("usuarios", UsuarioViewSet, "usuarios")

urlpatterns = [
    path("auth/login/", login_view),
    path("v1/", include(router_v1.urls)),
]
