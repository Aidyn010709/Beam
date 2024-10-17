from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


from applications.network.decorators import handle_network_access
from applications.network.filters import NetworkFilter
from applications.network.queries import network_query
from applications.network.serializers import (
    NetworkDetailSerializer,
    NetworkListSerializer,
    NetworkSerializer,
)

class NetworkViewSet(ModelViewSet):
    queryset = network_query.all()
    serializer_class = NetworkSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = NetworkFilter
    filter_backends = [
        DjangoFilterBackend,
    ]

    # @handle_network_access(access_field="access_clients")
    # def get_queryset(self):
    #     return self.queryset

    def get_serializer_class(self):
        if self.action == "list":
            return NetworkListSerializer
        elif self.action == "retrieve":
            return NetworkDetailSerializer
        return NetworkSerializer
    
