from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import APIException
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from beam.custom_permissions import CustomDjangoModelPermissions
from applications.network.decorators import handle_network_access

from applications.product.filters import CategoryFilter, ProductFilter
from applications.product.models import Category, Product
from applications.network.models import Network
from applications.product.serializers import (
    CategorySerializer,
    ProductSerializer,
)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name"]
    filterset_class = CategoryFilter
    permission_classes = (
        IsAuthenticated,
        CustomDjangoModelPermissions,
    )
    queryset = Category.objects.select_related("network", "indicator")

    @handle_network_access(access_field="network__access_clients")
    def get_queryset(self):
        network = self.request.query_params.get("network")
        if network:
            return self.queryset.filter(network=network)
        return self.queryset

    def perform_create(self, serializer):
        network_id = self.request.data.get("network")
        if network_id:
            network = Network.objects.get(id=network_id)
        serializer.save(network=network)


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name"]
    permission_classes = (IsAuthenticated, CustomDjangoModelPermissions)
    filterset_class = ProductFilter
    queryset = Product.objects.select_related("network", "indicator")

    @handle_network_access(access_field="network__access_clients")
    def get_queryset(self):
        network = self.request.query_params.get("network")
        if network:
            return self.queryset.filter(network=network)
        return self.queryset
    
    def perform_create(self, serializer):
        network_id = self.request.data.get("network")
        if network_id:
            network = Network.objects.get(id=network_id)
        serializer.save(network=network)
