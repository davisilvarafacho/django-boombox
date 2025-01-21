from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import AuthViewSet, LoginViewSet

router_auth = DefaultRouter()
router_auth.register("", AuthViewSet, "auth")

urlpatterns = [
    path("auth/", include(router_auth.urls)),
    path("auth/token/obtain/", LoginViewSet.as_view()),
]
