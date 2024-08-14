from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import TenantsViewSet

router_v1 = DefaultRouter()
router_v1.register("tenants", TenantsViewSet, "tenants")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
