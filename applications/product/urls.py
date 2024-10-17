from django.urls import include, path
from rest_framework import routers

from applications.product.views import (
    CategoryViewSet,
    ProductViewSet,
)

router = routers.DefaultRouter()
router.register("product", ProductViewSet, basename="products")
router.register("category", CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns += router.urls
