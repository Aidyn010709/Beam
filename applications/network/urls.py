from django.urls import include, path
from rest_framework import routers

from applications.network.views import NetworkViewSet

router = routers.DefaultRouter()

router.register("", NetworkViewSet, basename="network")


urlpatterns = [
    path("", include(router.urls)),
]
